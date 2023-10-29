from django.forms import ModelForm, Textarea, TextInput, ValidationError, CharField
from report.models import Report
from booksdatabase.models import Book

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['book_title', 'comment']
    
    # Untuk Book Title
    book_title = CharField(
        widget=TextInput(attrs={'placeholder': 'Type Book\'s Title here'}),
        required= True
    )
    # Untuk comment pengguna
    comment = CharField(
        widget=Textarea(attrs={'placeholder': 'Type your comment here'}),
        required= True
    )

    def clean(self):
        cleaned_data = super().clean()
        book = Book.objects.get(title=cleaned_data.get('book_title'))
        comment = cleaned_data.get('comment')

        # Add custom validation for book and comment
        if not book or not comment:
            raise ValidationError("Both book and comment are required.")
