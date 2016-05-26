# encoding=utf8
from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
	user = models.OneToOneField(User)
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
	is_active = models.BooleanField(default=False,verbose_name=u"是否通过审核")
	need_confirm = models.BooleanField(default=True,verbose_name=u"需要审核")
	askuser = models.ManyToManyField("self",through="BlogPermisson",symmetrical=False)

    def __unicode__(self):
        return self.user.username  

    class Meta:
        db_table = "user_detail"
        verbose_name = "用户详细数据"
        ordering = ["create_time"]

class Blog(models.Model):
	userDetail = models.OneToOneField(UserDetail)
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"创建时间")
	blog_title = models.CharFeild(max_length=200,default="",verbose_name=u"blog名称")

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
	ask_from_user = models.ForeignKey(UserDetail)
	asked_user = models.ForeignKey(UserDetail)
	ask_time = models.DateTimeField(auto_now_add=True,verbose_name=u"请求权限时间")
	need_confirm = models.BooleanField(default=True,verbose_name=u"需要审核")

	def __unicode__(self):
        return self.ask_from_user.user.username + "'s priority for " + self.asked_user.user.username ##可以这么写?
    class Meta:
        db_table = "blog_permisson"
        verbose_name = "博客权限"
        ordering = ["ask_time"]

class BlogText(models.Model):
	blog = models.ForeignKey(Blog)
	create_time = models.DateTimeField(auto_now_add=True,verbose_name=u"文档创建日期")
	context = models.TextField(verbose_name=u"blogText内容")
	blog_text_title = models.CharFeild(max_length=400,default="",verbose_name=u"blogText名称")

	def __unicode__(self):
        return self.blog_text_title  
    class Meta:
        db_table = "blog_text"
        verbose_name = "博客文档"
        ordering = ["create_time"]

class Comment(models.Model):
	blogtext = models.ForeignKey(BlogText)
	parent_comment = ForeignKey("self",blank=True,null=True,related_name="children_comments")
	context = models.TextField()
	comment_user = models.ForeignKey(UserDetail,blank=True,null=True,on_delete=models.SET_NULL)
	comment_time = models.DateTimeField(auto_now_add=True,verbose_name=u"评论时间")

	class Meta:
		db_table = "comment"
		verbose_name = "博客评论"
		ordering = ["comment_time"]