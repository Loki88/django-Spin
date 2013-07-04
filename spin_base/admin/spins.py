from django.contrib import admin
from django.utils.translation import ugettext as _
from spin_base.models import Spin, SpinReport
from spin_base.admin import CommentSpinInlineAdmin

class SpinInlineAdmin(admin.TabularInline):
	'''
	TabularInline that links spint to user who's submitted them.
	'''
	model = Spin
	date_hierarchy = 'date'
	fk_name = 'author'
	extra = 0
	readonly_fields = ('content', 'respinned', 'date', 'is_signaled')

	def has_add_permission(self, request):
		return False


class SpinAdmin(admin.ModelAdmin):
	'''
	ModelAdmin for spin model class.
	'''
	model = Spin
	date_hierarchy = 'date'
	inlines = (CommentSpinInlineAdmin, )
	list_display = ('author', 'content', 'date', 'is_signaled', )
	list_select_related = True


admin.site.register(Spin, SpinAdmin)