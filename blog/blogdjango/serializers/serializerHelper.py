# encoding=utf8
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from blogdjango.models import BlogText,UserDetail,Comment,ShortComment
import json

def ModelToJson(obj):
	"""
	模型转成json
	"""
	if isinstance(obj,QuerySet) or isinstance(obj,list):
		result = []
		for item in obj:
			itemjsonsource = json.loads(serialize('json',[item])[1:-1])
			itemjson = itemjsonsource["fields"]
			itemjson["id"] = itemjsonsource["pk"]
			if isinstance(item,BlogText):
				itemjson["gettags"] = item.gettags()
			if isinstance(item,UserDetail):
				itemjson["head_photo"] = item.getheadphotourl()
			result.append(itemjson)
		return result
	else:
		itemjsonsource = json.loads(serialize('json',[obj])[1:-1])
		itemjson = itemjsonsource["fields"]
		itemjson["id"] = itemjsonsource["pk"]
		if isinstance(obj,BlogText):
			itemjson["gettags"] = obj.gettags()
		if isinstance(obj,UserDetail):
			itemjson["head_photo"] = obj.getheadphotourl()
		return itemjson
		