# This Python file uses the following encoding: utf-8

from django import forms
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext as _
from spin_base.models import UserProfile
import os
from PIL import Image
from spin import settings
import pytz

class UserProfileForm(UserChangeForm):
	'''
	Form to change account informations.
	'''

	resize_width = 256  #px

	password = forms.CharField(required=False, widget=forms.widgets.PasswordInput(attrs={'id': 'inputPassword', 'class': 'input-medium form-input',	'placeholder' : 'Password'}))

	confirm_password = forms.CharField(required=False, widget=forms.widgets.PasswordInput(attrs={
		'id': 'inputPasswordConfirm', 'class': 'input-medium', 'placeholder' : _('Confirm Password')}))

	time_zone = forms.CharField(required=False, widget=forms.widgets.Select())

	class Meta:
		model = UserProfile
		fields = ('private', 'image', 'first_name', 'last_name', 'email', 'username', 'password', 'time_zone')
		widgets = {
			'first_name': forms.widgets.TextInput(attrs={'id': 'inputName',	'class': 'input-medium form-input', 'placeholder' : _('Name')}),
			'last_name' : forms.widgets.TextInput(attrs={'id': 'inputSurname', 'class': 'input-medium form-input',	'placeholder' : _('Last name')}),
			'email' : forms.widgets.TextInput(attrs={'id': 'inputEmail', 'class': 'input-medium form-input',	'placeholder' : 'email'}),
			'username' : forms.widgets.TextInput(attrs={'id': 'inputUsername', 'class': 'input-medium form-input', 'placeholder' : _('Username')}),
			# 'password' : forms.widgets.PasswordInput(attrs={'id': 'inputPassword', 'class': 'input-medium form-input',	'placeholder' : 'Password'}),
			'image': forms.widgets.ClearableFileInput(attrs={'id': 'inputImage', 'class': 'input-medium span* form-input', 'placeholder' : _('Name')}),
		}

	# class Media:
	# 	js = ('js/form-upload.js',)

	def is_valid(self):
		form = super(UserProfileForm, self).is_valid()
		# if self.cleaned_data.get('password', None) is not None and not check_password(self.cleaned_data.get('password'), self.instance.password):
		# 	if self.cleaned_data.get('password', '') != self.cleaned_data.get('confirm_password'):
		# 		try:
		# 			self.errors['password'].append(_("Passwords don't match"))
		# 		except KeyError:
		# 			self.errors['password'] = [_("Passwords don't match"), ]
		# 	else:
		# 		self.cleaned_data['password'] = make_password(self.cleaned_data.get('password'))
		# else:
		# 	self.cleaned_data['password'] = None

		queryset = UserProfile.objects.all()
		if self.initial.get('username') != self.cleaned_data.get('username'):
			user_count = queryset.filter(username=self.cleaned_data.get('username')).exists()
			if user_count:
				try:
					self.errors['username'].append(_('Username taken'))
				except KeyError:
					self.errors['username'] = [_('Username taken'), ]

		if self.initial.get('email') != self.cleaned_data.get('email'):
			email_count = queryset.filter(email=self.cleaned_data.get('email')).exists()
			if email_count:
				try:
					self.errors['email'].append(_('This email is used'))
				except KeyError:
					self.errors['email'] = [_('This email is used'), ]
		
		

		if self.cleaned_data.get('time_zone') not in pytz.common_timezones:
			self.cleaned_data['time_zone'] = settings.TIME_ZONE

		if self.errors and not form:
			try:
				self.errors['__all__'].append(_('Please correct the fields in error'))
			except KeyError:
				self.errors['__all__'] = _('Please correct the fields in error')
			return False
		else:
			return True


	def save(self, commit=True):
		user = super(UserProfileForm, self).save(commit=False)
		image = user.image
		if self.initial['image'] is not None and image and\
			self.initial['image'].name != image.name:
			try:
		 		path = os.path.join(settings.MEDIA_ROOT, self.initial['image'].name)
		 		# remove full size image
		 		os.remove(path)
		 		path = os.path.splitext(path)
		 		# remove resized image
		 		os.remove(path[0]+'resized_'+path[1])
		 	except OSError:
		 		pass
		user.save()
		image = user.image
		if image is not None and image is not self.initial.get('image'):
			img = Image.open(settings.MEDIA_ROOT + image.name)
 			resize_height = int(float(img.size[1]*self.resize_width/img.size[0]))
 			img = img.resize((self.resize_width, resize_height), Image.ANTIALIAS)
 			path = os.path.splitext(settings.MEDIA_ROOT + user.image.name)
 			img.save(path[0] + 'resized_' + path[1], 'jpeg')
 		if not commit:
 			return user