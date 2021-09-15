from django.urls import path
from django.urls.resolvers import URLPattern
from ..views import apply_views as views


urlpatterns=[
    path('', views.getApplies, name='applies'),

    path('add/', views.addApplyItems, name='applies-add'),
    path('myapplies/', views.getMyApplies, name='myapplies'),
    path('myapplies2/', views.getPostApplies, name='myapplies2'),


    path('<str:pk>/', views.getApplyById, name='user-apply'),
    
    path('<str:pk>/pay/', views.updateApplyToPaid, name='pay'),
    path('<str:pk>/notdeliver/', views.updateApplyToNotDelivered, name='order-notdelivered'),

    path('<str:pk>/deliver/', views.updateApplyToDelivered, name='order-delivered'),

]
