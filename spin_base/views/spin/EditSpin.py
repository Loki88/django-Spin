# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from spin_base.models import Spin
from spin_base.forms import SpinForm
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class EditSpin(AjaxFormResponseMixin, UpdateView):
	'''
	View that permits to modify a spin.
	'''
	form_class = SpinForm
	model = Spin

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		spin = self.get_object()
		if spin in request.user.userprofile.spinned.all():
			return super(EditSpin, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseForbidden()

	def form_valid(self, form):
		user = self.request.user.userprofile
		form.instance.author = user
		spin = get_object_or_404(Spin, id=self.kwargs['pk'])
		form.instance.spin = spin
		if spin in user.spinned.all():
			return super(EditSpin, self).form_valid(form)
		else:
			response = HttpResponse()
			response.status_code = 403
			return response

	def form_invalid(self, form):
		if self.request.is_ajax():
			return super(EditSpin, self).form_invalid(form)
		return HttpResponseRedirect(self.request.session.get('path', '')+'#'+self.object.id)

	# def form_invalid(self, form):
	# 	return HttpResponseRedirect(self.request.session.get('path', '')+'#'+self.object.id)

	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect(self.request.session.get('path', ''))

	def get_success_url(self):
		return self.request.session.get('path', '')