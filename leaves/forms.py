from django import forms
from .models import Leave

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'from_date', 'to_date', 'reason', 'status']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError("From Date must not be greater than To Date.")
        return cleaned_data