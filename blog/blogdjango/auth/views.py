# encoding=utf8
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from blogdjango.models import UserDetail,Blog
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.views import deprecate_current_app
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url
from django.utils.translation import ugettext as _
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
			user_detail.username = username=request.POST['username']
			user_detail.save()
			return HttpResponseRedirect("/blog/index/")
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


@sensitive_post_parameters()
@csrf_protect
@login_required
@deprecate_current_app
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
	"""
	与官方源码差不多，修改了错误信息的返回组织方式
	"""
	errors = []
	if post_change_redirect is None:
		post_change_redirect = reverse('password_change_done')
	else:
		post_change_redirect = resolve_url(post_change_redirect)
	if request.method == "POST":
		form = password_change_form(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return HttpResponseRedirect(post_change_redirect)
		else:
			for messagelist in json.loads(form.errors.as_json()).itervalues():
				for message in messagelist:
					errors.append(message["message"])
	else:
		form = password_change_form(user=request.user)
	context = {
		'form': form,
		'title': _('Password change'),
		'errors':errors
	}
	if extra_context is not None:
		context.update(extra_context)

	return TemplateResponse(request, template_name, context)