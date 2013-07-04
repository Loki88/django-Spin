from django.contrib import admin
from django.utils.translation import ugettext as _
from spin_base.models import Comment, CommentReport

class ReportedComment(Comment):
	'''
	Proxy class that permits to define two ModelAdmin for Comment model class.
	'''
	class Meta:
		proxy = True


class CommentReportAdmin(admin.StackedInline):
	'''
	StackedInline that links reports to a reported comment.
	'''
	model = CommentReport
	extra = 0
	date_hierarchy = '-date'
	readonly_fields = ['user', 'content', 'date']
	fk_name = 'target_comment'

	def has_add_permission(self, request):
		return False


class ReportedCommentAdmin(admin.ModelAdmin):
	'''
	ModelAdmin for all reported comments.
	'''
	model = Comment
	list_display = ['author', 'content', 'date', 'report_number' ]
	inlines = [CommentReportAdmin,]
	actions = ['block_author', 'remove_block',]
	

	def get_readonly_fields(self, request, obj=None):
		return ['author', 'content', 'date', ]

	def has_add_permission(self, request):
		return False

	def queryset(self, request):
		return Comment.objects.filter(reported_comment__isnull=False).exclude(author=request.user.userprofile)

	def block_author(modeladmin, request, queryset):
		for comment in queryset:
			comment.author.is_active=False
			comment.author.activation=None
			comment.author.save(update_fields=['is_active', 'activation'])
	block_author.short_description = _('Ban user')

	def remove_block(modeladmin, request, queryset):
		for comment in queryset:
			comment.author.is_active=True
			comment.author.save(update_fields=['is_active'])
	remove_block.short_description = _('Remove Ban')


admin.site.register(ReportedComment, ReportedCommentAdmin)