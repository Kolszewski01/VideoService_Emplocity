from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MyUser
from frameApp.models import Frame, UserFrame


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

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            if avatar.name.endswith('.gif'):
                raise ValidationError("Nie możesz ustwaić gifu na avatar. Możesz jedynie kupić ;)")
        return avatar


class SelectAvatarForm(forms.Form):
    frame = forms.ModelChoiceField(queryset=Frame.objects.none(), label="Wybierz zakupiony awatar")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['frame'].queryset = Frame.objects.filter(userframe__user=user)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ("email","avatar")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ("email",)