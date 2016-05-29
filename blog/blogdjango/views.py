from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blogauth.decorators import blog_permission_required
from blogauth.decorators import account_active_required
from blogdjango.models import UserDetail
from blogdjango import blogAction
from django.views.decorators.csrf import csrf_protect
# Create your views here.


@account_active_required()
def selfIndex(request):
	mblogAction = blogAction(request.user)
	context = mblogAction.queryArticles()
	return HttpResponse(username)

@blog_permission_required(permission=1)
def userIndex(request,username):
	mblogAction = blogAction(request.user)
	context = mblogAction.queryArticles(username)
	return HttpResponse(askedusername + "asking for see " + username + "'s blog")


@blog_permission_required(permission=1)
def userComment(request,username,articalid):
	mblogAction = blogAction(request.user)
	context = mblogAction.queryActicleComment(articalid,username)
	return HttpResponse(askedusername + "asking for see " + username + "'s blog")

@account_active_required()	
def askPermission(request,username):
	mblogAction = blogAction(request.user)
	context = mblogAction.askBlogPermission(username)
	return 

@account_active_required()
def getAskedPermission():
	mblogAction = blogAction(request.user)
	context = mblogAction.queryAskedPermission()
	return 

@csrf_protect
@account_active_required()
def processPermission():
	mblogAction = blogAction(request.user)
	context = mblogAction.processAskedPermission(request.POST) ##POST中的部分数据，后续要改
	return 

@csrf_protect
@account_active_required()
def addNewComment(username,acticleId):
	mblogAction = blogAction(request.user)
	context = mblogAction.processAskedPermission(username,acticleId,request.POST) ##参数要修正
	return 

@csrf_protect
@account_active_required()
def addNewActicle():
	mblogAction = blogAction(request.user)
	context = mblogAction.addNewActicle() #
	return 

@csrf_protect
@account_active_required()
def updateActicle():
	mblogAction = blogAction(request.user)
	context = mblogAction.updateActicle()
	return 
