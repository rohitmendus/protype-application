from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
	password1 = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'id': 'password1'}),
    )
	password2 = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'id': 'password2'}),
    )
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'email')
		labels = {
			'username': '',
			'password1': '',
			'password2': '',
			'email': ''
		}
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control', 'id':'username'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'id':'email'})
		}

class UpdateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email')
		labels = {
			'username': '',
			'email': ''
		}
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control', 'id':'username-edit'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'id':'email-edit'})
		}

class ProfileForm(forms.ModelForm):
	class Meta:
		model = ProfileUser
		fields = ('name', 'mobile', 'age', 'sex', 'salutation', 'health', 'department')
		labels = {
			'name': '',
			'mobile': '',
			'age': '',
			'sex': '',
			'salutation': '',
			'health': '',
			'department': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'id':'name'}),
			'mobile': forms.TextInput(attrs={'class': 'form-control', 'id':'mobile'}),
			'age': forms.NumberInput(attrs={'class': 'form-control', 'id':'age'}),
			'sex': forms.Select(attrs={'class': 'form-select', 'id':'sex'}),
			'salutation': forms.Select(attrs={'class': 'form-select', 'id':'salutation'}),
			'health': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id':'health'}),
			'department': forms.Select(attrs={'class': 'form-select', 'id':'dept'}),
		}


class ProgrammeForm(forms.ModelForm):
	class Meta:
		model = Programme
		fields = ('name', 'description', 'department')
		labels = {
			'name': '',
			'description': '',
			'department': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'id':'name'}),
			'description': forms.Textarea(attrs={'class': 'form-control textarea', 'id':'description', 'rows': '3'}),
			'department': forms.Select(attrs={'class': 'form-select', 'id':'dept'}),
		}

class DepartmentForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = ('name', 'description')
		labels = {
			'name': '',
			'description': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'id':'name'}),
			'description': forms.Textarea(attrs={'class': 'form-control textarea', 'id':'description', 'rows': '3'}),
		}