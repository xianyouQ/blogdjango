# encoding=utf8
from blogdjango.models import *
from blog import settings
import traceback

priority = {"denied":0,"read":1,"write":2}


class BlogAction:
	"""
	blog操作查询类
	"""
	def __init__(self,user):
		self.user = user

	
	def queryArticles(self,userName=None):
		"""
		根据用户(名)获取其博客文章以及其他信息
		"""
		context = {}
		articles = []
		try:
			if userName == None: ##获取自己的博客主页数据
				articles = BlogText.objects.select_related('blog__userDetail').filter(blog__userDetail__user=self.user)
			elif self.blog_permission_required(priority["read"],userName):
				articles = BlogText.objects.select_related('blog__userDetail__user').filter(blog__userDetail__user__username__exact=userName)
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
		except Exception:
			context["error"] = "Internal Server Error"
			context["err_user"] = userName
			return context
		if len(articles) > 0:
			context["articles"] = articles
			context["blog"] = articles[0].blog
			context["userDetail"] = articles[0].blog.userDetail
		else:
			context["error"] = "can't get anything"
			context["err_user"] = userName
		return context
		
	def queryActicleComment(self,acticleId,userName=None):
		"""
		根据用户(名)以及他的文章id获取评论
		"""
		context = {}
		try:
			if userName == None: ##获取自己的评论
				comments = Comment.objects.select_related(comment_user).filter(blogtext__id__exact=acticleId).filter(blogtext__blog__userDetail__user=self.user)
			elif self.blog_permission_required(priority["read"],userName):
				comments = Comment.objects.select_related(comment_user).filter(blogtext__id__exact=acticleId).filter(blogtext__blog__userDetail__user__username__exact=userName)
			else:
				context["error"] = {}
		except DoesNotExist:
			context["error"] = "Can't get anything comments the user you asked"
			context["err_user"] = userName
			return context
		context["comment"] = comments
		return context

	def askBlogPermission(self,userName):
		"""
		请求查看某个blog的权限
		"""
		context = {}
		try:
			userDetail = UserDetail.objects.get(user__username__exact=userName)
			askPermisson = BlogPermisson()   ##可能需要检查是否曾经申请过
			askPermisson.ask_from_user = self.user
			askPermisson.asked_user = userDetail
			askPermisson.save()
		except DoesNotExist:
			context["error"] = "No such User:" + userName
			return context
		return context
		
	def queryAskedPermission(self):
		"""
		查看自己收到的权限请求
		"""
		context = {}
		try:
			askPermissons = BlogPermisson.objects.select_related(ask_from_user).filter(asked_user=self.user).filter(need_confirm=True)
		except DoesNotExist:
			return context
		permissions = []
		for permission in askPermissons:
			permissions.append(permission.ask_from_user)
		context["permisson"] = permissions
		return context
		
		
	def processAskedPermission(self,requestContext):
		"""
		处理权限请求
		"""
		context = {}
		for priority,usernameList in requestContext.items():
			try:
				changenum = BlogPermisson.objects.filter(asked_user=self.user).filter(ask_from_user__user__username__in=usernameList).update(blog_priority=priority,need_confirm=False)
				context[priority]=changenum
			except Exception:
				context[priority] = 0
		return context
			
			
	def addNewComment(self,username,acticleId,message,parent_id):
		"""
		添加新评论
		"""

		context = {}
		try:
			if not self.blog_permission_required(priority["write"],userName):
				context["denied"] = True
				return context
			parentComment = Comment.objects.select_related(blogtext).filter(blogtext__blog__userDetail__user__username__exact=username).get(acticleId_exact=acticleId)
			newComment = Comment()
			newComment.blogtext = parentComment.blogtext
			newComment.parent_comment = parentComment
			newComment.context = message
			newComment.comment_user = self.user
			newComment.save()
		except:
			context["error"] = "can't commit comment request"
		return context
		
	def addNewActicle(self,title,message,published=False):
		"""
		添加新文章
		"""
		context = {}
		try:
			blog = Blog.objects.get(userDetail__user=self.user)
			acticle = BlogText()
			acticle.blog = blog
			acticle.context = message
			acticle.is_publish = published
			acticle.save()
			context["acticleId"] = acticle.id
		except:
			context["error"] = "can't process request"
		return context
		
	def updateActicle(self,title,acticleId,message=None,published=False):
		"""
		更新文章
		"""
		context = {}
		context["acticleId"] = acticleId
		try:
			updatenum = BlogText.objects.filter(blog__userDetail__user=self.user).filter(id=acticleId).update(context=message,is_publish=published)
			context["update"] = updatenum
		except:
			context["update"] = 0
		return context

	def blog_permission_required(self,permission,username):
		"""
		检查对某个账户blog的访问权限，如果没有会根据redirect_template返回对应页面,或者抛出PermissionDenied
		"""
		try:
			dbpermission = BlogPermisson.objects.filter(asked_user__user=user).filter(from_user__user__username__exact=username).values("blog_priority")
			print len(dbpermission)
			if len(dbpermission) > 0 and dbpermission[0] >= permission:
				return True
			else:
				return False
		except Exception,e:
				return False
	