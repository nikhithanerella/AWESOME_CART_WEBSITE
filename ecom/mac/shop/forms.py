# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Ensure passwords match
        if password != confirm_password:
            return "confirm password not matched"

        # Ensure email is unique
        if User.objects.filter(email=cleaned_data['email']).exists():
            print("A user with that email already exists.")
        
        return cleaned_data
