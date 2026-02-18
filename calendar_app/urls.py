from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('add/', views.calendar_add, name='calendar_add'),
    path('<int:pk>/delete/', views.calendar_delete, name='calendar_delete'),
]
