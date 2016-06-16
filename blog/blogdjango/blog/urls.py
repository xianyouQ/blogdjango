from django.conf.urls import url,include
from blogdjango.blog import views
from django.contrib.auth.views import login
urlpatterns = [
	url(r'^index/$',views.selfIndex,name="selfIndex"),
	url(r'^test/$',views.test),
	url(r'^comment/$',views.Comment),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/$',views.userIndex),
	url(r'^user/(?P<username>[a-zA-Z0-9]+)/permission/',views.askPermission),
	url(r'^article/$',views.addNewActicle,name="addNewActicle"),
	url(r'^shortArticle/$',views.shortArticle,name="shortArticle"),
	url(r'^permission/$',views.processPermission,name="processPermission"),
	url(r'^userProfile/$',views.userProfile,name="userProfile"),
	url(r'^photo/$',views.photoView,name="photoView"),
	url(r'^uploadHeadPhoto/$',views.uploadHeadPhoto,name="uploadHeadPhoto"),
	url(r'^uploadArticlePhoto/$',views.uploadArticlePhoto,name="uploadArticlePhoto"),
]
