from django.db import models
from django.utils.translation import ugettext as _
from spin import settings

class Customization(models.Model):
	'''
	This class contains the style for the spin app.
	'''

	well_color = models.CharField(max_length=6, blank=True, null=True)
	'''
	color of well boxes
	'''

	background_color = models.CharField(max_length=6, blank=True, null=True)
	'''
	'''
	
	nav_inverse = models.BooleanField(_('Do you want a reverse navbar?'), default=True, blank=True)
	'''
	'''
	
	background_image = models.CharField(max_length=100, blank=True, null=True)
	'''
	'''
	class Meta:
		app_label = 'spin_base'