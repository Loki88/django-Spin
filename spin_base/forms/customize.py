from django import forms
from spin import settings
from spin_base.models import Customization
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core import validators
import re

class ColorInput(forms.Widget):
	'''
	Widget that displays the input for color-picker
	'''
	#attrs = {'id': 'color', 'class': 'color-pick',}

	def render(self, name, value, attrs=None):
		'''
		Returns:
			string. The html that represents the widget.
		'''
		if value is None:
			value = ''
		if attrs is not None:
			self.attrs['name'] = name
			if len(value) == 0 or value[0] != '#':
				self.attrs['value'] = '#'+value
			else:
				self.attrs['value'] = value
			return render_to_string('widgets/colorinput.html', self.attrs)
		else:
			return render_to_string('widgets/colorinput.html', {'name': name, 'value': value})


class ColorField(forms.CharField):
	'''
	Field based on ColorInput widget
	'''
	widget = ColorInput
	'''
	'''

	def to_python(self, value):
		'''
		This method catches the value from the input tag and
		returns the value in python.
		'''
		pattern = re.compile(r'^(#)?[0-9ABCDEFabcdef]{6}$')
		if value == '#':
			return ''
		elif not pattern.match(value):
			raise ValidationError('Bad color hex')
		else:
			return value[1:]


	def clean(self, value):
		return super(ColorField, self).clean(value)


class RelativeImages(forms.FilePathField):
	'''
	Form field that displays the select with background images.
	It cleans the path where the images are at, returning a relative one.
	'''

	def clean(self, value):
		'''
		'''
		super(RelativeImages, self).clean(value)
		pattern = re.compile(r'^'+settings.MEDIA_ROOT)
		return re.sub(pattern, '', value)
		


class CustomizeForm(forms.ModelForm):
	'''
	Form that handles the customization data.
	'''
	well_color = ColorField(required=False, label=_('Page box color'), widget=ColorInput(attrs={'id':'well',}))
	'''
	'''
	background_color = ColorField(required=False, widget=ColorInput(attrs={'id':'bkgr',}))
	'''
	'''
	background_image = RelativeImages(required=False, path=settings.MEDIA_ROOT+'img/custom_background/')
	'''
	'''
	class Meta:
		model = Customization

	class Media:
		css = {
			'all': ('css/farbtastic.css',),
		}
		js = ( 'js/farbtastic.js', 'js/start-picker.js', 'js/customize.js', )

	# def clean_background_image(self):

	# 	if self.cleaned_data.get('background_image') == 'blank':
	# 		self.cleaned_data['background_image'] = None
	# 	return self.cleaned_data.get('background_image')


	# def save(self, commit=True):
	# 	style = super(CustomizeForm, self).save(commit=False)

	# 	if self.cleaned_data['background_image'] is None:
	# 		del style.background_image

	# 	if commit:
	# 		style.save()
	# 	else:
	# 		return style