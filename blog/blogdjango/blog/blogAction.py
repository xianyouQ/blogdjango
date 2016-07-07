# encoding=utf8
from blogdjango.models import *
from blog import settings
import traceback
from django.core.serializers import serialize
from blogdjango.serializers.serializerHelper import ModelToJson
import base64
from django.core.files.base import ContentFile
import time,os,sys,json

class BlogAction:
	"""
	blog操作查询类
	"""
	def __init__(self,user):
		self.user = user

	def queryFriendDynamic(self,echpage=6,startNum=sys.maxint):
		"""
		查询好友动态
		"""
		context = {}
		try:
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			myFriends = Friends.objects.select_related("asked_user").filter(ask_from_user__exact=mUserDetail)
			asked_users = [Friend.asked_user for Friend in myFriends]
			mshortArticles = ShortArticle.objects.select_related("userDetail").filter(userDetail__in=asked_users).filter(id__lt=startNum)[0:echpage]
			queryShortComments = ShortComment.objects.select_related("comment_user").filter(shortarticle__in=list(mshortArticles))
			context["shortArticles"] = []
			for shortArticle in mshortArticles:
				parentCommentList = {}
				for comment in queryShortComments:
					if comment.shortarticle != shortArticle:
						continue
					if comment.parent_comment == None:
						parentCommentList[comment.id] = []
						newComment = {}
						newComment["comment"] = ModelToJson(comment)
						newComment["user"] = ModelToJson(comment.comment_user)
						parentCommentList[comment.id].append(newComment)
					else:
						newComment = {}
						newComment["comment"] = ModelToJson(comment)
						newComment["user"] = ModelToJson(comment.comment_user)
						parentCommentList[newComment["comment"]["parent_comment"]].append(newComment)
				newShortArticle = {}
				newShortArticle["shortArticle"] = ModelToJson(shortArticle)
				newShortArticle["userDetail"] = ModelToJson(shortArticle.userDetail)
				newShortArticle["comments"] = parentCommentList
				context["shortArticles"].append(newShortArticle)
			context["code"] = 200
			context["userDetail"] = ModelToJson(mUserDetail)
		except:
			traceback.print_exc()
			context["code"] = 500
		
		return context
	def queryIndexData(self,userName=None):
		"""
		根据用户(名)获取其主页数据
		"""
		context = {}
		try:
			if userName == None: ##获取自己的博客主页数据
				shortArticles = ShortArticle.objects.select_related('userDetail').filter(userDetail__user=self.user)[0:3]
				article = BlogText.objects.filter(userDetail__user=self.user)[0:1]
				photos = BlogPhoto.objects.filter(userDetail__user=self.user)[0:3]
				if len(shortArticles) == 0:
					mUserDetail = UserDetail.objects.get(user__exact=self.user)
				else:
					mUserDetail = shortArticles[0].userDetail
			else:
				mUserDetail,access = self.blog_permission_required(userName)
				if access:
					context["username"] = userName
					shortArticles = ShortArticle.objects.filter(userDetail__exact=mUserDetail)[0:3]
					article = BlogText.objects.filter(userDetail__exact=mUserDetail,is_publish=True)[0:1]
					photos = BlogPhoto.objects.filter(userDetail__exact=mUserDetail)[0:3]
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = userName
					context["code"] = 403
					return context
			context["lastArticle"] = ModelToJson(article[0])
			context["shortArticles"] = ModelToJson(shortArticles)
			context["userDetail"] = ModelToJson(mUserDetail)
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
				querycomments = Comment.objects.select_related("comment_user").filter(blogtext__id__exact=requestContext["articleId"]).filter(blogtext__userDetail__user=self.user)
			else:
				mUserDetail,access = self.blog_permission_required(userName)
				if access:
					querycomments = Comment.objects.select_related("comment_user").filter(blogtext__id__exact=requestContext["articleId"]).filter(blogtext__userDetail__username__exact=userName)
					context["username"] = userName

				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = userName
					context["code"] = 403
					return context
			comments = {}
			for comment in querycomments:
				if comment.parent_comment == None:
					comments[comment.id] = []
					newComment = {}
					newComment["comment"] = ModelToJson(comment)
					newComment["user"] = ModelToJson(comment.comment_user)
					comments[comment.id].append(newComment)
				else:
					newComment = {}
					newComment["comment"] = ModelToJson(comment)
					newComment["user"] = ModelToJson(comment.comment_user)
					comments[newComment["comment"]["parent_comment"]].append(newComment)
			context["comment"] = comments
			context["code"] = 200
		except KeyError:
			traceback.print_exc()
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
		print userName
		try:
			if self.user.username == userName:
				context["code"] = 400
				return context
			userDetail = UserDetail.objects.get(username__exact=userName)
			try:
				askPermisson = Friends.objects.get(ask_from_user__user__exact=self.user,asked_user__exact=userDetail)
				if askPermisson.need_confirm == False and not askPermisson.blog_priority:
					context["code"] = 403
					return context
			except Friends.DoesNotExist:
				mUserDetail = UserDetail.objects.get(username__exact=self.user.username)
				askPermisson = Friends(ask_from_user=mUserDetail,asked_user=userDetail)
				askPermisson.save()
		except UserDetail.DoesNotExist:
			traceback.print_exc()
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
			askPermissons = Friends.objects.select_related("ask_from_user").filter(asked_user=mUserDetail).filter(need_confirm=True)
		except:
			traceback.print_exc()
			context["code"] = 500
			return context
		context["permissons"] = askPermissons
		context["userDetail"] = ModelToJson(mUserDetail)
		context["code"] = 200
		return context
		
		
	def processAskedPermission(self,requestContext):
		"""
		处理权限请求
		"""
		context = {}
		for priority,usernameStr in requestContext.items():
			usernameList = usernameStr.split(",")
			try:
				changenum = Friends.objects.filter(asked_user__user=self.user).filter(ask_from_user__username__in=usernameList).update(blog_priority=priority,need_confirm=False)
				if priority:
					selfUserDetail = UserDetail.objects.get(user__exact=self.user)
					for username in usernameList:
						try:
							asked_user = UserDetail.objects.get(username__exact=username)
							Friends.objects.update_or_create(ask_from_user=selfUserDetail, asked_user=asked_user, need_confirm=False,blog_priority=True)
						except UserDetail.DoesNotExist:
							continue
				context[priority]=changenum
			except Exception:
				traceback.print_exc()
				context["code"] = 500
				context[priority] = 0
		context["code"]=200
		return context
			
			
			
	def processBlogPermission(self,requestContext):
		"""
		启/停权限控制
		"""
		context = {}
		
		try:
			update = requestContext["permission"]
			if update == "true":
				changenum = UserDetail.objects.filter(user__exact=self.user).update(access_confirm=True)
			else:
				changenum = UserDetail.objects.filter(user__exact=self.user).update(access_confirm=False)
			if changenum != 1:  #如果值本来就 不变，会是1的吗
				context["code"] = 404
			else:
				context["code"] = 200
		except KeyError:
			context["code"] = 400
		except:
			traceback.print_exc()
			context["code"] = 500
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
					parentComment = Comment.objects.select_related("blogtext").filter(blogtext__userDetail__user__exact=self.user). \
					filter(blogtext__id__exact=requestContext["articleId"]).filter(id__exact=requestContext["parentId"])[0]
				else: 
					userDetail,access = self.blog_permission_required(userName)
					if access:
						parentComment = Comment.objects.select_related("blogtext").filter(blogtext__userDetail__exact=userDetail). \
						filter(blogtext__id__exact=requestContext["articleId"]).filter(id__exact=requestContext["parentId"])[0]
						context["username"] = userName						
					else:
						context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
						context["username"] = userName
						context["code"] = 403
						return context
				newComment.blogtext = parentComment.blogtext
				newComment.parent_comment = parentComment
				toUser = UserDetail.objects.get(username__exact=requestContext["toUser"]) #能否根据主键直接设置外键
				newComment.comment_to_user = toUser
			else: 
				if userName == None:
					blogText = BlogText.objects.filter(userDetail__user__exact=self.user).filter(id__exact=requestContext["articleId"])[0]
				else:
					userDetail,access = self.blog_permission_required(userName)
					if access:
						blogText = BlogText.objects.filter(userDetail__exact=userDetail).filter(id__exact=requestContext["articleId"])[0]
						context["username"] = userName
					else:
						context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
						context["username"] = userName
						context["code"] = 403
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
		
	def addShortNewComment(self,requestContext):
		"""
		添加评论
		"""

		context = {}
		userName = requestContext.get("username",None)
		if not requestContext.get("message","").strip():
			context["code"] = 404
			return context
		try:
			newShortComment = ShortComment()
			if "parentId" in requestContext:
				if userName == None: 
					parentShortComment = ShortComment.objects.select_related("shortarticle").filter(shortarticle__userDetail__user__exact=self.user). \
					filter(shortarticle__id__exact=requestContext["shortarticleId"]).filter(id__exact=requestContext["parentId"])[0]
				else: 
					userDetail,access = self.blog_permission_required(userName)
					if access:
						parentShortComment = ShortComment.objects.select_related("shortarticle").filter(shortarticle__userDetail__exact=userDetail). \
						filter(shortarticle__id__exact=requestContext["shortarticleId"]).filter(id__exact=requestContext["parentId"])[0]
						context["username"] = userName						
					else:
						context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
						context["username"] = userName
						context["code"] = 403
						return context
				newShortComment.shortarticle = parentShortComment.shortarticle
				newShortComment.parent_comment = parentShortComment
				toUser = UserDetail.objects.get(username__exact=requestContext["toUser"]) #能否根据主键直接设置外键
				newShortComment.comment_to_user = toUser
			else: 
				if userName == None:
					shortArticle = ShortArticle.objects.filter(userDetail__user__exact=self.user).filter(id__exact=requestContext["shortarticleId"])[0]
				else:
					userDetail,access = self.blog_permission_required(userName)
					if access:
						shortArticle = ShortArticle.objects.filter(userDetail__exact=userDetail).filter(id__exact=requestContext["shortarticleId"])[0]
						context["username"] = userName
					else:
						context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
						context["username"] = userName
						context["code"] = 403
						return context
				newShortComment.shortarticle = shortArticle
			newShortComment.context = requestContext["message"]
			mUserDetail = UserDetail.objects.get(user__exact=self.user)
			newShortComment.comment_user = mUserDetail
			newShortComment.save()
			context["newId"] = newShortComment.id
			context["comment_time"] = newShortComment.comment_time.isoformat()
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
				updatenum = BlogText.objects.filter(userDetail__user=self.user).filter(id=requestContext["articleId"]). \
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
				mUserDetail = UserDetail.objects.get(user=self.user)
				article = BlogText()
				article.userDetail = mUserDetail
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
				Articles = BlogText.objects.select_related("userDetail").filter(userDetail__user=self.user).filter(article_tags__icontains=tag).filter(id__lt=startNum)[0:echpage]
				if len(Articles) == 0:
					userDetail = UserDetail.objects.get(user__exact=self.user)
				else:
					userDetail = Articles[0].userDetail
			else: 
				userDetail,access = self.blog_permission_required(username)
				if access:
					print "hahaha"
					Articles = BlogText.objects.filter(userDetail__exact=userDetail).filter(is_publish__exact=True).filter(article_tags__icontains=tag).filter(id__lt=startNum)[0:echpage]
					selfUserDetail = UserDetail.objects.get(user__exact=self.user)
					context["selfUserDetail"] = ModelToJson(selfUserDetail)
					context["username"] = username
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = username
					context["code"] = 403
					return context
			context["code"] = 200
			context["Articles"] = ModelToJson(Articles)
			context["userDetail"] = ModelToJson(userDetail)
		except:
			context["code"] = 500
			traceback.print_exc()

		return context


	def blog_permission_required(self,username):
		"""
		检查对某个账户blog的访问权限，如果没有会根据redirect_template返回对应页面,或者抛出PermissionDenied
		"""

		try:
			mUserDetail = UserDetail.objects.get(username=username)
			if mUserDetail.access_confirm:
				dbpermission = Friends.objects.get(ask_from_user__user=self.user,asked_user__exact=mUserDetail)
				if dbpermission.blog_priority:
					return mUserDetail,True
				else:
					return mUserDetail,False
			else:
				return mUserDetail,True
		except UserDetail.DoesNotExist:
			return None,False
		except Friends.DoesNotExist:
			return mUserDetail,False
		except Exception,e:
			traceback.print_exc()
			return mUserDetail,None
				
	def addNewShortArticle(self,requestContext):
		"""
		添加新的短博文
		"""
		context = {}
		try:
			if not requestContext.get("content","").strip():
				context["code"] = 404
				return context
			mUserDetail = UserDetail.objects.get(user=self.user)
			mShortArticle = ShortArticle()
			mShortArticle.userDetail = mUserDetail
			mShortArticle.context = requestContext["content"]
			mShortArticle.save()
			context["id"] = mShortArticle.id
			context["create_time"] = str(mShortArticle.create_time)
			context["userDetail"] = ModelToJson(mUserDetail)
		except KeyError:
			context["code"] = 400
		except:
			context["code"] = 500
		context["code"] = 200
		return  context
		
	def queryShortArticle(self,username=None,echpage=6,startNum=sys.maxint):
		"""
		查询所有的短博文
		"""	
		context = {}
		try:
			if username == None:
				shortArticles = ShortArticle.objects.select_related("userDetail").filter(userDetail__user=self.user).filter(id__lt=startNum)[0:echpage]
				print len(shortArticles)
				if len(shortArticles) == 0:
					mUserDetail = UserDetail.objects.get(user__exact=self.user)
				else:
					mUserDetail = shortArticles[0].userDetail
			else:
				mUserDetail,success = self.blog_permission_required(username)
				if success:
					selfUserDetail = UserDetail.objects.get(user__exact=self.user)
					shortArticles = ShortArticle.objects.filter(userDetail__exact=mUserDetail).filter(id__lt=startNum)[0:echpage]
					context["username"] = username
					context["selfUserDetail"] = ModelToJson(selfUserDetail)
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = username
					context["code"] = 403
					return context
			mshortArticles = list(shortArticles) 
			##必须要加，不然会报(1235, "This version of MySQL doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'")，
			#可能跟queryset的惰性有关，导致下一个查询出现了select * from a where a.b in (select b from c limit 10)，mysql认为这样的sql不合法。
			queryShortComments = ShortComment.objects.select_related("comment_user").filter(shortarticle__in=mshortArticles)
			context["shortArticles"] = []
			for shortArticle in shortArticles:
				parentCommentList = {}
				for comment in queryShortComments:
					if comment.shortarticle != shortArticle:
						continue
					if comment.parent_comment == None:
						parentCommentList[comment.id] = []
						newComment = {}
						newComment["comment"] = ModelToJson(comment)
						newComment["user"] = ModelToJson(comment.comment_user)
						parentCommentList[comment.id].append(newComment)
					else:
						newComment = {}
						newComment["comment"] = ModelToJson(comment)
						newComment["user"] = ModelToJson(comment.comment_user)
						parentCommentList[newComment["comment"]["parent_comment"]].append(newComment)
				newShortArticle = {}
				newShortArticle["shortArticle"] = ModelToJson(shortArticle)
				newShortArticle["comments"] = parentCommentList
				context["shortArticles"].append(newShortArticle)
			context["code"] = 200
			context["userDetail"] = ModelToJson(mUserDetail)
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
			traceback.print_exc()
			context["code"] = 500
		return context
	
	def uploadPhoto(self,requestContext):
		"""
		上传图片
		"""
		context = {}
		try:
			mUserDetail = UserDetail.objects.get(user=self.user)
			context["photos"] = []
			for upload in requestContext.FILES.values():
				file_suffix = upload.name.split(".")[-1]
				filename = str(int(time.time())) + "."+file_suffix
				upload_content = ContentFile(upload.read(),filename)
				mBlogPhoto = BlogPhoto()
				mBlogPhoto.userDetail = mUserDetail
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
				photos = BlogPhoto.objects.select_related("userDetail").filter(userDetail__user=self.user).filter(id__lt=startNum)[0:echpage]
				if len(photos) == 0:
					mUserDetail = UserDetail.objects.get(user__exact=self.user)
				else:
					mUserDetail = photos[0].userDetail
			else:
				mUserDetail,success = self.blog_permission_required(username)
				if success:
					photos = BlogPhoto.objects.filter(userDetail__exact=mUserDetail).filter(id__lt=startNum)[0:echpage]
					context["username"] = username
				else:
					context["denied"] = settings.NO_PERMISSON_TO_BLOG_TEMPLATE
					context["username"] = username
					context["code"] = 403
					return context
			context["code"] = 200
			context["photos"] = []
			context["userDetail"] = ModelToJson(mUserDetail)
			for photo in photos:
				newphoto = {}
				newphoto["id"] = photo.id
				newphoto["url"] = photo.getphotourl()
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
			context["userDetail"] = ModelToJson(mUserDetail)
			context["code"] = 200
		except:
			context["code"] = 500
		return context
