from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'username', 'password','img')
        widgets = {'img': forms.HiddenInput()}

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["img"])
        print(self.cleaned_data)
        if commit:
            user.save()
        return user