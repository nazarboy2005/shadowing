from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import AccountModel

UserModel = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, min_length=8)


class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=6)


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = AccountModel
        exclude = ('user',)



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = AccountModel
        fields = ['full_name', 'country', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'input-field w-full border border-gray-300 p-3 rounded-md',
                'placeholder': 'Enter your full name',
            }),
            'country': forms.TextInput(attrs={
                'class': 'input-field w-full border border-gray-300 p-3 rounded-md',
                'placeholder': 'Enter your country',
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'w-full text-gray-700',
            }),
        }
