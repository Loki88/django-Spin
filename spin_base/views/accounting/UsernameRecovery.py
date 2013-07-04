# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import FormView
from spin_base.forms import EmailForm
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

class UsernameRecovery(AjaxFormResponseMixin, FormView):
	'''
	This view sends an email to recover the username.
	It requires the email address, then sends an email with
	the username.
	'''
	form_class = EmailForm
	'''
	'''
	template_name = 'forms/lost_username.html'
	'''
	'''
	context_object_name = 'recover'
	'''
	'''

	def form_valid(self, form):
		'''
		'''
		user = get_object_or_404(UserProfile, email=form.cleaned_data['email'])
		self.send_recovery_mail(user)
		messages.success(self.request, _('An email has been sent to your email account.'))
		return super(UsernameRecovery, self).form_valid(form)

	def get_success_url(self):
		'''
		'''
		return reverse('spin:home')

	def send_recovery_mail(self, user):
		'''
		'''
		subject, mail_from, mail_to = _('spin: username recovery message'), 'spin@site.com', user.email
		text_content = _('Username recovery message') + '\n'
		text_content += user.first_name + _("your username is written below, be carefull, don't lost it 	again.\n\
		Username = %s \n To login the site, click on the below link:\n" % user.username)
		text_content += self.request.get_host() + reverse('spin:login') + '\n'
		text_content += _('If you should encounter some problem, contact us.')
		context = { 'server_url': self.request.get_host(), }
		context['lost_user'] = user
		html_content = render_to_string('email/recover_username.html', context)
		msg = EmailMultiAlternatives(subject, text_content, mail_from, [mail_to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()