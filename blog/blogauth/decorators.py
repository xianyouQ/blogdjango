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


def user_permisson_test(test_func=None, Login_url=None,redirect_to=None,redirect_field_name=REDIRECT_FIELD_NAME,):
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
			elif redirect_to == None:
				raise PermissionDenied
			else:
				return HttpResponseRedirect(redirect_to)
		return _wrapped_view
	return decorator


def blog_permission_required(permission,redirect_to=None):
	"""
	检查对某个账户blog的访问权限，如果没有权限会重定向redirect_field_name 或者抛出PermissionDenied
	"""
	def check_perms(user,*args,**kwargs):
		dbpermission = user.blog_asked_permisson.get(ask_from_user__user__username==username).values("blog_priority")
		if dbpermission > permission:
			return True
		else:
			return False
	return user_permisson_test(check_perms,  Login_url="/accounts/login/",redirect_to=redirect_to)
	
def account_active_required(redirect_to=None):
	"""
	检查账号是否激活，如果没有会重定向redirect_field_name 或者抛出PermissionDenied
	"""
	def check_perms(user,*args,**kwargs):
		active = user.userdetail.is_active ##写法应该有误
		if active == True:
			return True
		else:
			return False
	return user_permisson_test(check_perms,Login_url="/accounts/login/",redirect_to=redirect_to)
	
	
def account_admin_required(redirect_to=None):
	"""
	检查账号是否有管理权限，如果没有权限会重定向redirect_field_name 或者抛出PermissionDenied
	"""
	def check_perms(user,*args,**kwargs):
		if user.is_staff:
			return True
		else:
			return False
	return user_permisson_test(check_perms, Login_url="/accounts/login/",redirect_to=redirect_to)