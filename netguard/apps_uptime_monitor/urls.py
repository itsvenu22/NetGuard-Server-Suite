from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup",views.signup, name="signup" ),
    path("otp",views.otp, name="otp" ),
    path("forgot",views.forgot, name="forgot" ),
    path("forgot_otp",views.forgot_otp, name="forgot_otp"),
    path("ip_tools",views.ip_tools, name="ip_tools"),
    path("landing", views.landing, name="landing"),
]
