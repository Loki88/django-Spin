# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.views.generic.edit import DeleteView
from spin_base.forms import SpinForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os

class AccountDelete(AjaxFormResponseMixin, DeleteView):
	'''
	This views handles the request to delete a user account.
	It's only accessible by logged user.
	'''
	template_name = 'spin_base/accounting/account_confirm_delete.html'


	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		'''
		'''
		return super(AccountDelete, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		'''
		'''
		if not request.is_ajax():
			return super(AccountDelete, self).get(request, *args, **kwargs)
		else:
			return 

	def get_context_data(self, **kwargs):
		'''
		'''
		context = super(AccountDelete, self).get_context_data(**kwargs)
		context['spin_form'] = SpinForm()
		context['request_path'] = self.request.session.get('path')
		return context

	def delete(self, request, *args, **kwargs):
		'''
		This method gets the request to delete and calls the parent delete
		after the removement of the user images.

		Throw:
			OSError: if the images is not found
		'''
		user = self.request.user.userprofile
		try:
			path = os.path.splitext(settings.MEDIA_ROOT + user.image.name)
			user.image.delete()
			os.remove(path[0]+'resized_'+path[1])
		except OSError:
			pass
		return super(AccountDelete, self).delete(request, *args, **kwargs)

	def get_object(self):
		'''
		'''
		return self.request.user.userprofile

	def get_success_url(self):
		'''
		'''
		return reverse('spin:home')