from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from employees.models import Employee
from leaves.models import Leave


@login_required
def dashboard_view(request):
    total_employees = Employee.objects.count()
    total_leaves = Leave.objects.count()
    pending_count = Leave.objects.filter(status='Pending').count()
    approved_count = Leave.objects.filter(status='Approved').count()
    rejected_count = Leave.objects.filter(status='Rejected').count()

    # Department-wise employee count
    dept_employee_data = Employee.objects.values('department').annotate(count=Count('id')).order_by('-count')

    # Department-wise leave count
    dept_leave_data = Leave.objects.values('employee__department').annotate(count=Count('id')).order_by('-count')

    context = {
        'total_employees': total_employees,
        'total_leaves': total_leaves,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'dept_labels': [d['department'] for d in dept_employee_data],
        'dept_emp_counts': [d['count'] for d in dept_employee_data],
        'dept_leave_labels': [d['employee__department'] or 'N/A' for d in dept_leave_data],
        'dept_leave_counts': [d['count'] for d in dept_leave_data],
    }
    return render(request, 'dashboard/dashboard.html', context)