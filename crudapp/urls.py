from django.urls import path
from . import views

urlpatterns = [    
    path('new/', views.new, name='new'),
    path('detail/<int:blog_id>', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('postcreate/', views.postcreate, name='postcreate'),
]