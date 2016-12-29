# encoding=utf8
from django.conf.urls import url,include
from django.contrib.auth.views import login,logout
from blogdjango.auth.views import userRegister,password_change
from blogdjango.auth.forms import MyAuthenticationForm

urlpatterns = [
    url(r'^login/$', login,{'template_name': 'registration/login.html','authentication_form':MyAuthenticationForm},name='login'),
    url(r'^logout/$', logout,{'template_name': 'registration/login.html'},name='logout'),
    url(r'^password_change/$', password_change,{'template_name': 'registration/password_change.html','post_change_redirect': '/accounts/login/'}, name='password_change'),  ##
    #不加{'post_change_redirect': 'done/'}会报NoReverseMatch Error（reverse(password_change_done)),原因未知
	url(r'^register/$',userRegister,name="userRegister"),
]
