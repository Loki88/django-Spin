# This Python file uses the following encoding: utf-8

from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from spin_base.models import UserProfile
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


class ActivationView(RedirectView):
	'''
	This view permits the activation of UserProfile.

	Raises:
		404 errors if the calls doesn't fit some pre-requisites
	'''
	permanent = False

	def dispatch(self, request, *args, **kwargs):
		'''
		'''
		user = get_object_or_404(UserProfile, pk=kwargs['pk'])
		if user.activation == kwargs['activation_key'] and user.activation is not None:
			user.is_active = True
			user.save()
			messages.success(request, _('Your account has been successfully activated.'))
		else:
			messages.warning(request, _('Your account is not active, this may be an our problem. Retry, but if the problem persists, contact us.'))
		del kwargs['pk']
		del kwargs['activation_key']
		return super(ActivationView, self).dispatch(request, *args, **kwargs)
	
	def get_redirect_url(self):
		'''
		'''
		return reverse('spin:home')