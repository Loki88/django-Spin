# This Python file uses the following encoding: utf-8

from spin import settings
from spin_base.mixin import AjaxFormResponseMixin
from spin_base.forms import UserProfileForm, SpinForm
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from PIL import Image
import pytz
import os

class AccountView(AjaxFormResponseMixin, UpdateView):
	'''
	This method permits the update of user informations.
	It handles the timezones, so the user can report dates and time
	to his locale.
	'''
	form_class = UserProfileForm
	'''
	'''
	template_name = 'spin_base/accounting/account.html'
	'''
	'''
	resize_width = 256


	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		'''
		'''
		return super(AccountView, self).dispatch(request, *args, **kwargs)

	def get_object(self):
		'''
		'''
		self.object = self.request.user.userprofile
		return self.object

	def get_context_data(self, **kwargs):
		'''
		'''
		context = super(AccountView, self).get_context_data(**kwargs)
		context['spin_form'] = SpinForm()
		context['timezones'] = pytz.common_timezones
		return context

	def form_valid(self, form):
		'''
		This method responds to form valid *event* and sets a new time zone if
		modified. Then returns parent response.
		'''
		instance = form.save(commit=False)
		self.request.session['spin_timezone'] = instance.time_zone
		return super(AccountView, self).form_valid(form)


	def get_success_url(self):
		'''
		'''
		return self.request.session.get('path')