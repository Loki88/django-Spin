# This Python file uses the following encoding: utf-8

from django.conf.urls import patterns, include, url
from spin_base.views import HomeView, UserHomeView, UserDetail, FollowersList, FollowingList, PublicProfiles
from spin_base.views import RegistrationView, LoginView, LogoutView, AccountView, AccountDelete, ActivationView
from spin_base.views import Follow, StopFollow, AddBlock, RemoveBlock, ApproveFollowing
from spin_base.views import CreateSpin, PublicSpin, CommentSpin, EditSpin, DeleteSpin, DetailSpin, DeleteComment
from spin_base.views import ReSpinView, Search
from spin_base.views import ReportCommentView, ReportSpinView, ReportUserView
from spin_base.views import CustomizationView, RestoreCustomization
from spin_base.views import PasswordRecovery, UsernameRecovery, SetNewPassword
from django.views.generic import TemplateView

# general urls
urlpatterns = patterns('',
		url('^$', HomeView.as_view(), name='home'),
		url('^home/(\?page=(?P<page>[0-9]+))?$', UserHomeView.as_view(), name='user-home'),
		url('^(?P<slug>\w+)/profile/(\?page=(?P<page>[0-9]+))?$', UserDetail.as_view(), name='user-profile'),
		url('^(?P<username>\w+)/following/(\?page=(?P<page>[0-9]+))?$', FollowingList.as_view(), name="user-following-list"),
		url('^(?P<username>\w+)/followers/(\?page=(?P<page>[0-9]+))?$', FollowersList.as_view(), name='user-followers-list'),
		url('^public/profiles/(\?page=(?P<page>[0-9]+))?$', PublicProfiles.as_view(), name='public-profiles'),
		url('^public/spins/(\?page=(?P<page>[0-9]+))?$', PublicSpin.as_view(), name='latest-spins'),
		url('^search/$', Search.as_view(), name="search")
	)

# accounting urls
urlpatterns += patterns('',
		url('^user/logout/$', LogoutView.as_view(), name='logout'),
		url('^congratulation/$', TemplateView.as_view(
			template_name="spin_base/accounting/registration_successfull.html"), name='registration_complete'),
		url('^registration/$', RegistrationView.as_view(), name='registration'),
		url('^login/$', LoginView.as_view(), name='login'),
		url('^account/$', AccountView.as_view(), name="user-account" ),
		url('^delete/$', AccountDelete.as_view(), name="delete-account"),
		url('^activation/(?P<pk>\d+)/a/(?P<activation_key>[\w:-_]+)', ActivationView.as_view(), name="activation"),
		url('^user/recovery/$', UsernameRecovery.as_view(), name='username-recovery' ),
		url('^password/recovery/$', PasswordRecovery.as_view(), name='password-recovery' ),
		url('^(?P<pk>\d+)/passrecovery/$', SetNewPassword.as_view(), name='set-new-password' ),
	)

# following urls
urlpatterns += patterns('',
		url('^(?P<username>\w+)/follow/$', Follow.as_view(), name='user-follow'),
		url('^(?P<username>\w+)/stopfollow/$', StopFollow.as_view(), name='user-stop-follow'),
		url('^(?P<username>\w+)/block/$', AddBlock.as_view(), name='user-block'),
		url('^(?P<username>\w+)/removeblock/$', RemoveBlock.as_view(), name='user-remove-block'),
		url('^(?P<username>\w+)/(?P<method>(accept|reject){1})/$', ApproveFollowing.as_view(), name='user-approve'),
	)

# spins urls
urlpatterns += patterns('',
		url('^spin-it/$', CreateSpin.as_view(), name="create-spin"),
		url('^spin/edit/(?P<pk>\d+)/$', EditSpin.as_view(), name="edit-spin"),
		url('^(?P<spin_id>\d+)/delete/$', DeleteSpin.as_view(), name="delete-spin"),
		url('^(?P<spin_id>\d+)/comment/$', CommentSpin.as_view(), name='comment-spin' ),
		url('^(?P<spin_id>\d+)/respin/$', ReSpinView.as_view(), name='respin'),
		url('^(?P<pk>\d+)/details/$', DetailSpin.as_view(), name='spin'),
		url('^(?P<pk>\d+)/delete/comment/$', DeleteComment.as_view(), name='delete-comment'),
	)

# reporting urls
urlpatterns += patterns('',
	url('^report/comment/(?P<comment>\d+)$', ReportCommentView.as_view(), name='report-comment'),
	url('^report/spin/(?P<spin>\d+)$', ReportSpinView.as_view(), name='report-spin'),
	url('^report/user/(?P<userid>\d+)$', ReportUserView.as_view(), name='report-user'),
	)

# customizations urls
urlpatterns += patterns('',
	url('^customize/$', CustomizationView.as_view(), name='customize' ),
	url('^reset/customization/$', RestoreCustomization.as_view(), name='restore-customization' )
	)