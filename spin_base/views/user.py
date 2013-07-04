# This Python file uses the following encoding: utf-8

from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import get_object_or_404
from spin_base.forms import SpinForm, CommentForm
from spin_base.models import UserProfile, Spin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


class UserDetail(SingleObjectMixin, ListView):
	'''
	This class renders a generic user's profile, managing the different users that could visit this one.
	'''
	template_name = 'spin_base/user/user_profile.html'
	slug_field = 'username'
	paginate_by = 5


	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(UserDetail, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		'''
		Returns the context needed for correct rendering of user's profile page.
		It controls all the possible relations between two users.
		'''
		try:
			kwargs['page']
		except:
			kwargs['page']=1
		kwargs['profile'] = self.object
		context = super(UserDetail, self).get_context_data(**kwargs)
		request_user = self.request.user.userprofile
		self.request.session['path']=self.request.path
		context['spin_form'] = SpinForm()
		context['comment_form'] = CommentForm()
		if request_user.username != self.object.username:
			if not request_user.is_black_listed(self.object):
				rel = request_user.is_following(self.object)
				if rel != False:
					context['follows'] = True
					if rel.approved:
						context['can_see'] = True
				
				if not self.object.private:
					context['can_see']=True
		else:
			context['requests'] = self.get_private_user_requests()
			context['can_see'] = True
			context['follows_disabled'] = True
			context['profile_active'] = 'active'

		if context.get('can_see'):
			context['user_media'] = self.object.spinned.filter(multispin__multimedia_path__isnull=False)[:4]
		return context


	def get_queryset(self):
		self.object = self.get_object(UserProfile.objects.all())
		if self.request.user.userprofile in self.object.blocked.all():
			return Spin.objects.none()
		return self.object.spinned.all()

	def get_private_user_requests(self):
		'''
		Provides waiting requests to follow.
		'''
		return self.request.user.userprofile.user_followed.filter(approved=False)

