# -*- coding:utf-8 -*-
from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm 
from principal.models import *

class NuevoUserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
		widgets= {
		'password': forms.PasswordInput(),
		}

