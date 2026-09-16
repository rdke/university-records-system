from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('queries/', views.database_queries, name='database-queries'),
    path('<str:entity>/', views.entity_list, name='entity-list'),
    path('<str:entity>/new/', views.entity_create, name='entity-create'),
    path('<str:entity>/<int:pk>/edit/', views.entity_update, name='entity-update'),
    path('<str:entity>/<int:pk>/delete/', views.entity_delete, name='entity-delete'),
]