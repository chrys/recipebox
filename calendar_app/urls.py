from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('schedule-week/', views.schedule_current_week, name='schedule_current_week'),
    path('entry/<int:pk>/replace/', views.replace_calendar_recipe, name='replace_calendar_recipe'),
    path('admin/', views.admin_settings, name='admin_settings'),
    path('admin/category/add/', views.add_category, name='add_category'),
    path('admin/category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('admin/schedule/update/', views.update_schedule, name='update_schedule'),
    path('add/', views.calendar_add, name='calendar_add'),
    path('<int:pk>/delete/', views.calendar_delete, name='calendar_delete'),
]
