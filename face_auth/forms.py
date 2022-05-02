from django import forms
from .models import User
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'username', 'password','img')
        widgets = {'img': forms.HiddenInput()}

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # print(self.cleaned_data)
        img_data = self.cleaned_data['img']

        format, imgstr = img_data.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr), name=f'{user.username}.' + ext)
        user.face_image = data
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20)
    password = forms.CharField(label="Password",strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),)
