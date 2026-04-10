from django import forms
from .models import Event, Category
from django.utils import timezone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'venue', 'banner', 'date', 'time',
                  'total_seats', 'ticket_price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("Event date cannot be in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total_seats')
        if total is not None and total <= 0:
            self.add_error('total_seats', 'Total seats must be greater than 0.')
        return cleaned_data
