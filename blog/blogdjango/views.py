# encoding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blogauth.decorators import account_active_required
from blogdjango.models import UserDetail
from blogdjango.blogAction import BlogAction
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
import json
# Create your views here.


def welcome(request):
	return TemplateResponse(request,"blog/welcome.html",{})

@account_active_required()
def selfIndex(request):
	mblogAction = BlogAction(request.user)
	context = mblogAction.queryArticles()
	return TemplateResponse(request,"blog/index.html",context)

@account_active_required()
def userIndex(request,username):
	mblogAction = BlogAction(request.user)
	context = mblogAction.queryArticles(username)
	if context.has_key("denied"):
		return TemplateResponse(request,context["denied"],context)
	return TemplateResponse(request,"blog/index.html",context)


@account_active_required()
def userComment(request,username,articalid):
	mblogAction = BlogAction(request.user)
	context = mblogAction.queryActicleComment(articalid,username)
	return HttpResponse(json.dumps(context),content_type="application/json")

@account_active_required()	
def askPermission(request,username):
	mblogAction = BlogAction(request.user)
	context = mblogAction.askBlogPermission(username)
	return HttpResponse(json.dumps(context),content_type="application/json")

@account_active_required()
def getAskedPermission(request):
	mblogAction = BlogAction(request.user)
	context = mblogAction.queryAskedPermission()
	return HttpResponse(request,"",context)

@csrf_protect
@account_active_required()
def processPermission(request):
	mblogAction = BlogAction(request.user)
	context = mblogAction.processAskedPermission(request.POST) ##POST中的部分数据，后续要改
	return HttpResponse(json.dumps(context),content_type="application/json")

@csrf_protect
@account_active_required()
def addNewComment(request,username,acticleId):
	mblogAction = BlogAction(request.user)
	context = mblogAction.processAskedPermission(username,acticleId,request.POST) ##参数要修正
	return HttpResponse(json.dumps(context),content_type="application/json")

@csrf_protect
@account_active_required()
def addNewActicle(request):
	if request.method == 'POST':
		mblogAction = BlogAction(request.user)
		return_code = 200
		if "articleId" in request.POST:
			context = mblogAction.updateActicle(request.POST["title"],request.POST["articleId"],request.POST["message"],True)
		else:
			context = mblogAction.addNewActicle(request.POST["title"],request.POST["message"],True)
		if "update" in context and context["update"] == 0:
			return_code = 404
		if "error" in context:
			return_code = 500
		return HttpResponse(json.dumps(context),content_type="application/json",status=return_code)
	else:
		return TemplateResponse(request,"blog/ArticleEdit.html",{})

