from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from spin_base.models import Customization
from spin_base.forms import CustomizeForm, SpinForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CreateCustomizationView(CreateView):
	'''
	This view creates a customization look for the app.
	'''
	model = Customization
	form_class = CustomizeForm
	template_name = 'spin_base/generic/customize.html'
	context_object_name = 'custom'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(CreateCustomizationView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CreateCustomizationView, self).get_context_data(**kwargs)
		context['spin_form'] = SpinForm()
		return context

	def get_success_url(self):
		return self.request.session.get('path')

	def form_valid(self, form):
		customization = form.save(commit=False)
		user = self.request.user.userprofile
		previous_style = user.style
		if previous_style is not None and previous_style.style_users.count() == 1:
			previous_style.delete()
		ret = super(CreateCustomizationView, self).form_valid(form)
		user.style=customization
		user.save()
		return ret


class UpdateCustomizationView(UpdateView):
	'''
	This view updates the user customized look for the app.
	'''
	model = Customization
	form_class = CustomizeForm
	template_name = 'spin_base/generic/customize.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(UpdateCustomizationView, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super(UpdateCustomizationView, self).get_context_data(**kwargs)
		context['spin_form'] = SpinForm()
		return context

	def get_success_url(self):
		return self.request.session.get('path')


class CustomizationView(View):
	'''
	This view dispatches the requests for update and create.
	It look for a present customization, if not present, calls CreateCustomizationView, else UpdateCustomizationView.
	'''
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		style = request.user.userprofile.style
		if not style:
			view = CreateCustomizationView.as_view()
		else:
			view = UpdateCustomizationView.as_view()
			kwargs['pk'] = style.id
		return view(request, *args, **kwargs)

class RestoreCustomization(View):
	'''
	Resets the app look.
	'''
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		style = request.user.userprofile.style
		style.nav_inverse=True
		style.well_color=''
		style.background_color=''
		style.background_image=''
		style.save()
		return HttpResponseRedirect(reverse('spin:customize'))