from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'email', 'department', 'mobile_number', 'date_of_joining')
    search_fields = ('name', 'employee_id')