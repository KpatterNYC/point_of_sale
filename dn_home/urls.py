from django.urls import path
from dn_home import views

urlpatterns = [
    path("",views.homePage,name="homepage"),
    path("dashboard",views.dashBoard,name="dashboard")
]
