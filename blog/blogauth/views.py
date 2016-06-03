# encoding=utf8
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from blogdjango.models import UserDetail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import json

# Create your views here.

@csrf_protect
def userRegister(request):
	"""
	用户注册
	"""
	errors = []
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(username=request.POST['username'], password=request.POST['password1'])
			login(request, user)
			user_detail = UserDetail()
			user_detail.user = user
			user_detail.save()
			return TemplateResponse(request,'registration/register_done.html',{"username":user.username,"title":"Register Success"})
		else:
			for messagelist in json.loads(form.errors.as_json()).itervalues():
				for message in messagelist:
					errors.append(message["message"])
	else:
		form = UserCreationForm()
	context = {'form': form,"errors":errors}			
	return TemplateResponse(request,'registration/register_form.html',context)
	#return render_to_response('registration/register_form.html',context,context_instance=RequestContext(request))
	##如果使用render_to_response，就必须要加上context_instance=RequestContext(request)，跟csrf相关，具体原因还不了解
