from django.views.generic import RedirectView
from spin_base.models import Spin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class ReSpinView(RedirectView):
	'''
	This view handles the respin operation.
	It implements only the dispatch method, which contains the logic of the repin.
	'''
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		super(ReSpinView, self).dispatch(request, *args, **kwargs)
		spin = get_object_or_404(Spin, pk=kwargs['spin_id'])
		user = self.request.user.userprofile
		if user.id != spin.author.id and user not in spin.author.blocked.all():
			respin = self.request.user.userprofile.spinned.all().filter(respinned=spin)
			if not respin.exists():
				re_spin = Spin()
				re_spin.author = self.request.user.userprofile
				re_spin.content = spin.content
				re_spin.respinned = spin
				re_spin.save()
			else:
				respin.delete()
		return super(ReSpinView, self).dispatch(request, *args, **kwargs)

	def get_redirect_url(self):
		return request.session.get('path', '')
