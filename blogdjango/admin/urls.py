from django.conf.urls import url,include
from blogdjango.admin.views import adminIndex,NewAccounts


urlpatterns = [
	url(r'^index/',adminIndex),
	url(r'^users/',NewAccounts,name="NewAccounts"),
]