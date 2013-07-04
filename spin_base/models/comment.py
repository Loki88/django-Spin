from django.db import models
from spin_base.models import Spin, UserProfile

class Comment(models.Model):
	'''
	Comments from users to spins
	'''

	author = models.ForeignKey(UserProfile, related_name='comments')
	'''
	Author of the commente
	'''

	spin = models.ForeignKey(Spin, related_name='commented')
	'''
	The commented spin
	'''

	content = models.CharField(max_length=140)
	'''
	The comment content
	'''

	date = models.DateTimeField(auto_now=True)
	'''
	Date when comment was posted
	'''
	# da eliminare
	# last_modified = models.DateTimeField(auto_now_add=True)

	class Meta:
		app_label = 'spin_base'
		ordering = ['date']

	# def get_absolute_url(self):
	# 	return reverse('spin:user-profile', kwargs={'slug'=})

	def is_signaled(self):
		'''
		Returns:
			True -- if the comment has been reported
			False -- if it's not been reported
		'''
		if self.reported_comment.all().exists():
			return True
		else:
			return False


	def report_number(self):
		'''
		Returns:
			the number of reports
		'''
		return self.reported_comment.count()