from django.conf.urls import url,include
from blogdjango import views

urlpatterns = [
	url(r'^index/$',views.selfIndex,name="selfIndex"),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/$',views.userIndex),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/(?P<articalid>[0-9]+)/refreshcomment/',views.userComment),
	url(r'^newarticle/$',views.requestEdit),
	url(r'^postarticle/$',views.addNewActicle,name="addNewActicle"),
	url(r'permission/$',views.getAskedPermission,name="getAskedPermission")
]
