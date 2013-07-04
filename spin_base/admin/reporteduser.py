from django.contrib import admin
from django.utils.translation import ugettext as _
from spin_base.models import UserProfile, UserReport
from spin_base.admin import UserProfileAdmin

class ReportedUserProfile(UserProfile):
	'''
	Proxy class that permits to define two ModelAdmin for User model class.
	'''
	class Meta:
		proxy = True

class UserReportAdmin(admin.StackedInline):
	'''
	StackedInline that links reports to a reported user.
	'''
	model = UserReport
	extra = 0
	date_hierarchy = '-date'
	readonly_fields = ['user', 'content', 'date']
	fk_name = 'target_profile'

	def has_add_permission(self, request):
		return False

class ReportedUserAdmin(UserProfileAdmin):
	'''
	ModelAdmin for all reported users.
	'''
	inlines = [UserReportAdmin,]

	def has_add_permission(self, request):
		return False

	def queryset(self, request):
		return UserProfile.objects.filter(is_active=True, reported_user__isnull=False,
			activation__isnull=False).exclude(reported_user=request.user.userprofile)


admin.site.register(ReportedUserProfile, ReportedUserAdmin)