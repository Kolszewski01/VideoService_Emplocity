from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser


User = get_user_model()

class MyUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(MyUserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['avatar']

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ("email","avatar")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ("email",)