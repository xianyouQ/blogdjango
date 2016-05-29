# encoding=utf8
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect
from blogdjango import models
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url
from blog import settings


def user_permisson_test(test_func=None, Login_url=None,redirect_template=None,redirect_context={},redirect_field_name=REDIRECT_FIELD_NAME,):
	"""
	装饰器
	参考官方源码,只改了小部分(好吧,其实差不多根本没改,详见django.contrib.auth.decorators.user_passes_test)
	"""
	def decorator(view_func):
		@wraps (view_func, assigned = available_attrs(view_func))
		def _wrapped_view(request,*args,**kwargs):
			if not request.user.is_authenticated():
				path = request.build_absolute_uri()
				resolved_login_url = resolve_url(Login_url or settings.LOGIN_URL)
				login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
				current_scheme, current_netloc = urlparse(path)[:2]
				if ((not login_scheme or login_scheme == current_scheme) and (not login_netloc or login_netloc == current_netloc)):
					path = request.get_full_path()
				return redirect_to_login(path, resolved_login_url, redirect_field_name)
			if test_func(request.user,*args,**kwargs):
				return view_func(request, *args, **kwargs)
			elif redirect_template == None:
				raise PermissionDenied
			else:
				return TemplateResponse(request,redirect_template,redirect_context)
		return _wrapped_view
	return decorator


def blog_permission_required(permission,redirect_template=None):
	"""
	检查对某个账户blog的访问权限，如果没有登陆会要求登陆，如果没有权限会重定向到redirect_to 或者抛出PermissionDenied
	"""
	def check_perms(user,*args,**kwargs):
		dbpermission = user.blog_asked_permisson.get(ask_from_user__user__username__exact==username).values("blog_priority")
		if dbpermission > permission:
			return True
		else:
			return False
	return user_permisson_test(check_perms,  Login_url="/accounts/login/",redirect_template=redirect_template)
	
def account_active_required(redirect_template=None):
	"""
	检查账号是否激活，如果没有登陆会要求登陆，如果没有会重定向到redirect_to 或者抛出PermissionDenied
	"""
	def check_perms(user,*args,**kwargs):
		return user.userdetail.is_active

	return user_permisson_test(check_perms,Login_url="/accounts/login/",redirect_template=redirect_template)
	
	
def account_admin_required(redirect_template=None):
	"""
	检查账号是否有管理权限，如果没有登陆会要求登陆，如果没有权限会重定向到redirect_to 或者抛出PermissionDenied
	"""
	def check_perms(user,*args,**kwargs):
		return user.is_staff:
		
	return user_permisson_test(check_perms, Login_url="/accounts/login/",redirect_template=redirect_template)