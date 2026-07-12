from django.urls import path
from . import views
from .views import LeaveListCreateAPI, LeaveDetailAPI

urlpatterns = [
    path('', views.leave_list, name='leave_list'),
    path('add/', views.leave_add, name='leave_add'),
    path('update/<int:pk>/', views.leave_update, name='leave_update'),
    path('delete/<int:pk>/', views.leave_delete, name='leave_delete'),
    path('api/', LeaveListCreateAPI.as_view(), name='leave_api_list'),
    path('api/<int:pk>/', LeaveDetailAPI.as_view(), name='leave_api_detail'),
]