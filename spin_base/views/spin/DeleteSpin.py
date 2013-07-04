# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from spin_base.models import Spin, Comment
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import os


class DeleteSpin(AjaxFormResponseMixin, DeleteView):
	'''
	View that deletes spins.
	'''
	model = Spin
	pk_url_kwarg = 'spin_id'
	context_object_name = 'confirm_delete'
	template_name = 'spin_base/spin/spin_confirm_delete.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		spin = self.get_object()
		if spin in request.user.userprofile.spinned.all():
			return super(DeleteSpin, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseForbidden()

	def get_context_data(self, **kwargs):
		context = super(DeleteSpin, self).get_context_data(**kwargs)
		context['request_path'] = self.request.session['path']
		return context

	def delete(self, request, *args, **kwargs):
		try:
			path = os.path.splitext(settings.MEDIA_ROOT + spin.multispin.multimedia_path.name)
			spin.multispin.multimedia_path.delete()
			os.remove(path[0]+'resized_'+path[1])
		except:
			pass
		Comment.objects.filter(spin__pk=self.kwargs[self.pk_url_kwarg]).delete()
		return super(DeleteSpin, self).delete(request, *args, **kwargs)
			

	def get_success_url(self):
		return self.request.session.get('path', '')