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
    path("dns_tools",views.dns_tools, name="dns_tools"),
    path("security_tools",views.security_tools, name="security_tools"),
    path("certificate_info",views.certificate_info, name="certificate_info"),
    path("subdomain_info",views.subdomain_info, name="subdomain_info"),
    path("landing", views.landing, name="landing"),
]
