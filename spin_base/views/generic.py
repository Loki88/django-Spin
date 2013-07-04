# This Python file uses the following encoding: utf-8

from django.views.generic import TemplateView, ListView
from django.utils.translation import ugettext as _
from spin_base.forms import LoginForm, RegistrationForm, SpinForm, CommentForm
from spin_base.models import UserProfile, Spin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
	'''
	This view displays home page. If user is authenticated this redirects to
	following and followers' ribbits page, else this shows the home page with
	login form and registration one.
	'''

	template_name = 'spin_base/home_base.html'
	'''
	Class attribute which defines the page to display in response to a user call.
	'''

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated() and request.user.is_active:
			return HttpResponseRedirect( reverse('spin:user-home') )
		return super(HomeView, self).dispatch(request, *args, **kwargs)


	def get_context_data(self, **kwargs):
		context = {}
		username = self.request.get_signed_cookie('access', False)
		if username:
			login_form = LoginForm(initial={'username': username, 'remember': True})
		else:
			login_form = LoginForm()
		context['login_form'] = login_form
		context['registration_form'] = RegistrationForm()
		return context


class UserHomeView(ListView):
	'''
	This view displays the home for authenticated users.
	The home shows the list of latest followers' spins.
	'''
	# queryset = Spin.objects.all()
	paginate_by = 15
	template_name = 'spin_base/user_home.html'
	context_object_name = 'relevant_elements'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(UserHomeView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		try:
			kwargs['page']
		except:
			kwargs['page']=1
		context = super(UserHomeView, self).get_context_data(**kwargs)
		self.request.session['path'] = self.request.path
		context['comment_form'] = CommentForm()
		context['spin_form'] = SpinForm()
		context['home_active'] = 'active'
		return context

	def get_queryset(self):
		return Spin.objects.filter(author__user_followed__follower=self.request.user.userprofile, author__user_followed__approved=True)


class PublicProfiles(ListView):
	'''
	This view displays the public user profiles, so the user can start following someone.
	'''
	#queryset = UserProfile.objects.all().filter(private=False).order_by('-spinned__date').distinct('username')
	template_name = 'spin_base/generic/user_list.html'
	context_object_name = 'user_list'
	paginate_by = 15

	def get_context_data(self, **kwargs):
		context = super(PublicProfiles, self).get_context_data(**kwargs)
		self.request.session['path'] = self.request.path
		context['list_title'] = _('Public profiles on Spin:')
		context['spin_form'] = SpinForm()
		context['public_profiles_active'] = 'active'
		return context

	def get_queryset(self):
		return UserProfile.objects.filter(private=False).exclude(username=self.request.user.username).order_by('last_login')

class ListControl(ListView):
	'''
	Utility class that defines the base list actions for followers and followings lists.
	'''
	template_name = 'spin_base/generic/user_list.html'
	context_object_name = 'user_list'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.username != kwargs['username']:
			try:
				target_user = UserProfile.objects.get(username=kwargs['username'])
			except:
				pass
			else:
				if (target_user.private and target_user.user_followed.filter(follower=request.user.userprofile, approved=True).exists())\
						or (not target_user.private):
					return super(ListControl, self).dispatch(request, *args, **kwargs)
			
			return HttpResponseRedirect(request.session.get('path', ''))
		else:
			return super(ListControl, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ListControl, self).get_context_data(**kwargs)
		self.request.session['path'] = self.request.path
		context['spin_form'] = SpinForm()
		return context

class FollowersList(ListControl):
	'''
	Displays user's followers.
	'''
	# template_name = 'spin_base/user_list.html'
	# context_object_name = 'user_list'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(FollowersList, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return UserProfile.objects.filter(user_following__followed__username=self.kwargs['username'],  user_following__approved=True)

	def get_context_data(self, **kwargs):
		context = {}
		context = super(FollowersList, self).get_context_data(**kwargs)
		context['active_followers'] = 'active'
		context['list_title'] = self.kwargs['username'] + " " + _('followers list')
		return context

class FollowingList(ListControl):
	'''
	Displays user's followings.
	'''
	# template_name = 'spin_base/user_list.html'
	# context_object_name = 'user_list'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(FollowingList, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return UserProfile.objects.filter(user_followed__follower__username=self.kwargs['username'],  user_followed__approved=True)

	def get_context_data(self, **kwargs):
		context = {}
		context = super(FollowingList, self).get_context_data(**kwargs)
		context['active_following'] = 'active'
		context['list_title'] = self.kwargs['username'] + " " + _('following list')
		return context