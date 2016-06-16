# encoding=utf8
from blogdjango.models import *
from blog import settings
import traceback
from django.core.serializers import serialize
import base64
from django.core.files.base import ContentFile
import time,os

priority = {"denied":0,"read":1,"write":2}

class BlogAction:
	"""
	blog操作查询类
	"""
	def __init__(self,user):
		self.user = user

	
	def queryIndexData(self,userName=None):
		"""
		根据用户(名)获取其主页数据
		"""
		context = {}
		try:
			if userName == None: ##获取自己的博客主页数据
				article = BlogText.objects.select_related('blog__userDetail').filter(blog__userDetail__user=self.user)[0]
				shortArticles = ShortArticle.objects.filter(blog=article.blog)[0:5]
				photos = BlogPhoto.objects.filter(blog=article.blog)[0:8]
			elif self.blog_permission_required(priority["read"],userName):
				article = BlogText.objects.select_related('blog__userDetail__user').filter(blog__userDetail__user__username__exact=userName,is_publish=True)[0]
				shortArticles = ShortArticle.objects.filter(blog=article.blog)[0:5]
				photos = BlogPhoto.objects.filter(blog=article.blog)[0:8]
				context["username"] = userName
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = userName
			context["lastArticle"] = article
			context["shortArticles"] = shortArticles
			context["blog"] = article.blog
			context["userDetail"] = article.blog.userDetail
			context["lastimgs"] = photos
			context["code"] ="200"
		except Exception:
			context["code"] ="500"
			return context

		return context
		
	def queryActicleComment(self,requestContext):
		"""
		根据用户(名)以及他的文章id获取评论
		"""
		context = {}
		userName = requestContext.get("username",None)
		try:
			if userName == None: ##获取自己的评论
				querycomments = Comment.objects.select_related("comment_user__user").filter(blogtext__id__exact=requestContext.get("acticleId")).filter(blogtext__blog__userDetail__user=self.user)
			elif self.blog_permission_required(priority["read"],userName):
				querycomments = Comment.objects.select_related("comment_user__user").filter(blogtext__id__exact=requestContext.get("acticleId")).filter(blogtext__blog__userDetail__user__username__exact=userName)
				context["username"] = userName
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = userName
			comments = {}
			for comment in querycomments:
				if comment.parent_comment == None:
					comments[comment.id] = []
					newComment = {}
					newComment["comment"] = serialize('json',[comment])[1:-1]
					newComment["user"] = serialize('json',[comment.comment_user.user])[1:-1]
					comments[comment.id].append(newComment)
				else:
					newComment = {}
					newComment["comment"] = serialize('json',[comment])[1:-1]
					newComment["user"] = serialize('json',[comment.comment_user.user])[1:-1]
					comments[comment.parent_comment.id].append(newComment)  #是否会导致多次查询数据库
			context["comment"] = comments
			context["code"] = 200
		except:
			traceback.print_exc()
			context["code"] = 500
			return context
		
		return context

	def askBlogPermission(self,userName):
		"""
		请求查看某个blog的权限
		"""
		context = {}
		try:
			if self.user.username == userName:
				context["code"] = 400
				return context
			userDetail = UserDetail.objects.get(user__username__exact=userName)
			#askPermisson,created = BlogPermisson.objects.get_or_create(ask_from_user__exact=mUserDetail,asked_user__exact=userDetail)
			try:
				askPermisson = BlogPermisson.objects.get(ask_from_user__user__exact=self.user,asked_user__exact=userDetail)
				if askPermisson.need_confirm == False and askPermisson.blog_priority == priority["denied"]:
					context["code"] = 403
					return context
			except BlogPermisson.DoesNotExist:
				mUserDetail = UserDetail.objects.get(user__exact=self.user)
				askPermisson = BlogPermisson(ask_from_user=mUserDetail,asked_user=userDetail)
				askPermisson.save()
		except UserDetail.DoesNotExist:
			context["code"] = 404
			return context
		except:
			context["code"] = 500
			traceback.print_exc()
			return context
		context["code"] = 200
		return context
		
	def queryAskedPermission(self):
		"""
		查看自己收到的权限请求
		"""
		context = {}
		try:
			askPermissons = BlogPermisson.objects.select_related("ask_from_user__user").filter(asked_user__user=self.user).filter(need_confirm=True)
		except:
			traceback.print_exc()
			context["code"] = 500
			return context
		context["permissons"] = askPermissons
		context["code"] = 200
		return context
		
		
	def processAskedPermission(self,requestContext):
		"""
		处理权限请求
		"""
		context = {}
		for priority,usernameStr in requestContext.items():
			usernameList = usernameStr.split(",")
			print usernameList
			try:
				changenum = BlogPermisson.objects.filter(asked_user__user=self.user).filter(ask_from_user__user__username__in=usernameList).update(blog_priority=priority,need_confirm=False)
				context[priority]=changenum
			except Exception:
				traceback.print_exc()
				context["code"] = 500
				context[priority] = 0
		context["code"]=200
		return context
			
			
			
	
	def addNewComment(self,requestContext):
		"""
		添加新评论
		"""

		context = {}
		userName = requestContext.get("username",None)
		if not requestContext.get("message","").strip():
			context["code"] = 404
			return context
		try:
			newComment = Comment()
			if "parentId" in requestContext:
				if userName == None: 
					parentComment = Comment.objects.select_related("blogtext").filter(blogtext__blog__userDetail__user__exact=self.user). \
					filter(blogtext__id__exact=requestContext.get("acticleId")).filter(id__exact=requestContext.get("parentId"))[0]
				elif self.blog_permission_required(priority["write"],username):
					parentComment = Comment.objects.select_related("blogtext").filter(blogtext__blog__userDetail__user__username__exact=username). \
					get(blogtext__id__exact=requestContext.get("acticleId")).filter(id__exact=requestContext.get("parentId"))[0]
					context["username"] = userName
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = userName
					return context
				newComment.blogtext = parentComment.blogtext
				newComment.parent_comment = parentComment
				toUser =  UserDetail.objects.get(user__username__exact=requestContext.get("toUser")) #能否根据主键直接设置外键
				newComment.comment_to_user = toUser
			else: 
				if userName == None:
					blogText = BlogText.objects.filter(blog__userDetail__user__exact=self.user).filter(id__exact=requestContext.get("acticleId"))[0]
				elif self.blog_permission_required(priority["write"],username):
					blogText = BlogText.objects.filter(blog__userDetail__user__username__exact=username).filter(id__exact=requestContext.get("acticleId"))[0]
					context["username"] = username
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = username
					return context
				newComment.blogtext = blogText
			newComment.context = requestContext.get("message")
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			newComment.comment_user = mUserDetail
			newComment.save()
			context["newId"] = newComment.id
			context["code"] = 200
		except KeyError:
			context["code"] = 400
		except:
			traceback.print_exc()
			context["code"] = 500
		return context
		
		
	def updateOrCreateArticle(self,requestContext):
		"""
		更新文章
		"""
		context = {}
		
		if not requestContext.get("content","").strip():
			context["code"] = 404
			return context
		if "acticleId" in requestContext:
			try:
				updatenum = BlogText.objects.filter(blog__userDetail__user=self.user).filter(id=requestContext.get("acticleId")). \
				update(context=requestContext.get("content"),is_publish=requestContext.get("is_publish",False),article_tags=requestContext.get("tags",""),blog_text_title=requestContext.get("title"))
				if updatenum == 0:
					context["code"] = 400
				elif updatenum > 1:
					context["code"] = 500
				else:
					context["code"] = 200
				context["acticleId"] = requestContext.get("acticleId")
			except KeyError:
				context["code"] = 400
				return context
			except:
				context["code"] = 500
		else:
			try:
				blog = Blog.objects.get(userDetail__user=self.user)
				article = BlogText()
				article.blog = blog
				article.context = requestContext.get("content")
				article.is_publish = requestContext.get("is_publish",False)      ######暂存不知道为啥会有问题。。。。。。。。。。。
				article.article_tags = requestContext.get("tags","")
				article.blog_text_title = requestContext.get("title","")
				article.save()
				context["acticleId"] = article.id
				context["code"] = 200
			except KeyError:
				context["code"] = 400
				return context
			except:
				context["code"] = 500
		return context


	def queryArticle(self,username=None,tag="",echpage=5,pagenum=0):
		"""
		查询文章
		"""
		context = {}
		NumStart = pagenum * echpage
		NumEnd = ( pagenum + 1 ) * echpage
		try:
			if username == None:
				Articles = BlogText.objects.filter(blog__userDetail__user=self.user).filter(article_tags__icontains=tag)[NumStart:NumEnd]
			elif self.blog_permission_required(priority["read"],userName):
				Articles = BlogText.objects.filter(blog__userDetail__user__username__exact=username).filter(is_publish__exact=True).filter(article_tags__icontains=tag)[NumStart:NumEnd]
				context["username"] = username
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = username				
			context["code"] = 200
			context["Articles"] = Articles
		except:
			context["code"] = 500
			traceback.print_exc()

		return context


	def blog_permission_required(self,permission,username):
		"""
		检查对某个账户blog的访问权限，如果没有会根据redirect_template返回对应页面,或者抛出PermissionDenied
		"""

		try:
			dbpermission = BlogPermisson.objects.filter(ask_from_user__user=self.user).filter(asked_user__user__username__exact=username).values("blog_priority")
			if len(dbpermission) > 0 and dbpermission[0].blog_priority >= permission:
				return True
			else:
				return False
		except Exception,e:
				return False
				
	def addNewShortArticle(self,requestContext):
		"""
		添加新的短博文
		"""
		context = {}
		try:
			if not requestContext.get("content","").strip():
				context["code"] = 404
				return context
			blog = Blog.objects.get(userDetail__user=self.user)
			mShortArticle = ShortArticle()
			mShortArticle.blog = blog
			mShortArticle.context = requestContext["content"]
			mShortArticle.save()
		except KeyError:
			context["code"] = 400
		except:
			context["code"] = 500
		context["code"] = 200
		return  context
		
	def queryShortArticle(self,username=None,echpage=5,pagenum=0):
		"""
		查询所有的短博文，后续加上分页功能
		"""
		context = {}
		NumStart = pagenum * echpage
		NumEnd = ( pagenum + 1 ) * echpage
		try:
			if username == None:
				shortArticles = ShortArticle.objects.filter(blog__userDetail__user=self.user)[NumStart:NumEnd]
			elif self.blog_permission_required(priority["read"],userName):
				shortArticles = ShortArticle.objects.filter(blog__userDetail__user__username__exact=username)[NumStart:NumEnd]
				context["username"] = username
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = username	
			context["code"] = 200
			context["shortArticles"] = shortArticles
		except:
			context["code"] = 500
			traceback.print_exc()
		return context

	def uploadHeadPhoto(self,requestContext):
		"""
		上传头像
		"""
		context = {}
		
		try:
			picName = requestContext.get("picName")
			photoData = base64.decodestring(requestContext.get('photo_base64').split(',')[1])
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			mUserDetail.head_photo = ContentFile(photoData,picName)
			mUserDetail.save()
			context["code"] = 200
			context["photoUrl"] = mUserDetail.head_photo.url
		except KeyError:
			context["code"] = 400
		except:
			context["code"] = 500
		return context
	
	def uploadPhoto(self,requestContext):
		"""
		上传图片
		"""
		context = {}
		try:
			mBlog = Blog.objects.get(userDetail__user__exact=self.user)
			context["photoUrls"] = []
			for upload in requestContext.FILES.values():
				mBlogPhoto = BlogPhoto.objects.create(blog=mBlog,photo=upload)
				context["photoUrls"].append(mBlogPhoto.photo.url)
			context["code"] = 200
		except KeyError:
			context["code"] = 400
		except:
			context["code"] = 500
		return context
		
	def requeryPhoto(self,username = None,echpage=5,pagenum=0):
		"""
		查询图片
		"""
		context = {}
		NumStart = pagenum * echpage
		NumEnd = ( pagenum + 1 ) * echpage
		try:
			if username == None:
				photos = BlogPhoto.objects.filter(blog__userDetail__user=self.user)[NumStart:NumEnd]
			elif self.blog_permission_required(priority["read"],userName):
				photos = BlogPhoto.objects.filter(blog__userDetail__user__username__exact=username)[NumStart:NumEnd]
				context["username"] = username
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = username	
			context["code"] = 200
			context["photos"] = photos
		except:
			context["code"] = 500
			traceback.print_exc()
		return context
		
	def uploadArticlePhoto(self,requestContext):
		"""
		上传博客中使用到的图片
		"""
		context = {}
		article_photo_dir = settings.ARTICLE_PHOTO_DIR
		try:
			file = requestContext.FILES['file']
			filename = int(time.time())
			strstr = "%Y" + os.path.sep + "%m" + os.path.sep + "%d"
			path=time.strftime(strstr, time.localtime() )
			truepath = os.path.join(article_photo_dir, path)
			if not os.path.isdir(truepath):
				os.makedirs(truepath)
			fp = open(os.path.join(truepath,str(filename) +".jpg"), 'wb')
			for chunk in file.chunks():
				fp.write(chunk)
			fp.close()
			context["code"] = 200
			context["url"] = path + os.path.sep + str(filename) + ".jpg"
		except KeyError:
			context["code"] = 400
		except:
			context["code"] = 500
		return context

