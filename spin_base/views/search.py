from django.views.generic import ListView
from itertools import chain
import datetime
from spin_base.models import UserProfile, Spin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from spin_base.forms import LoginForm, RegistrationForm, SpinForm, CommentForm

class Search(ListView):
	'''
	View that implements the search operations, including tag search.
	'''
	paginate_by = 10
	template_name = 'spin_base/search_results.html'
	context_object_name = 'search_results'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(Search, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		search_string=self.request.GET.get('search_string', '')
		if search_string != '':
			if search_string[0] == '@':
				# search for user
				return UserProfile.objects.filter(username__istartswith=search_string[1:])
			elif search_string[0] == '#':
				# search for Spin
				if len(search_string) < 4:
					return []
				return Spin.objects.filter(content__icontains=search_string[1:])
			else:
				# search for user and Spin
				if len(search_string) < 3:
					return []
				users = list(UserProfile.objects.filter(username__istartswith=search_string))
				spins = list(Spin.objects.filter(content__icontains=search_string))
				# full_length = len(users) + len(spins)
				results = users + spins
				
				return sorted(results, key= lambda x: x.get_date(), reverse=True)
			
				# return self.fall_back_to_sql(search_string)
				
		else:
			return []

	def get_context_data(self, **kwargs):
		context = super(Search, self).get_context_data(**kwargs)
		context['search_string'] = self.request.GET.get('search_string')
		self.request.session['path'] = self.request.path
		context['comment_form'] = CommentForm()
		context['spin_form'] = SpinForm()
		return context

