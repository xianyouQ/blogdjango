from django.shortcuts import render
from blogauth.decorators import account_admin_required
from django.http import HttpResponse
# Create your views here.

@account_admin_required()
def adminIndex(request):
	username = request.user.username.split('@')[0]
	return HttpResponse("Welcome," + username)