# This Python file uses the following encoding: utf-8

from django.views.generic import View
from django.http import HttpResponseRedirect
from spin_base.models import UserProfile, Relationship
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


class AddBlock(View):
	'''
	This class manages adding block to user profile.
	'''
	
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		super(AddBlock, self).dispatch(request, *args, **kwargs)
		user_to_block = get_object_or_404(UserProfile, username=kwargs['username'])
		if user_to_block not in request.user.userprofile.blocked.all():
			request.user.userprofile.blocked.add(user_to_block)
			try:
				rel = request.user.userprofile.user_followed.get(follower=user_to_block)
			except:
				# the user is not followed by the blocked one
				pass
			else:
				rel.delete()
		return HttpResponseRedirect(request.session.get('path', ''))

class RemoveBlock(View):
	'''
	This class manages removing block to user profile.
	'''

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		super(RemoveBlock, self).dispatch(request, *args, **kwargs)
		user_blocked = get_object_or_404(UserProfile, username=kwargs['username'])
		if user_blocked in request.user.userprofile.blocked.all():
			request.user.userprofile.blocked.remove(user_blocked)

		return HttpResponseRedirect(request.session.get('path', ''))

class Follow(View):
	'''
	This class permits user to follow another one or to ask following.
	'''

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		super(Follow, self).dispatch(request, *args, **kwargs)
		user_to_follow = get_object_or_404(UserProfile, username=kwargs['username'])
		if self.request.user.userprofile not in user_to_follow.blocked.all():
			if not user_to_follow.user_followed.filter(follower=request.user.userprofile).exists():
				rel = Relationship(follower=request.user.userprofile, followed=user_to_follow)
				if user_to_follow.private:
					rel.approved = False
				rel.save()

		return HttpResponseRedirect(request.session.get('path', ''))

class StopFollow(View):
	'''
	This class removes the following relationship from one side of this one.
	'''

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		super(StopFollow, self).dispatch(request, *args, **kwargs)
		user_followed = get_object_or_404(UserProfile, username=kwargs['username'])
		try:
			rel = user_followed.user_followed.get(follower=request.user.userprofile)
		except:
			# the user is not a follower
			pass
		else:
			rel.delete()

		return HttpResponseRedirect(request.session.get('path', ''))

class ApproveFollowing(View):
	'''
	This class permits private users to approve the following requests.
	If a user wants to disapprove, he should call StopFollow.
	'''

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		super(ApproveFollowing, self).dispatch(request, *args, **kwargs)
		if self.request.user.userprofile.private:
			user_waiting = get_object_or_404(UserProfile, username=kwargs['username'])
			try:
				rel = request.user.userprofile.user_followed.get(follower=user_waiting, approved=False)
			except:
				# there is no waiting relation or it's approved
				pass
			else:
				if kwargs['method'] == 'accept':
					rel.approved=True
					rel.save()
				else:
					rel.delete()

		return HttpResponseRedirect(reverse('spin:user-profile', kwargs={'slug': self.request.user.username}))