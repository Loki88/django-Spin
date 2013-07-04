from django import forms
from spin_base.models import Comment
from django.utils.translation import ugettext as _

class CommentForm(forms.ModelForm):
	'''
	Form inherited from ModelForm that manages the comments.
	'''
	content = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'id':'comment-input', 'class':'comment-input-class row-fluid spin-area'}))

	class Meta:
		model = Comment
		exclude = ('author', 'spin')

	class Media:
		css = {
			'all': ('css/comment.css',)
		}
		js = ('js/comment-form.js',)