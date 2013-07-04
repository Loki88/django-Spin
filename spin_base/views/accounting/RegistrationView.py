# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.views.generic.edit import CreateView
from spin_base.forms import RegistrationForm
from spin_base.models import UserProfile
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

class RegistrationView(AjaxFormResponseMixin, CreateView):
	'''
	This view handles the registration of a user, creating a profile.
	When the user is registred it sends an email with activation link.
	'''
	model = UserProfile
	template_name = 'spin_base/accounting/registration_page.html'
 	form_class = RegistrationForm
 	context_object_name = 'registration_form'

 	def get_context_data(self, **kwargs):
 		context = super(RegistrationView, self).get_context_data(**kwargs)
		context[self.context_object_name] = context['form']
		return context

 	def form_valid(self, form):
 		instance = form.save(commit=False)
 		response = super(RegistrationView, self).form_valid(form)
 		self.send_activation_mail(instance)
 		instance.save()
 		return response

 	def get_success_url(self):
 		return reverse('spin:registration_complete')

 	def send_activation_mail(self, user):
 		if user.email is not None:
 			subject, mail_from, mail_to = _('Wellcome to spin'), 'spin@site.com', user.email
 			text_content = _('Tank you for registrating on spin') + '\n'
 			text_content += user.first_name + _("your account is ready to be used and you're experience on spin's starting.\n\
				You have just to confirm your email address. To do this, click on the following link or copy and paste it in your browser:\n")
 			text_content += self.request.get_host() + reverse('spin:activation', kwargs={'pk': user.pk, 'activation_key': user.activation}) + '\n'
 			text_content += _('If you should encounter some problem, contact us.')
 			context = { 'server_url': self.request.get_host(), }
 			context['new_user'] = user
 			html_content = render_to_string('email/activation_mail.html', context)
 			msg = EmailMultiAlternatives(subject, text_content, mail_from, [mail_to])
 			msg.attach_alternative(html_content, "text/html")
 			msg.send()