from django.shortcuts import render
from blogauth.decorators import account_admin_required
from django.template.response import TemplateResponse
from blogadmin.adminAction import adminAction
from django.http import HttpResponse
import json
# Create your views here.

@account_admin_required()
def adminIndex(request):
	username = request.user.username.split('@')[0]
	return TemplateResponse(request,"admin/base.html",{})
	
@account_admin_required()
def NewAccounts(request):
	mAdminAction = adminAction()
	if request.method == 'POST':
		context = mAdminAction.processConfirmAsk(request.POST)
		print context
		return HttpResponse(json.dumps(context),content_type="application/json")
	else:
		context = mAdminAction.queryNeedConfirmAccounts()
		return TemplateResponse(request,"admin/usermanage.html",context)
