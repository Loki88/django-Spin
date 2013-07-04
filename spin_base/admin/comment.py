from django.contrib import admin
from django.utils.translation import ugettext as _
from spin_base.models import Report, UserReport, SpinReport, CommentReport, Comment


class CommentSpinInlineAdmin(admin.TabularInline):
	'''
	Admin TabularInline that links comments to spins into spin edit form.
	'''
	model = Comment
	date_hierarchy = 'date'
	fk_name = 'spin'
	extra = 0
	readonly_fields = ('author', 'content', 'date', 'is_signaled')

	def has_add_permission(self, request):
		return False


class CommentUserInlineAdmin(admin.TabularInline):
	'''
	Admin TabularInline that links comments to users into user edit form.
	'''
	model = Comment
	date_hierarchy = 'date'
	fk_name = 'author'
	extra = 0
	readonly_fields = ('content', 'date', 'spin', 'is_signaled')

	def has_add_permission(self, request):
		return False


class CommentAdmin(admin.ModelAdmin):
	'''
	Admin model that manages comment in admin side.
	'''
	model = Comment
	date_hierarchy = 'date'
	list_display = ('author', 'content', 'date', 'is_signaled', )
	list_select_related = True

admin.site.register(Comment, CommentAdmin)