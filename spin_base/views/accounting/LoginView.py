# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.views.generic.edit import FormView
from django.contrib.auth import login
from spin_base.forms import LoginForm
from django.core.urlresolvers import reverse

class LoginView(AjaxFormResponseMixin, FormView):
	'''
	View that handles the login process
	'''
	template_name = 'spin_base/accounting/login_page.html'
	form_class = LoginForm

	def dispatch(self, request, *args, **kwargs):
		'''
		'''
 		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		'''
		'''
		context = super(LoginView, self).get_context_data(**kwargs)
		context['login_form'] = self.form_class()
		return context

	def post(self, request, *args, **kwargs):
		'''
		The post is called when login form is submitted.
		It validates the requests, then try the login and sets
		some session informations, such *spin_timezone* for user .
		'''
		form = self.form_class(request.POST)
		user = form.is_valid()
		if user:
			login(request, user)
			request.session['login_remember'] = form.cleaned_data.get('remember')
			request.session.set_expiry(0)
			profile = user.userprofile
			if profile.time_zone is not None:
				request.session['spin_timezone'] = profile.time_zone
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		'''
		'''
		response = super(LoginView,self).form_valid(form)
		response.delete_cookie('access')
		return response

	def get_success_url(self):
		'''
		'''
		if self.request.session.get('path'):
			return self.request.session.get('path')
		else:
			return reverse('spin:home')