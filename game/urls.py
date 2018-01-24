from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:situation_id>/', views.detail, name='detail'),
    path('<int:situation_id>/choose/', views.choose, name='choose'),
]
