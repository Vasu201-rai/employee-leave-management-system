from django.shortcuts import render
from employees.models import Employee
from leaves.models import Leave
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    total_employees = Employee.objects.count()
    total_leaves = Leave.objects.count()
    pending_count = Leave.objects.filter(status='Pending').count()
    approved_count = Leave.objects.filter(status='Approved').count()
    rejected_count = Leave.objects.filter(status='Rejected').count()

    context = {
        'total_employees': total_employees,
        'total_leaves': total_leaves,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'dashboard/dashboard.html', context)