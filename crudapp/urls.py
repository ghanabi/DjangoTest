from django.urls import path
from . import views

urlpatterns = [    
    path('new/', views.new, name='new'),
    path('detail/<int:blog_id>', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('postcreate/', views.postcreate, name='postcreate'),
    path('update/<int:blog_id>/', views.update, name='update'),
    path('delete/<int:blog_id>/', views.delete, name='delete'),
    path('search', views.search, name='search'),
    path('some_view', views.some_view, name='some_view'),    
    path('test', views.test, name='test'),
    path('test2', views.test2, name='test2'),
]
