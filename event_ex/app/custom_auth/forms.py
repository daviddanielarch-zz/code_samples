from contextlib import suppress

from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Passwords dont match")

        with suppress(User.DoesNotExist):
            User.objects.get(email=cleaned_data['email'])
            raise forms.ValidationError("User already exists")

