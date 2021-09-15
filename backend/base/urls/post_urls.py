from django.urls import path
from django.urls.resolvers import URLPattern
from ..views import post_views as views


urlpatterns=[
    path('',views.getPosts, name="posts"),
    path('create/', views.createPost, name="post-create"),
    path('upload/', views.uploadImage, name="imdage-upload"),
    path('myposts/', views.getMyPosts, name='myposts'),

    path('<str:pk>/reviews/', views.createPostReview, name='create-review'),
    path('top/', views.getTopPosts, name='top-posts'),
    path('<str:pk>/',views.getPost, name="post"),

    path('delete/<str:pk>/', views.deletePost, name="post-delete"),
    path('update/<str:pk>/', views.updatePost, name="post-update"),

]