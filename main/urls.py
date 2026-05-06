from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/<slug:slug>/', views.category_gallery, name='category_gallery'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('like/<int:id>/', views.like_blog, name='like_blog'),
]