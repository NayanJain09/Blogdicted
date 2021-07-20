from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [
    path('contact',views.contact,name='contact'), 
    path('search/', views.search, name="search"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('<str:name>/',views.profile,name='profile'),
    path('',views.home,name='home'),  
]