from django.shortcuts import render
from blogauth.decorators import account_admin_required
from django.template.response import TemplateResponse
# Create your views here.

@account_admin_required()
def adminIndex(request):
	username = request.user.username.split('@')[0]
	return TemplateResponse(request,"admin/base.bak.html",{})