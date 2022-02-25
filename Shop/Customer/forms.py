from django import forms
from .models import UserData
from mapwidgets.widgets import GooglePointFieldWidget


class ManageCreateUserDataForm(forms.ModelForm):
	class Meta:
		model = UserData
		fields = [
			'user',
			'first_name',
			'address',
			'city',
		]
		widgets = {
			'address': GooglePointFieldWidget,
		}

