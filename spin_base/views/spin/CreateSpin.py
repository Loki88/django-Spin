# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.views.generic.edit import CreateView
from spin_base.forms import SpinForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class CreateSpin(AjaxFormResponseMixin, CreateView):
	'''
	View that handles the creation of a Spin.
	'''
	form_class = SpinForm
	template_name = 'spin_base/user_home.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(CreateSpin, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.author = self.request.user.userprofile
		return super(CreateSpin, self).form_valid(form)

	# def form_invalid(self, form):
	# 	if self.request.is_ajax():
	# 		return super(CreateSpin, self).form_invalid(form)
	# 	return HttpResponseRedirect(self.get_success_url)

	def get_success_url(self):
		return self.request.session.get('path', '')