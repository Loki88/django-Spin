# This Python file uses the following encoding: utf-8

from django.contrib.auth.models import User
from django.db import models
from spin import settings
from django.core.urlresolvers import reverse
from django.core.signing import Signer
from datetime import datetime

def get_upload_path(instance, filename):
		'''
		Returns the path from MEDIA_ROOT where to upload the file

		Kwargs:
			instance -- the file instance
			filename -- the name of file

		Returns:
			string. The path where to save the image
		'''
		username = str(instance.username)
		date = datetime.utcnow()
		return 'profiles/' + username + date.strftime("%Y-%m-%d")+filename


class UserProfile(User):
	'''
	UserProfile adds some features to Django's authentication User class.
	'''

	following = models.ManyToManyField('self', symmetrical=False,\
		related_name='followers', through='Relationship')
	'''
	The following mechanism needs relationship between many users. An user
	can have many follower and following many people. The relationship needs to be
	approved by a private user, so there's the need of a field "approved" in a
	separate table.
	'''

	blocked = models.ManyToManyField('self', symmetrical=False,\
		related_name='black_listed')
	'''
	This field represents user's black list.
	'''

	image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
	'''
	This rapresents the profile image. It's different from other images
	attacched to posts, since this isn't but is visible only in user profile.
	'''

	private = models.BooleanField(default=False)
	'''
	A bool indicating if the profile is reserved to accepted followings.
	'''

	style = models.ForeignKey('Customization', related_name='style_users', blank=True, null=True)
	'''
	The id of the choosen style for spin-app.
	'''

	activation = models.CharField(blank=True, null=True, default=None, max_length=200)
	'''
	This is different from user.is_active. It contains the activation key.
	'''

	time_zone = models.CharField(max_length=30)
	'''
	This is the time zone, for timing middleware.
	'''
	

	class Meta:
		app_label = "spin_base"
		


	def __unicode__(self):
		string = self.first_name
		string += ' ' + self.last_name
		string += ' @'+self.username
		return string

	def get_absolute_url(self):
		'''
		Returns the url where is visible the user profile.
		'''
		return reverse('spin:user-profile', kwargs= {'slug': self.username})

	def is_following(self, user):
		'''
		Returns:
			True -- user is followed by this instance of user profile
			False -- if he's not followed

		Kwargs:
			instance: the file instance
			filename: the name of file
		'''
		try:
			rel = self.user_following.get(followed=user)
		except:
			return False
		else:
			return rel
			
	def get_date(self):
		try:
			return self.last_login
		except:
			return self.date_joined


	def is_black_listed(self, user):
		'''
		Returns True if *self* is in *user*'s black list.
		Kwargs:
			user: UserProfile object, who need to be checked in black list
		'''
		if self.black_listed.filter(username=user.username).exists():
			return True
		else:
			return False

	def get_requests(self):
		'''
		Returns the number of waiting requests.
		'''
		return self.user_followed.filter(approved=False).count('id')

	def is_signaled(self):
		'''
		'''
		if self.reported_user.all().exists():
			return True
		else:
			return False

	def report_number(self):
		'''
		'''
		return self.reported_user.count()

	def set_activation_key(self):
		'''
		Sets the activation key for the user
		
		Returns:
			None
		'''
		signing = Signer(self.email)
		self.activation = signing.sign(self.username)