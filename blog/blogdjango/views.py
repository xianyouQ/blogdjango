from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blogauth.decorators import blog_permission_required
from blogauth.decorators import account_active_required
# Create your views here.

@account_active_required()
def index(request):
	username = request.user.username.split('@')[0]
	return HttpResponse(username)

@blog_permission_required(permission=1)
def userindex(request,username):
	askedusername = request.user.username.split('@')[0]
	return HttpResponse(askedusername + "asking for see " + username + "'s blog")

@blog_permission_required(permission=1)
def userartical(request,username,articalid):
	askedusername = request.user.username.split('@')[0]
	return HttpResponse(askedusername + "asking for see " + username + "'s blog")

@blog_permission_required(permission=1)
def usercomment(request,username,articalid):
	askedusername = request.user.username.split('@')[0]
	return HttpResponse(askedusername + "asking for see " + username + "'s blog")
