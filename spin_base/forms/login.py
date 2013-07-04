from django import forms
from django.forms import widgets
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
import hashlib

'''
This section is dedicated to the integration of forms with
Twitter Bootstrap. The plan is to display a styled form
everytime necessary defining the widgets every field needs for 
the specific forms. In this way, the style is not hardcoded and
can be modified programmatically. Think to add some javascript effect
at these forms or fields: Media class makes it possible.
'''

class LoginForm(forms.Form):
	'''
	Form that handles the login.
	'''
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'input-medium span*', \
		'id' : 'inputUsername', 'placeholder' : 'Username'}))
	'''
	'''
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class' : 'input-medium span*',\
		'id' : 'inputPassword', 'placeholder' : 'Password'}))
	'''
	'''
	remember = forms.BooleanField(required=False)
	'''
	'''


	class Media:
		js = ('js/accounting.js',)

	def is_valid(self):
		'''
		'''
		form = super(LoginForm, self).is_valid()
		if form:
			user = authenticate(username=self.cleaned_data.get('username'), \
				password=self.cleaned_data.get('password'))
			if user is not None:
				if user.is_active:
					return user
				else:
					self.errors['__all__'] = _('This account is not active')
					return False
		self.errors['__all__'] = _('Wrong username or password')
		return False




class InlineLoginForm(LoginForm):
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'input-small',\
		'id' : 'prependedInput', 'placeholder' : 'Username'}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class' : 'input-small', \
		'placeholder' : 'Password'}))
	remember = forms.BooleanField()
