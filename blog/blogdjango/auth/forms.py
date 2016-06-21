#encoding=utf8
from django.contrib.auth.forms import AuthenticationForm

class MyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass