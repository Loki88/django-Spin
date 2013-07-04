from django.db import models
from spin_base.models import UserProfile, Spin, Comment


class Report(models.Model):
	'''
	Base class for reporting user's abuses
	'''

	user = models.ForeignKey(UserProfile, related_name='reported')
	'''
	User who submit the report.
	'''
	content = models.TextField(max_length=200)
	'''
	Text explaination of report.
	'''
	date = models.DateTimeField(auto_now=True)
	'''
	Date when it was submitted.
	'''

	class Meta:
		app_label = "spin_base"

	def get_target(self):
		'''
		Returns:
			object. the target which report is referred to.
		'''
		try:
			target = self.userreport.target_profile
		except:
			try:
				target = self.spinreport.target_spin
			except:
				try:
					target = self.commentreport.target_comment
				except:
					return None

		return target




class UserReport(Report):
	'''
	Specific report for UserProfile.
	'''

	target_profile = models.ForeignKey(UserProfile, related_name='reported_user')
	'''
	Target profile of a report.
	'''
	class Meta:
		app_label = 'spin_base'


class SpinReport(Report):
	'''
	Specific report for Spin.
	'''

	target_spin = models.ForeignKey(Spin, related_name='reported_spin')
	'''
	'''
	
	class Meta:
		app_label = 'spin_base'


class CommentReport(Report):
	'''
	Specific report for Comment.
	'''

	target_comment = models.ForeignKey(Comment, related_name='reported_comment')
	'''
	'''
	class Meta:
		app_label = 'spin_base'