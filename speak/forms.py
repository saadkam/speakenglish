
from django.contrib.auth.models import User
from django import forms

from speak.models import Question


class NewUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'username': forms.TextInput(attrs={'class': 'input'}),
                   'email': forms.TextInput(attrs={'class': 'input'}),
                   }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ('username', 'password', )
        widgets = {'username': forms.TextInput(attrs={'class': 'input'}),}
        label = {'username': 'user', 'password': 'pass'}





