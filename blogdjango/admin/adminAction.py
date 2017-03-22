# encoding=utf8
from django.contrib.auth.models import User
import traceback
import json

class adminAction:
	"""
	后台操作管理类
	"""
	def __init__(self):
		pass

	def queryNeedConfirmAccounts(self):
		"""
		查询当前需要审核的帐号
		"""
		context = {}
		try:
			queryaccounts = User.objects.filter(is_active=False)
		except Exception:
			context["code"] = 500
			return context
		context["code"] = 200
		context["accounts"] = queryaccounts
		return context

	def processConfirmAsk(self,requestContext):
		"""
		处理审核请求
		"""
		context = {}
		for is_active,usernameStr in requestContext.items():
			usernameList = usernameStr.split(",")
			try:
				changenum = User.objects.filter(username__in=usernameList).update(is_active=is_active)
				context[is_active]=changenum
			except Exception:
				context[is_active] = 0
		return context