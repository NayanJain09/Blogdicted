from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('postComment', views.postComment, name="postComment"),
    path('create',views.create,name="create"),
    path('category/<str:field>',views.category,name='category'),
    path('edit/<str:slug>',views.editBlog,name='editBlog'),
    path('delete/<str:slug>',views.deleteBlog,name='deleteBlog'),
    path('<str:slug>/',views.blogPost,name='blogPost'),
    path('',views.blogHome,name='blogHome'),  
]