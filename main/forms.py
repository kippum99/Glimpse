from django.contrib.auth.models import User
from .models import Video
from django import forms
from django.contrib.auth.forms import UserCreationForm

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'group']

class JSSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_js = True
        if commit:
            user.save()
        return user

class EmpSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file', 'title', 'jobtypes', 'city', 'state', 'remote', 'role', 'categories', 'tribals']
