# This Python file uses the following encoding: utf-8

from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

class LogoutView(RedirectView):
	'''
	Destroys the session and return to home, calling the django auth
	logout function
	'''
	permanent = False
	'''
	If True sets a permanent redirect.
	'''

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		'''
		'''
		super(LogoutView, self).dispatch(request, *args, **kwargs)
		# response = HttpResponseRedirect(self.get_redirect_url())
		if request.session.get('login_remember', False):
			response.set_signed_cookie('access', str(request.user.username), max_age=129600)
		logout(request)
		return super(LogoutView, self).dispatch(request, *args, **kwargs)

	def get_redirect_url(self):
		'''
		'''
		return reverse('spin:home')