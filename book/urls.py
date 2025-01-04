# urls.py
from django.urls import path
from . import views
from .views import UserRegistrationView, LoginView, LogoutView

urlpatterns = [
    path('stalls/', views.stall_details, name='stall_details'),
    path('get-stall-details/<int:stall_id>/', views.get_stall_details, name='get_stall_details'),
    path('', views.index, name='index'),
    path('shortest-path/', views.shortest_path_view, name='shortest_path'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),  # Custom LoginView
    path('logout/', LogoutView.as_view(), name='logout'), 
]
