from django.db import models
from spin_base.models import UserProfile
from datetime import datetime

class Spin(models.Model):
	'''
	This class represents the shared information by a user.
	The name Spin derives from the spin, it alludes to an
	information cycle: Spin, reSpin
	'''

	author = models.ForeignKey(UserProfile, related_name='spinned')
	'''
	The user who's posted the Spin
	'''

	content = models.CharField(max_length=140)
	'''
	The text shared in the Spin
	'''

	date = models.DateTimeField(auto_now=True)
	'''
	The date when the Spin's been created
	'''

	last_modified = models.DateTimeField(auto_now_add=True)
	'''
	The date when the Spin's been modified for the last time
	'''

	respinned = models.ForeignKey('self', blank=True, null=True, related_name='respins')
	'''
	The spin which has been respinned, None if the spin is not a respin.
	'''
	
	class Meta:
		app_label = "spin_base"
		ordering = ['-date']
		get_latest_by = 'date'

	def __unicode__(self):
		return 'Spin: '+str(self.author)+' #'+str(self.id)

	def is_signaled(self):
		'''
		'''
		if self.reported_spin.all().exists():
			return True
		else:
			return False

	def report_number(self):
		'''
		'''
		return self.reported_spin.count()

	def get_date(self):
		return self.last_modified


def get_upload_path(instance, filename):
		'''
		Returns the path from MEDIA_ROOT where to upload the file

		Kwargs:
			instance: the file instance
			filename: the name of file

		Returns:
			string. The path where to save the file
		'''
		author = str(instance.author)
		date = datetime.utcnow()
		return author + "/"+ date.strftime("%Y/%m/%d/")+date.strftime("%H-%M-%S")+str(filename)


class MultiSpin(Spin):
	'''
	A Spin with multimedia content.
	'''

	multimedia_path = models.FileField(upload_to=get_upload_path, max_length=254)
	'''
	Filesystem path of multimedia content.
	'''

	class Meta:
		app_label = "spin_base"

	def __unicode__(self):
		return 'Multi'+super(MultiSpin, self).__unicode__()
