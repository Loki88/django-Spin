# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.views.generic.edit import FormView
from spin_base.forms import PasswordForm
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.signing import TimestampSigner
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

class SetNewPassword(AjaxFormResponseMixin, FormView):
	'''
	This class is callable only if has been requested recovery of password.
	This validates the url, then a cookie, timestamp-signed and crypted.
	Only a user which satisfies thes requisites can set a new password.
	'''
	form_class = PasswordForm
	template_name = 'forms/recovery_password.html'
	context_object_name = 'recover'
	max_age = 1200
	value = ''


	def dispatch(self, request, *args, **kwargs):
		'''
		'''
		signer = TimestampSigner()
		try:
			value = request.get_signed_cookie('recovery_key')
			self.value = signer.unsign(value, max_age=self.max_age)
		except:
			return HttpResponseForbidden('This page is expired')
		else:
			return super(SetNewPassword, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		'''
		'''
		context = super(SetNewPassword, self).get_context_data(**kwargs)
		context['recovery'] = {'pk': self.kwargs['pk']}
		return context

	def form_valid(self, form):
		'''
		'''
		user = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
		if self.value == str(user):
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.success(self.request, _('Your password has been successfully changed.'))
			response = super(SetNewPassword, self).form_valid(form)
			response.delete_cookie('recovery_key')
			return response
		else:
			return super(SetNewPassword, self).form_invalid(form)

	def get_success_url(self):
		'''
		'''
		return reverse('spin:home')