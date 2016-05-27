# encoding=utf8
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from blogdjango import models

def user_permisson_test(function=None, redirect_field_name=None,):
	def decorator(view_func):
		@wraps (view_func, assigned = available_attrs(view_func))
		def _wrapped_view(request,* args,** kwargs):
			if function(request.user,* args,** kwargs):
				return view_func(request, *args, **kwargs)
			elif redirect_field_name == None:
				raise PermissionDenied
			else:
				return HttpResponseRedirect(redirect_field_name)
		return _wrapped_view
	return decorator


def blog_permission_required(permission,redirect_field_name=None, raise_exception=False):
	"""
	检查对某个账户blog的访问权限，如果没有权限user_permisson_test会抛出PermissionDenied
	"""
	def check_perms(user,* args,** kwargs):
		if user.is_authenticated():
			dbpermission = user.blog_asked_permisson.get(ask_from_user__user__username==username).values("blog_priority")
			if dbpermission > permission:
				return True
			else:
				return False
		else:
			return False
	return user_permisson_test(check_perms, redirect_field_name=redirect_field_name)