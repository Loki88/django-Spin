# This Python file uses the following encoding: utf-8

from spin_base.models import Spin
from spin_base.forms import CommentForm, SpinForm
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class PublicSpin(ListView):
	'''
	View that renders a list of latest public spins.
	'''
	model = Spin
	paginate_by = 10
	template_name = 'spin_base/spin/public_spin.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(PublicSpin, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(PublicSpin, self).get_context_data(**kwargs)
		self.request.session['path'] = self.request.path
		context['spin_form'] = SpinForm()
		context['comment_form'] = CommentForm()
		context['public_spins_active'] = 'active'
		return context

	def get_queryset(self):
		# mettere in vista i più rilevanti oltre che i più recenti
		return Spin.objects.filter(author__private=False).exclude(author__blocked=self.request.user.userprofile).order_by('-date')
