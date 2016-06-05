# encoding=utf8
from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
	user = models.OneToOneField(User)
	nickname = models.CharField(max_length=200,default="",verbose_name=u"昵称")
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
	is_active = models.BooleanField(default=False,verbose_name=u"是否通过审核")
	need_confirm = models.BooleanField(default=True,verbose_name=u"需要审核")
	askuser = models.ManyToManyField("self",through="BlogPermisson",symmetrical=False,related_name="Permission")
	contact_user = models.ManyToManyField("self",through="Message",symmetrical=False,related_name="Contact")  ###对称关系的话，through表会怎么表示
	signature = models.CharField(max_length=400,default="",verbose_name=u"个性签名")
	
	def __unicode__(self):
		return self.user.username  

	class Meta:
		db_table = "user_detail"
		verbose_name = "用户详细数据"
		ordering = ["create_time"]

class Blog(models.Model):
	userDetail = models.OneToOneField(UserDetail)
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
	blog_title = models.CharField(max_length=200,default="",verbose_name=u"blog名称")

	def __unicode__(self):
		return self.blog_title  

	class Meta:
		db_table = "blog"
		verbose_name = "博客"
		ordering = ["create_time"]

class BlogPermisson(models.Model):
	priority_level = (
        (0, '无读权限'),
        (1, '可读'),
        (2, '可评论')
	)
	blog_priority = models.SmallIntegerField(choices=priority_level,default=0,verbose_name="权限")
	ask_from_user = models.ForeignKey(UserDetail,related_name="blog_permissons")
	asked_user = models.ForeignKey(UserDetail,related_name="blog_asked_permisson")
	ask_time = models.DateTimeField(auto_now_add=True,verbose_name=u"请求权限时间")
	need_confirm = models.BooleanField(default=True,verbose_name=u"需要审核")

	def __unicode__(self):
		return self.ask_from_user.user.username + "'s priority for " + self.asked_user.user.username ##可以这么写?
	class Meta:
		db_table = "blog_permisson"
		verbose_name = "博客权限"
		ordering = ["ask_time"]
		

class BlogText(models.Model):
	id = models.AutoField(primary_key=True)
	blog = models.ForeignKey(Blog) ##考虑是否删除
	article_type = models.CharField(max_length=400,default="",verbose_name=u"blogText tag")
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"文档创建日期")
	context = models.TextField(verbose_name=u"blogText内容")
	blog_text_title = models.CharField(max_length=400,default="",verbose_name=u"blogText名称")
	is_publish = models.BooleanField(default=False,verbose_name=u"是否可以展示")

	def __unicode__(self):
		return self.blog_text_title  
	class Meta:
		db_table = "blog_text"
		verbose_name = "博客文档"
		ordering = ["create_time"]
		
class ShortArticle(models.Model):
	id = models.AutoField(primary_key=True)
	blog = models.ForeignKey(Blog)
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"文档创建日期")
	context = models.TextField(verbose_name=u"内容")
	short_text_title = models.CharField(max_length=400,default="",verbose_name=u"名称")
	def __unicode__(self):
		return self.short_text_title  
	class Meta:
		db_table = "short_article"
		verbose_name = "短博文"
		ordering = ["create_time"]
		
class Comment(models.Model):
	blogtext = models.ForeignKey(BlogText)
	parent_comment = models.ForeignKey("self",blank=True,null=True,related_name="children_comments")
	context = models.TextField()
	comment_user = models.ForeignKey(UserDetail,blank=True,null=True,on_delete=models.SET_NULL)
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
		ordering = ["contact_time"]
	
		
