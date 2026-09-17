from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('queries/', views.database_queries, name='database-queries'),
]