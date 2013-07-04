# This Python file uses the following encoding: utf-8

from spin_base.models import Spin, Comment
from spin_base.forms import CommentForm, SpinForm
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

class DetailSpin(SingleObjectMixin, ListView):
	'''
	This view renders a single spin in detail with all its comments.
	'''
	template_name = 'spin_base/spin/spin.html'
	context_object_name = 'spin'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		response = super(DetailSpin, self).dispatch(request, *args, **kwargs)
		if self.object is None:
			return HttpResponseForbidden()
		else:
			return response

	def get_queryset(self):
		self.object = self.get_object(Spin.objects.all())
		user = self.request.user.userprofile
		if self.object not in self.request.user.userprofile.spinned.all():
			if self.object.author.user_followed.filter(approved=False, follower=user).exists() or\
				self.object.author.private or user in self.object.author.blocked.all():
				self.object = None
				return Comment.objects.none()
		return self.object.commented.all()

	def get_context_data(self, **kwargs):
		context = super(DetailSpin, self).get_context_data(**kwargs)
		if self.object is not None:
			context['spin'] = self.object
			context['profile'] = self.object.author
			self.request.session['path'] = self.request.path
			context['comment_form'] = CommentForm()
			context['spin_form'] = SpinForm()
		context['full_size'] = True
		return context