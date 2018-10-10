from .models import Employer, Tribal, User, Video
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

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

class EmpSignUpForm(UserCreationForm):
    tribals = forms.ModelMultipleChoiceField(
        queryset=Tribal.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_emp = True
        user.save()
        employer = Employer.objects.create(user=user)
        employer.tribals.add(*self.cleaned_data.get('tribals'))
        return user

class EmpVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file', 'title', 'jobtypes', 'city', 'state', 'remote', 'role', 'categories', 'tribals', 'experiences']

class JSVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file', 'title', 'jobtypes', 'categories', 'tribals']
