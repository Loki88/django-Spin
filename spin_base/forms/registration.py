from django import forms
from django.db.models import Count
from django.utils.translation import ugettext as _
from spin_base.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
import hashlib


class RegistrationForm(UserCreationForm):
	'''
	Form class that extends the UserCreationForm for UserProfile, a class inherited from django.contrib.auth.models.User.
	'''

	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
		'id': 'inputUsername', 'class': 'input-medium span* form-input', 'placeholder' : _('Username')}))

	password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={
		'id': 'inputPasswordConfirm', 'class': 'input-medium span*', 'placeholder' : _('Password')}))

	password2 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={
		'id': 'inputPasswordConfirm', 'class': 'input-medium span*', 'placeholder' : _('Confirm Password')}))

	class Meta:
		model = UserProfile
		fields = ('private', 'first_name', 'last_name', 'email', 'username')
		widgets = {
			'first_name': forms.widgets.TextInput(attrs={'id': 'inputName',	'class': 'input-medium span* form-input', 'placeholder' : _('Name')}),
			'last_name' : forms.widgets.TextInput(attrs={'id': 'inputSurname', 'class': 'input-medium span* form-input',	'placeholder' : _('Last name')}),
			'email' : forms.widgets.TextInput(attrs={'id': 'inputEmail', 'class': 'input-medium span* form-input',	'placeholder' : 'email'}),
		}

	class Media:
		extends = True
		js = ('js/accounting.js',)

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data.get('email')).exists():
			raise forms.ValidationError(_('This email is yet used'))
		else:
			return self.cleaned_data.get('email')


	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
 		user.set_activation_key()
 		user.is_active = False
 		user.save()
 		if commit:
 			user.save()
 		else:
 			return user