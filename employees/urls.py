from django.urls import path
from . import views
from .views import EmployeeListCreateAPI, EmployeeDetailAPI

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_add, name='employee_add'),
    path('update/<int:pk>/', views.employee_update, name='employee_update'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('api/', EmployeeListCreateAPI.as_view(), name='employee_api_list'),
    path('api/<int:pk>/', EmployeeDetailAPI.as_view(), name='employee_api_detail'),
]