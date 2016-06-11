# encoding=utf8
from django.conf.urls import url,include
from django.contrib.auth.views import login,logout,password_change_done
from blogauth.views import userRegister,password_change

urlpatterns = [
    url(r'^login/$', login,{'template_name': 'registration/login.html'},name='login'),
    url(r'^logout/$', logout,{'template_name': 'registration/login.html'},name='logout'),
    url(r'^password_change/$', password_change,{'template_name': 'registration/password_change.html','post_change_redirect': '/accounts/login/'}, name='password_change'),  ##
    #不加{'post_change_redirect': 'done/'}会报NoReverseMatch Error（reverse(password_change_done)),原因未知
    url(r'^password_change/done/$', password_change_done, name='password_change_done'),
	url(r'^register/$',userRegister,name="userRegister"),
]
