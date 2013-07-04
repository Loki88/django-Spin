# This Python file uses the following encoding: utf-8

from spin_base.models import UserProfile
from django.db import models

class Relationship(models.Model):
	'''
	This class handles the process of request/response
	involved in user's relationship; when a followed user
	is private, he need to approve the relationship.
	'''

	follower = models.ForeignKey(UserProfile, related_name='user_following')
	'''
	The user who made the request to follow.
	'''

	followed = models.ForeignKey(UserProfile, related_name='user_followed')
	'''
	The user who will receive the request.
	'''

	approved = models.BooleanField(default=True)
	'''
	Bool to approve following requests.
	'''

	class Meta:
		app_label = "spin_base"