from django import forms
from spin_base.models import Report, UserReport, SpinReport, CommentReport
from django.utils.translation import ugettext as _

class ReportUserForm(forms.ModelForm):
	'''
	Model form to report a user.
	'''
	class Meta:
		model = UserReport
		fields = ('content',)

	def is_reported(self):
		'''
		This checks if the user has been yet reported by the user who try to submit a report.
		Returns:
		'''
		if self.instance.target_profile_id is not None:
			if UserReport.objects.filter(target_profile__id=self.instance.target_profile_id,
					user= self.instance.user).exists():
				self.errors['__all__'] = _("You've yet submitted a report about this user.")
				return True
			else:
				return False
		return True

class ReportSpinForm(forms.ModelForm):
	'''
	Model form to report a spin.
	'''
	class Meta:
		model = SpinReport
		fields = ('content',)

	def is_reported(self):
		'''
		This checks if the spin has been yet reported by the user who try to submit a report.
		Returns:
		'''
		if self.instance.target_spin_id is not None:
			if SpinReport.objects.filter(target_spin__id=self.instance.target_spin_id,
					user= self.instance.user).exists():
				self.errors['__all__'] = _("You've yet submitted a report about this spin.")
				return True
			else:
				return False
		return True

class ReportCommentForm(forms.ModelForm):
	'''
	Model form to report a comment.
	'''
	class Meta:
		model = CommentReport
		fields = ('content',)

	def is_reported(self):
		'''
		This checks if the comment has been yet reported by the user who try to submit a report.
		Returns:
		'''
		if self.instance.target_comment_id is not None:
			if CommentReport.objects.filter(target_comment__id=self.instance.target_comment_id,
					user= self.instance.user).exists():
				self.errors['__all__'] = _("You've yet submitted a report about this comment.")
				return True
			else:
				return False
		return True