# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from spin_base.models import Comment
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


class DeleteComment(AjaxFormResponseMixin, DeleteView):
	'''
	View that deletes a comment.
	'''
	model = Comment
	context_object_name = 'confirm_delete'
	template_name = 'spin_base/spin/comment_confirm_delete.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		comment = self.get_object()
		if comment in self.request.user.userprofile.comments.all():
			return super(DeleteComment, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseForbidden()

	def get_context_data(self, **kwargs):
		context = super(DeleteComment, self).get_context_data(**kwargs)
		context['request_path'] = self.request.session['path']
		return context


	def get_success_url(self):
		return self.request.session.get('path', '')