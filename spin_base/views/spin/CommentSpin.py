# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from spin_base.forms import CommentForm
from spin_base.models import Spin
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class CommentSpin(AjaxFormResponseMixin, CreateView):
	'''
	This class permits to add a comment to a spin.
	'''
	form_class = CommentForm

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(CommentSpin, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.author = self.request.user.userprofile
		spin = get_object_or_404(Spin, pk=self.kwargs.get('spin_id'))
		if form.instance.author in spin.author.followers.all() or not spin.author.private:
			form.instance.spin = spin
			return super(CommentSpin, self).form_valid(form)
		else:
			response = HttpResponse()
			response.status_code = 403
			return response

	def form_invalid(self, form):
		if self.request.is_ajax():
			return super(CommentSpin, self).form_invalid(form)
		return HttpResponseRedirect(self.request.session.get('path', ''))
	
	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect(self.request.session.get('path', ''))
	
	def get_success_url(self):
		return self.request.session.get('path', '')