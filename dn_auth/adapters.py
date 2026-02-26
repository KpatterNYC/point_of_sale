from django.http import HttpRequest
from django.shortcuts import resolve_url
from allauth.account.adapter import DefaultAccountAdapter


class CustomEmsAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, req:HttpRequest):
        if hasattr(req.user,"worker_profile"):
            url="dashboard"
        else:
            url="create_worker_profile"
                
        return resolve_url(url)

    
    def get_signup_redirect_url(self, req:HttpRequest):
        return resolve_url("homepage")

    def get_logout_redirect_url(self, req:HttpRequest):
        return resolve_url("/")
    