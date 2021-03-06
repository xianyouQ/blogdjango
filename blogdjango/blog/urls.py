from django.conf.urls import url,include
from blogdjango.blog import views
from django.contrib.auth.views import login
urlpatterns = [
	url(r'^friendDynamic/$',views.FriendDymic,name="FriendDymic"),
	url(r'^index/$',views.selfIndex,name="selfIndex"),
	url(r'^comment/$',views.Comment),
	url(r'^querycomment/$',views.userComment),
	url(r'^shortcomment/$',views.shortComment),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/$',views.userIndex),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/article/$',views.userActicle),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/shortArticle/$',views.userShortArticle),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/photo/$',views.userPhotoView),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/permission/',views.askPermission),
	url(r'^article/$',views.addNewActicle,name="addNewActicle"),
	url(r'^shortArticle/$',views.shortArticle,name="shortArticle"),
	url(r'^permission/$',views.processPermission,name="processPermission"),
	url(r'^permissioncontrol/$',views.processBlogPermission,name="processBlogPermission"),
	url(r'^userProfile/$',views.userProfile,name="userProfile"),
	url(r'^photo/$',views.photoView,name="photoView"),
	url(r'^uploadHeadPhoto/$',views.uploadHeadPhoto,name="uploadHeadPhoto"),
	url(r'^uploadArticlePhoto/$',views.uploadArticlePhoto,name="uploadArticlePhoto"),
	#url(r'^test/$',views.test),
]
