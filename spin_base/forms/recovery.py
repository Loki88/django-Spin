from django import forms
from django.utils.translation import ugettext as _
from spin_base.models import UserProfile

class PasswordForm(forms.Form):
	'''
	This form catches the POST data for password recovery
	'''

	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-input'}))
	'''
	'''
	password = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'class': 'form-input'}))
	'''
	'''
	confirm_password = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'class': 'form-input'}))
	'''
	'''

	class Media:
		extends = True
		js = ('js/accounting.js',)

	def clean(self):
		'''
		Validates password and confirm_password.
		Raises:
			ValidationError: if passwords don't match.
		'''
		data = super(PasswordForm, self).clean()

		if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
			raise ValidationError(_("Passwords doesn't match"))

		return data

	def is_valid(self):
		valid = super(PasswordForm, self).is_valid()

		if not valid:
			self.errors['__all__'] = _('Please, correct the fields in error')
		return valid


class EmailForm(forms.Form):
	'''
	Permits the email recovery.
	'''

	email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-input'}))
	'''
	'''

	class Media:
		extends = True
		js = ('js/accounting.js',)

	def is_valid(self):
		valid = super(EmailForm, self).is_valid()

		if not valid:
			self.errors['__all__'] = _('Please, correct the fields in error')
		return valid


class UsernameForm(forms.Form):
	'''
	Permits the username recovery.
	'''

	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'form-input'}))
	'''
	'''
	
	class Media:
		extends = True
		js = ('js/accounting.js',)

	def is_valid(self):
		valid = super(UsernameForm, self).is_valid()

		if not valid:
			self.errors['__all__'] = _('Please, correct the fields in error')
		return valid