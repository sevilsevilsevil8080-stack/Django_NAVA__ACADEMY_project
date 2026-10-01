from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import StudentProfile


class StudentRegistrationForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        label=_('نام'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('نام خود را وارد کنید')
            }
        )
    )

    last_name = forms.CharField(
        max_length=150,
        label=_('نام خانوادگی'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('نام خانوادگی خود را وارد کنید')
            }
        )
    )

    email = forms.EmailField(
        label=_('ایمیل'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('example@email.com')
            }
        )
    )

    phone = forms.CharField(
        max_length=15,
        label=_('شماره موبایل'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('09123456789')
            }
        )
    )

    address = forms.CharField(
        label=_('آدرس'),
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _('آدرس خود را وارد کنید'),
                'rows': 3
            }
        )
    )

    password = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور')
            }
        )
    )

    password_confirm = forms.CharField(
        label=_('تکرار رمز عبور'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبور را دوباره وارد کنید')
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('این ایمیل قبلاً ثبت شده است.')
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    _('رمز عبور و تکرار آن یکسان نیستند.')
                )

        return cleaned_data