from django.conf.urls import url,include
from blogadmin.views import adminIndex


urlpatterns = [
	url(r'^index/',adminIndex),
]