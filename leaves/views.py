from django.shortcuts import render, redirect, get_object_or_404
from .models import Leave
from .forms import LeaveForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from employees.models import Employee
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import LeaveSerializer


@login_required
def leave_list(request):
    if not request.user.is_staff:
        # Normal user - sirf apni leaves
        leaves = Leave.objects.filter(employee__user=request.user)
    else:
        status_filter = request.GET.get('status', '')
        type_filter = request.GET.get('leave_type', '')
        leaves = Leave.objects.all()
        if status_filter:
            leaves = leaves.filter(status=status_filter)
        if type_filter:
            leaves = leaves.filter(leave_type=type_filter)

    paginator = Paginator(leaves, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'leaves/leave_list.html', {
        'leaves': page_obj,
        'status_filter': request.GET.get('status', ''),
        'type_filter': request.GET.get('leave_type', ''),
    })

@login_required
def leave_add(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            if not request.user.is_staff:
                leave.employee = Employee.objects.get(user=request.user)
            leave.save()
            return redirect('leave_list')
    else:
        form = LeaveForm()
        if not request.user.is_staff:
            form.fields.pop('employee')  # dropdown hata do normal user ke liye
    return render(request, 'leaves/leave_form.html', {'form': form})


@login_required
def leave_update(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_list')
    else:
        form = LeaveForm(instance=leave)
    return render(request, 'leaves/leave_form.html', {'form': form})


@login_required
def leave_delete(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == 'POST':
        leave.delete()
        return redirect('leave_list')
    return render(request, 'leaves/leave_confirm_delete.html', {'leave': leave})


class LeaveListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaves = Leave.objects.all()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Leave, pk=pk)

    def get(self, request, pk):
        leave = self.get_object(pk)
        serializer = LeaveSerializer(leave)
        return Response(serializer.data)

    def put(self, request, pk):
        leave = self.get_object(pk)
        serializer = LeaveSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leave = self.get_object(pk)
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)