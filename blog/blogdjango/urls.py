from django.conf.urls import url,include
from blogdjango import views

urlpatterns = [
	url(r'^index/',views.index,name="index"),
	url(r'^user/(?P<username>[0-9]+)/',views.userindex),
	url(r'^user/(?P<username>[0-9]+)/(?P<articalid>[0-9]+)/refreshcomment/',views.usercomment),
]
