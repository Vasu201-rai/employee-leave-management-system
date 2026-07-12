from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'email', 'department', 'mobile_number', 'date_of_joining']
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }