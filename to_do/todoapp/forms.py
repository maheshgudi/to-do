from django.contrib.auth.models import User
from django import forms

class UserLoginForm(forms.Form):
	"""
	User loginform for to-do app
	"""
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())
