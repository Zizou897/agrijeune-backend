from django.urls import path, include

from .views import (
    SignUpView,
    LoginView,
    LoginVendorView,
    LogoutView
)


urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login-client', LoginView.as_view(), name='loginClient'),
    path('login-vendor', LoginVendorView.as_view(), name='loginVendor'),
    path('logout', LogoutView.as_view(), name='logout'),
]
