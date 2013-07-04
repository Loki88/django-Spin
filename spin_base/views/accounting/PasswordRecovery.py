# This Python file uses the following encoding: utf-8

from spin_base.mixin import AjaxFormResponseMixin
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import FormView
from spin_base.forms import UsernameForm
from django.shortcuts import get_object_or_404
from django.core.signing import TimestampSigner
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


class PasswordRecovery(AjaxFormResponseMixin, FormView):
	'''
	This view sends an email to recover the userprofile password.
	It requires the username, then sends email and send a link with
	limited lifetime to user.
	'''
	form_class = UsernameForm
	'''
	'''
	template_name = 'forms/lost_password.html'
	'''
	'''
	context_object_name = 'recover'
	'''
	'''
	recovery_key = None
	'''
	'''

	def post(self, request, *args, **kwargs):
		'''
		Args:
			request: the WSGI request object
			args:
			kwargs:
		'''
		form = self.form_class(request.POST)
		if form.is_valid():
			try:
				user = get_object_or_404(UserProfile, username=form.cleaned_data['username'])
			except:
				pass
			else:
				self.send_recovery_mail(user)
		return super(PasswordRecovery, self).post(request, *args, **kwargs)

	def form_valid(self, form):
		'''
		'''
		user = get_object_or_404(UserProfile, username=form.cleaned_data['username'])
		signer = TimestampSigner()
		recovery_key = signer.sign(str(user))
		self.send_recovery_mail(user)
		messages.success(self.request, _('An email has been sent to your email account.'))
		response = super(PasswordRecovery, self).form_valid(form)
		response.set_signed_cookie('recovery_key', recovery_key, max_age=1200)
		return response

	def get_success_url(self):
		'''
		'''
		return reverse('spin:home')

	def send_recovery_mail(self, user):
		'''
		'''
		subject, mail_from, mail_to = _('spin: password recovery message'), 'spin@site.com', user.email
		text_content = _('Password recovery message') + '\n'
		text_content += user.first_name + _("the following link is valid for 20 minutes, do quickly, click on or copy and paste it on your browser.\n")
		text_content += self.request.get_host() + reverse('spin:set-new-password', kwargs={'pk': user.pk} ) + '\n'
		text_content += _('If you should encounter some problem, contact us.')
		context = { 'server_url': self.request.get_host(), }
		context['lost_user'] = user
		html_content = render_to_string('email/recover_password.html', context)
		msg = EmailMultiAlternatives(subject, text_content, mail_from, [mail_to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()