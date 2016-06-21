# encoding=utf8
from django.db import models
from django.contrib.auth.models import User
import json

class UserDetail(models.Model):
	user = models.OneToOneField(User)
	username = models.CharField(max_length=150,unique=True)
	nickname = models.CharField(max_length=200,default="",verbose_name=u"昵称")
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
	is_active = models.BooleanField(default=False,verbose_name=u"是否通过审核")
	need_confirm = models.BooleanField(default=True,verbose_name=u"需要审核")
	access_confirm = models.BooleanField(default=True,verbose_name=u"访问权限控制")
	friends = models.ManyToManyField("self",through="Friends",symmetrical=False,related_name="Permission")
	contact_user = models.ManyToManyField("self",through="Message",symmetrical=False,related_name="Contact")  ###对称关系的话，through表会怎么表示
	signature = models.CharField(max_length=400,default="",verbose_name=u"个性签名")
	head_photo = models.ImageField(upload_to="face/%Y/%m/%d",null=True)
	blog_title = models.CharField(max_length=200,default="",verbose_name=u"blog名称")
	
	def __unicode__(self):
		return self.user.username  
	def getheadphotourl(self):
		try:
			return "/" + self.head_photo.url
		except ValueError:
			return "/face/default.jpg"

	class Meta:
		db_table = "user_detail"
		verbose_name = "用户详细数据"
		ordering = ["create_time"]



class Friends(models.Model):
	blog_priority = models.BooleanField(default=False,verbose_name="权限")
	ask_from_user = models.ForeignKey(UserDetail,related_name="asking_user")
	asked_user = models.ForeignKey(UserDetail,related_name="asked_user")
	ask_time = models.DateTimeField(auto_now_add=True,verbose_name=u"请求好友时间")
	need_confirm = models.BooleanField(default=True,verbose_name=u"需要审核")


	class Meta:
		db_table = "blog_friends"
		verbose_name = "博客权限"
		ordering = ["ask_time"]
		

class BlogText(models.Model):
	id = models.AutoField(primary_key=True)
	userDetail = models.ForeignKey(UserDetail)
	article_tags = models.CharField(max_length=400,default="",verbose_name=u"blogText tag")
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"文档创建日期")
	context = models.TextField(verbose_name=u"blogText内容")
	blog_text_title = models.CharField(max_length=400,default="",verbose_name=u"blogText名称")
	is_publish = models.BooleanField(default=False,verbose_name=u"是否可以展示")

	def __unicode__(self):
		return self.blog_text_title  
	class Meta:
		db_table = "blog_text"
		verbose_name = "博客文档"
		ordering = ["-create_time"]

	def gettags(self):
		return self.article_tags.split(",")
		
class ShortArticle(models.Model):
	id = models.AutoField(primary_key=True)
	userDetail = models.ForeignKey(UserDetail)
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"文档创建日期")
	context = models.TextField(verbose_name=u"内容")
	short_text_title = models.CharField(max_length=400,default="",verbose_name=u"名称")
	def __unicode__(self):
		return self.short_text_title  
	class Meta:
		db_table = "short_article"
		verbose_name = "短博文"
		ordering = ["-create_time"]
		
class Comment(models.Model):
	id = models.AutoField(primary_key=True)
	blogtext = models.ForeignKey(BlogText)
	parent_comment = models.ForeignKey("self",blank=True,null=True,related_name="children_comments")
	context = models.TextField()
	comment_user = models.ForeignKey(UserDetail,blank=True,null=True,on_delete=models.SET_NULL,related_name="comment_from")
	comment_to_user = models.ForeignKey(UserDetail,blank=True,null=True,on_delete=models.SET_NULL,related_name="comment_to")
	comment_time = models.DateTimeField(auto_now_add=True,verbose_name=u"评论时间")

	class Meta:
		db_table = "blog_comment"
		verbose_name = "博客评论"
		ordering = ["comment_time"]
		
class ShortComment(models.Model):
	shortarticle = models.ForeignKey(ShortArticle)
	parent_comment = models.ForeignKey("self",blank=True,null=True,related_name="children_comments")
	context = models.TextField()
	comment_user = models.ForeignKey(UserDetail,blank=True,null=True,on_delete=models.SET_NULL)
	comment_time = models.DateTimeField(auto_now_add=True,verbose_name=u"评论时间")

	class Meta:
		db_table = "short_comment"
		verbose_name = "短博文评论"
		ordering = ["comment_time"]
		
class Message(models.Model):
	message = models.CharField(max_length=200,default="",verbose_name=u"聊天消息")
	contact_time = models.DateTimeField(auto_now_add=True,verbose_name=u"聊天时间")
	from_user = models.ForeignKey(UserDetail,related_name="sended_message")
	to_user = models.ForeignKey(UserDetail,related_name="recived_message")
	is_read = models.BooleanField(default=False,verbose_name=u"是否已读")
	
	class Meta:
		db_table = "blog_message"
		verbose_name = "聊天记录"
		ordering = ["-contact_time"]

class BlogPhoto(models.Model):
	id = models.AutoField(primary_key=True)
	userDetail = models.ForeignKey(UserDetail)
	upload_time = models.DateTimeField(auto_now_add=True,verbose_name=u"照片上传时间")
	photo = models.ImageField(upload_to="userphoto/%Y/%m/%d")

	def getphotourl(self):
		return "/" + self.photo.url
	class Meta:
		db_table = "blog_photo"
		verbose_name = "照片"
		ordering = ["-upload_time"]


		
