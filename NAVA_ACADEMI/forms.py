from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label='نام',
        widget=forms.TextInput(attrs={
            'placeholder': 'نام خود را وارد کنید'
        })
    )

    last_name = forms.CharField(
        max_length=150,
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'placeholder': 'نام خانوادگی خود را وارد کنید'
        })
    )

    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@email.com'
        })
    )

    phone = forms.CharField(
        max_length=15,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'placeholder': '09123456789'
        })
    )

    address = forms.CharField(
        label='آدرس',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'آدرس خود را وارد کنید',
            'rows': 3
        })
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور'
        })
    )

    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور را دوباره وارد کنید'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'این ایمیل قبلاً ثبت شده است.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    'رمز عبور و تکرار آن یکسان نیستند.'
                )

        return cleaned_data