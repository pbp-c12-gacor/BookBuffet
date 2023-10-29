from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    referral_code = forms.CharField(max_length=20, required=False)
    isAdmin = forms.ChoiceField(choices=[(True,"Admin"), (False, "User")], label="Admin/User")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'isAdmin', 'referral_code')

    def clean(self):
        cleaned_data = super().clean()
        is_admin = cleaned_data.get('isAdmin')
        referral_code = cleaned_data.get('referral_code')
        
        if (is_admin == "Admin" and referral_code != "PBPC12GACORMAXWIN"):
            raise forms.ValidationError("Invalid referral code for Admin registration.")
        return cleaned_data