# encoding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blogdjango.auth.decorators import account_active_required
from blogdjango.models import UserDetail
from blogdjango.blog.blogAction import BlogAction
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
import json

# Create your views here.



@account_active_required()
def selfIndex(request):
	mblogAction = BlogAction(request.user)
	context = mblogAction.queryIndexData()
	return TemplateResponse(request,"blog/index.html",context)

@account_active_required()
def userIndex(request,username):
	mblogAction = BlogAction(request.user)
	context = mblogAction.queryIndexData(username)
	if context.has_key("denied"):
		return TemplateResponse(request,context["denied"],context)
	return TemplateResponse(request,"blog/index.html",context)

@csrf_protect
@account_active_required()
def Comment(request):
	mblogAction = BlogAction(request.user)
	if request.method == 'GET':
		context = mblogAction.queryActicleComment(request.GET)
	else:
		context = mblogAction.addNewComment(request.POST)
	if context.has_key("denied"):
		return TemplateResponse(request,context["denied"],context)
	return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])

@account_active_required()	
def askPermission(request,username):
	mblogAction = BlogAction(request.user)
	context = mblogAction.askBlogPermission(username)
	return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])

@csrf_protect
@account_active_required()
def processPermission(request):
	mblogAction = BlogAction(request.user)
	if request.method == 'GET':
		context = mblogAction.queryAskedPermission()
	else:
		context = mblogAction.processAskedPermission(request.POST)
		return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
	return TemplateResponse(request,"blog/Permission.html",context,status = context["code"])

@csrf_protect
@account_active_required()
def addNewActicle(request):
	mblogAction = BlogAction(request.user)
	if request.method == 'POST':
		context = mblogAction.updateOrCreateArticle(request.POST)
		return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
	else:
		if "lastArticleId" in request.GET:
			context = mblogAction.queryArticle(tag=request.GET.get("tag-search",""),startNum=request.GET.get("lastArticleId"))
			return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
		context = mblogAction.queryArticle(tag=request.GET.get("tag-search",""))
		return TemplateResponse(request,"blog/ArticleEditor.html",context,status = context["code"])
		
@account_active_required()
def shortArticle(request):
	mblogAction = BlogAction(request.user)
	if request.method == 'POST':
		context = mblogAction.addNewShortArticle(request.POST)
		return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
	else:
		if "lastShortArticleId" in request.GET:
			context = mblogAction.queryShortArticle(startNum=request.GET.get("lastShortArticleId"))
			return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
		context = mblogAction.queryShortArticle()
		return TemplateResponse(request,"blog/shortArticleEditor.html",context,status = context["code"])
		
def test(request):
	return TemplateResponse(request,"blog/test.html")

@account_active_required()
def userProfile(request):
	mblogAction = BlogAction(request.user)
	if request.method == 'POST':
		context = mblogAction.uploadUserDetail(request.POST)
		return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
	else:
		context = mblogAction.queryUserDetail()
		return TemplateResponse(request,"blog/userProfile.html",context,status = context["code"])

@csrf_protect
@account_active_required()
def uploadHeadPhoto(request):
	if request.method == 'POST':
		mblogAction = BlogAction(request.user)
		context = mblogAction.uploadHeadPhoto(request.POST)
	else:
		context["code"] = 405
	return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])

@csrf_protect
@account_active_required()	
def photoView(request):
	mblogAction = BlogAction(request.user)
	if request.method == 'POST':
		context = mblogAction.uploadPhoto(request)
		return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
	else:
		if "lastPhotoId" in request.GET:
			context = mblogAction.requeryPhoto(startNum=request.GET.get("lastPhotoId"))
			return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"])
		context = mblogAction.requeryPhoto()
	return TemplateResponse(request,"blog/photo.html",context,status = context["code"])


@csrf_protect
@account_active_required()
def uploadArticlePhoto(request):
	if request.method == 'POST':
		mblogAction = BlogAction(request.user)
		context = mblogAction.uploadArticlePhoto(request)
	else:
		context["code"] = 405
	return HttpResponse(json.dumps(context),content_type="application/json",status = context["code"]) 