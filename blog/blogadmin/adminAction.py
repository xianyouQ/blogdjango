# encoding=utf8
from blogdjango.models import UserDetail
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
			queryaccounts = UserDetail.objects.select_related("user").filter(need_confirm__exact=True)
		except Exception:
			context["error"] = "Internal Server Error"
			return context
		accounts = []
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
				changenum = UserDetail.objects.filter(user__username__in=usernameList).update(is_active=is_active,need_confirm=False)
				context[is_active]=changenum
			except Exception:
				traceback.print_exc()
				context[is_active] = 0
		return context