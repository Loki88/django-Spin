from django.contrib import admin
from django.utils.translation import ugettext as _
from spin_base.models import Spin, SpinReport

class ReportedSpin(Spin):
	'''
	Proxy class that permits to define two ModelAdmin for Spin model class.
	'''
	class Meta:
		proxy = True

class SpinReportAdmin(admin.StackedInline):
	'''
	StackedInline that links reports to a reported spin.
	'''
	model = SpinReport
	extra = 0
	date_hierarchy = '-date'
	readonly_fields = ['user', 'content', 'date']
	fk_name = 'target_spin'

	def has_add_permission(self, request):
		return False

class ReportedSpinAdmin(admin.ModelAdmin):
	'''
	ModelAdmin for all reported spins.
	'''
	model = Spin
	list_display = ('author', 'content', 'date', 'last_modified', 'report_number', )
	inlines = [SpinReportAdmin,]
	actions = ['block_author', 'remove_block',]
	

	def get_readonly_fields(self, request, obj=None):
		try:
			obj.multispin
		except:
			return ['author', 'respinned', 'content', 'date', 'last_modified']
		else:
			return ['author', 'respinned', 'content', 'date', 'last_modified', 'multimedia_path']

	def has_add_permission(self, request):
		return False

	def queryset(self, request):
		return Spin.objects.filter(reported_spin__isnull=False).exclude(
			author=request.user.userprofile)

	def block_author(modeladmin, request, queryset):
		for spin in queryset:
			spin.author.is_active=False
			spin.author.activation=None
			spin.author.save(update_fields=['is_active', 'activation'])
	block_author.short_description = _('Ban user')

	def remove_block(modeladmin, request, queryset):
		for spin in queryset:
			spin.author.is_active=True
			spin.author.save(update_fields=['is_active'])
	remove_block.short_description = _('Remove Ban')


admin.site.register(ReportedSpin, ReportedSpinAdmin)