from django.urls import path
from . import views


app_name = 'user_management'
urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
]
