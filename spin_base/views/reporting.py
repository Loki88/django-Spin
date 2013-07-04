from django.views.generic.edit import CreateView
from spin_base.forms import ReportCommentForm, ReportSpinForm, ReportUserForm, SpinForm
from spin_base.models import CommentReport, SpinReport, UserReport
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class ReportCommentView(CreateView):
	'''

	'''
	model = CommentReport
	form_class = ReportCommentForm
	template_name = 'spin_base/generic/report.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ReportCommentView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ReportCommentView, self).get_context_data(**kwargs)
		context['request_path'] = self.request.path
		context['spin_form'] = SpinForm()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user.userprofile
		form.instance.target_comment_id = self.kwargs.get('comment', None)
		if form.is_reported():
			return self.form_invalid(form)

		return super(ReportCommentView, self).form_valid(form)

	def get_success_url(self):
		return self.request.session.get('path')


class ReportSpinView(CreateView):
	'''

	'''
	model = SpinReport
	form_class = ReportSpinForm
	template_name = 'spin_base/generic/report.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ReportSpinView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ReportSpinView, self).get_context_data(**kwargs)
		context['request_path'] = self.request.path
		context['spin_form'] = SpinForm()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user.userprofile
		form.instance.target_spin_id = self.kwargs.get('spin', None)
		if form.is_reported():
			return self.form_invalid(form)
		return super(ReportSpinView, self).form_valid(form)

	def get_success_url(self):
		return self.request.session.get('path')

class ReportUserView(CreateView):
	'''

	'''
	model = UserReport
	form_class = ReportUserForm
	template_name = 'spin_base/generic/report.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ReportUserView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ReportUserView, self).get_context_data(**kwargs)
		context['request_path'] = self.request.path
		context['spin_form'] = SpinForm()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user.userprofile
		form.instance.target_profile_id = self.kwargs.get('userid', None)
		if form.is_reported():
			return self.form_invalid(form)
		return super(ReportUserView, self).form_valid(form)

	def get_success_url(self):
		return self.request.session.get('path')