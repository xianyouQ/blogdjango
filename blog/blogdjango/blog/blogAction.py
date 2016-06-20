# encoding=utf8
from blogdjango.models import *
from blog import settings
import traceback
from django.core.serializers import serialize
from blogdjango.serializers.serializerHelper import ModelToJson
import base64
from django.core.files.base import ContentFile
import time,os,sys,json

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
				shortArticles = ShortArticle.objects.filter(blog=article.blog)[0:3]
				photos = BlogPhoto.objects.filter(blog=article.blog)[0:3]
			elif self.blog_permission_required(priority["read"],userName):
				article = BlogText.objects.select_related('blog__userDetail').filter(blog__userDetail__username__exact=userName,is_publish=True)[0]
				shortArticles = ShortArticle.objects.filter(blog=article.blog)[0:3]
				photos = BlogPhoto.objects.filter(blog=article.blog)[0:3]
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
				querycomments = Comment.objects.select_related("comment_user").filter(blogtext__id__exact=requestContext["articleId"]).filter(blogtext__blog__userDetail__user=self.user)
			elif self.blog_permission_required(priority["read"],userName):
				querycomments = Comment.objects.select_related("comment_user").filter(blogtext__id__exact=requestContext["articleId"]).filter(blogtext__blog__userDetail__user__username__exact=userName)
				context["username"] = userName
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = userName
			comments = {}
			for comment in querycomments:
				if comment.parent_comment == None:
					comments[comment.id] = []
					newComment = {}
					newComment["comment"] = ModelToJson(comment)
					newComment["user"] = comment.comment_user.username
					comments[comment.id].append(newComment)
				else:
					newComment = {}
					newComment["comment"] = ModelToJson(comment)
					newComment["user"] = comment.comment_user.username
					comments[comment.parent_comment.id].append(newComment)  #是否会导致多次查询数据库
			context["comment"] = comments
			context["code"] = 200
		except KeyError:
			context["code"] = 400
			return context
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
			userDetail = UserDetail.objects.get(username__exact=userName)
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
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			askPermissons = BlogPermisson.objects.select_related("ask_from_user__user").filter(asked_user=mUserDetail).filter(need_confirm=True)
		except:
			traceback.print_exc()
			context["code"] = 500
			return context
		context["permissons"] = askPermissons
		context["userDetail"] = mUserDetail
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
				changenum = BlogPermisson.objects.filter(asked_user__user=self.user).filter(ask_from_user__username__in=usernameList).update(blog_priority=priority,need_confirm=False)
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
					filter(blogtext__id__exact=requestContext["articleId"]).filter(id__exact=requestContext["parentId"])[0]
				elif self.blog_permission_required(priority["write"],username):
					parentComment = Comment.objects.select_related("blogtext").filter(blogtext__blog__userDetail__username__exact=username). \
					get(blogtext__id__exact=requestContext["articleId"]).filter(id__exact=requestContext["parentId"])[0]
					context["username"] = userName
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = userName
					return context
				newComment.blogtext = parentComment.blogtext
				newComment.parent_comment = parentComment
				toUser =  UserDetail.objects.get(username__exact=requestContext["toUser"]) #能否根据主键直接设置外键
				newComment.comment_to_user = toUser
			else: 
				if userName == None:
					blogText = BlogText.objects.filter(blog__userDetail__user__exact=self.user).filter(id__exact=requestContext["articleId"])[0]
				elif self.blog_permission_required(priority["write"],username):
					blogText = BlogText.objects.filter(blog__userDetail__username__exact=username).filter(id__exact=requestContext["articleId"])[0]
					context["username"] = username
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = username
					return context
				newComment.blogtext = blogText
			newComment.context = requestContext["message"]
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			newComment.comment_user = mUserDetail
			newComment.save()
			context["newId"] = newComment.id
			context["comment_time"] = newComment.comment_time.isoformat()
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
		if "articleId" in requestContext:
			try:
				updatenum = BlogText.objects.filter(blog__userDetail__user=self.user).filter(id=requestContext["articleId"]). \
				update(context=requestContext.get("content"),is_publish=requestContext.get("is_publish",False),article_tags=requestContext.get("tags",""),blog_text_title=requestContext.get("title",""))
				if updatenum == 0:
					context["code"] = 400
				elif updatenum > 1:
					context["code"] = 500
				else:
					context["code"] = 200
				context["articleId"] = requestContext.get("articleId")
			except KeyError:
				context["code"] = 400
				return context
			except:
				traceback.print_exc()
				context["code"] = 500
		else:
			try:
				blog = Blog.objects.get(userDetail__user=self.user)
				article = BlogText()
				article.blog = blog
				article.context = requestContext["content"]
				article.is_publish = requestContext.get("is_publish",False)      ######暂存不知道为啥会有问题。。。。。。。。。。。
				article.article_tags = requestContext.get("tags","")
				article.blog_text_title = requestContext.get("title","")
				article.save()
				context["articleId"] = article.id
				context["create_time"] = article.create_time.isoformat()
				context["code"] = 200
			except KeyError:
				context["code"] = 400
				return context
			except:
				traceback.print_exc()
				context["code"] = 500
		return context


	def queryArticle(self,username=None,tag="",echpage=5,startNum=sys.maxint):
		"""
		查询文章
		"""
		context = {}
		try:
			if username == None:
				Articles = BlogText.objects.select_related("blog__userDetail").filter(blog__userDetail__user=self.user).filter(article_tags__icontains=tag).filter(id__lt=startNum)[0:echpage]
			elif self.blog_permission_required(priority["read"],userName):
				Articles = BlogText.objects.select_related("blog__userDetail").filter(blog__userDetailr__username__exact=username).filter(is_publish__exact=True).filter(article_tags__icontains=tag).filter(id__lt=startNum)[0:echpage]
				context["username"] = username
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = username				
			context["code"] = 200
			context["Articles"] = ModelToJson(Articles)
			context["userDetail"] = 	Articles[0].blog.userDetail
		except:
			context["code"] = 500
			traceback.print_exc()

		return context


	def blog_permission_required(self,permission,username):
		"""
		检查对某个账户blog的访问权限，如果没有会根据redirect_template返回对应页面,或者抛出PermissionDenied
		"""

		try:
			dbpermission = BlogPermisson.objects.filter(ask_from_user__user=self.user).filter(asked_user__username__exact=username).values("blog_priority")
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
			context["create_time"] = str(mShortArticle.create_time)
		except KeyError:
			context["code"] = 400
		except:
			context["code"] = 500
		context["code"] = 200
		return  context
		
	def queryShortArticle(self,username=None,echpage=12,startNum=sys.maxint):
		"""
		查询所有的短博文
		"""
		context = {}
		try:
			if username == None:
				shortArticles = ShortArticle.objects.select_related("blog__userDetail").filter(blog__userDetail__user=self.user).filter(id__lt=startNum)[0:echpage]
			elif self.blog_permission_required(priority["read"],userName):
				shortArticles = ShortArticle.objects.select_related("blog__userDetail").filter(blog__userDetail__username__exact=username).filter(id__lt=startNum)[0:echpage]
				context["username"] = username
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = username	
			context["code"] = 200
			context["shortArticles"] = ModelToJson(shortArticles)
			context["userDetail"] = 	shortArticles[0].blog.userDetail
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
			context["photoUrl"] = mUserDetail.getheadphotourl()
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
			context["photos"] = []
			print requestContext.FILES
			for upload in requestContext.FILES.values():
				file_suffix = upload.name.split(".")[-1]
				filename = str(int(time.time())) + "."+file_suffix
				print filename
				upload_content = ContentFile(upload.read(),filename)
				mBlogPhoto = BlogPhoto()
				mBlogPhoto.blog = mBlog
				mBlogPhoto.photo = upload_content
				mBlogPhoto.save()
				newBlogPhoto = {}
				newBlogPhoto["url"] = mBlogPhoto.getphotourl()
				newBlogPhoto["id"] = mBlogPhoto.id
				context["photos"].append(newBlogPhoto)
			context["code"] = 200
		except KeyError:
			context["code"] = 400
		except:
			traceback.print_exc()
			context["code"] = 500
		return context
		
	def requeryPhoto(self,username = None,echpage=5,startNum=sys.maxint):
		"""
		查询图片
		"""
		context = {}
		try:
			if username == None:
				photos = BlogPhoto.objects.select_related("blog__userDetail").filter(blog__userDetail__user=self.user).filter(id__lt=startNum)[0:echpage]
			elif self.blog_permission_required(priority["read"],userName):
				photos = BlogPhoto.objects.select_related("blog__userDetail").filter(blog__userDetail__username__exact=username).filter(id__lt=startNum)[0:echpage]
				context["username"] = username
			else:
				context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
				context["username"] = username	
			context["code"] = 200
			context["photos"] = []
			context["userDetail"] = 	photos[0].blog.userDetail
			for photo in photos:
				newphoto = {}
				newphoto["id"] = photo.id
				newphoto["url"] = photo.getphotourl
				context["photos"].append(newphoto)
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
			file = requestContext.FILES['file'] ##获取文件名拿到对应的格式
			filename = int(time.time())
			strstr = "%Y" + os.path.sep + "%m" + os.path.sep + "%d"
			path=time.strftime(strstr, time.localtime() )
			truepath = os.path.join(settings.MEDIA_ROOT,article_photo_dir, path)
			if not os.path.isdir(truepath):
				os.makedirs(truepath)
			fp = open(os.path.join(truepath,str(filename) +".jpg"), 'wb')
			for chunk in file.chunks():
				fp.write(chunk)
			fp.close()
			context["code"] = 200
			context["url"] = os.path.sep + article_photo_dir + os.path.sep + path + os.path.sep + str(filename) + ".jpg"
		except KeyError:
			context["code"] = 400
		except:
			traceback.print_exc()
			context["code"] = 500
		return context
	def uploadUserDetail(self,requestContext):
		"""
		上传用户资料
		"""
		context = {}
		try:
			updatenum = UserDetail.objects.filter(user__exact=self.user).update(nickname=requestContext["nickname"],signature=requestContext["signature"])
			if updatenum == 1:
				context["code"] = 200
			else:
				context["code"] = 500
			
		except KeyError:
			context["code"] = 400
		except:
			traceback.print_exc()
			context["code"] = 500
		return context
	def queryUserDetail(self):
		"""
		查询用户资料
		"""
		context = {}
		try:
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			context["userDetail"] = mUserDetail
			context["code"] = 200
		except:
			context["code"] = 500
		return context
