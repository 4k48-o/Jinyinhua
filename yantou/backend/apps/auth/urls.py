"""
认证路由配置
"""
from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('captcha/', views.CaptchaView.as_view(), name='captcha'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

