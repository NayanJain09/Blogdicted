from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    # path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('postComment', views.postComment, name="postComment"),
    # path('myblogs', views.myblogs, name="myblogs"),
    path('create',views.create,name="create"),
    path('category/<str:field>',views.category,name='category'),
    path('edit/<str:slug>',views.editBlog,name='editBlog'),
    path('delete/<str:slug>',views.deleteBlog,name='deleteBlog'),
    path('<str:slug>/',views.blogPost,name='blogPost'),
    path('',views.blogHome,name='blogHome'),  
]