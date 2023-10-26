from django.forms import ModelForm, TextInput, Textarea
from report.models import Report

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['book', 'comment']
        widgets = {
            'book': TextInput(attrs={'id': 'book_title'}),
            'comment': Textarea(attrs={'placeholder': 'Enter comment'}),
        }