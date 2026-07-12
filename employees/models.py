from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name
