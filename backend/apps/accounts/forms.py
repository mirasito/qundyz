from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        }
        labels = {
            'username': 'Логин',
            'email': 'E-mail',
            'password': 'Пароль'
        }

    def clean_password2(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Пароли не совпадают.")
        return pwd2

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        validate_password(pwd)
        return pwd

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_pwd = self.cleaned_data['password']
        user.set_password(raw_pwd)
        if commit:
            user.save()
        return user