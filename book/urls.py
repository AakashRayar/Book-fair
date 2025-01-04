# urls.py
from django.urls import path
from . import views
from dj_rest_auth.views import LoginView, LogoutView
from .views import UserRegistrationView, LoginView, LogoutView, ForgetPasswordRequestView, ResetPasswordView

urlpatterns = [
    path('stalls/', views.stall_details, name='stall_details'),
    path('get-stall-details/<int:stall_id>/', views.get_stall_details, name='get_stall_details'),
    path('', views.index, name='index'),
    path('shortest-path/', views.shortest_path_view, name='shortest_path'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),  # Custom LoginView
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forget-password/', ForgetPasswordRequestView.as_view(), name='forget-password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]
