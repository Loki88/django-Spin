from django.contrib import admin
from spin_base.models import UserProfile, Relationship, UserReport
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from spin_base.admin import SpinInlineAdmin, CommentUserInlineAdmin


class RelationshipAdmin(admin.TabularInline):
	'''
	TabularInline that represents the following relationship between users.
	'''
	model = Relationship
	fk_name = 'follower'
	can_delete = False
	extra = 0
	readonly_fields = ('followed', 'approved', )

	def has_add_permission(self, request):
		return False

class FromUserReportAdmin(admin.TabularInline):
	model = UserReport
	date_hierarchy = 'date'
	extra = 0
	readonly_fields = ('user', 'content', 'target_profile')
	fk_name = 'target_profile'

	def has_add_permission(self, request):
		return False


class UserProfileAdmin(admin.ModelAdmin):
	'''
	ModelAdmin class that represents the users.
	'''
	exclude = ('password',)
	# filter_horizontal = ('blocked', 'following')
	list_display = ('first_name', 'last_name', 'last_login', 'private', 'is_signaled', )
	fieldsets = (
		(_('User informations'), {
			'fields' : ( 'last_login', 'private', 'first_name', 'last_name', 'username', 'date_joined')		
			}),
		(_('User relationship'), { 
			'classes': ('wide',),
			'fields' : ('blocked',),
			}),
		(_('Other informations'), {
			'classes': ('collapse',),
			'fields': ('is_active', 'image'),
			}),
		)
	inlines = (RelationshipAdmin, SpinInlineAdmin, CommentUserInlineAdmin)
	actions = ['block_user', 'remove_block', 'make_admin']

	def block_user(modeladmin, request, queryset):
	    queryset.update(is_active=False, activation=None)
	block_user.short_description = _('Ban user')

	def remove_block(modeladmin, request, queryset):
		queryset.update(is_active=True)
	remove_block.short_description = _('Remove ban')

	def make_admin(modeladmin, request, queryset):
		queryset.update(is_staff=True, is_superuser=True)
	make_admin.short_description = _('is admin')

	def get_readonly_fields(self, request, obj=None):
		return ('date_joined', 'last_login', 'username', 'first_name', 'last_name', 'private', )


admin.site.register(UserProfile, UserProfileAdmin)