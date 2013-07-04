from django import forms
import os
from PIL import Image
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext as _
from spin import settings
from spin_base.models import Spin, MultiSpin

class SpinForm(forms.ModelForm):
	'''
	Form that handles the fields to submit a spin.
	'''
	content_types = {'image': ('image/jpeg', 'image/gif', 'image/png', ), } #'video': ('video/mpeg', 'video/mp4', 'video/x-flv', 'video/x-ms-wmv', 'video/x-msvideo',)}
	'''
	Allowed content-types for file attached to a spin (multispin case).
	'''
	max_upload_size = 1572864
	'''
	Max upload size in byte.
	'''

	resize_width = 200 #px
	'''
	Resize width. The height is calculated from this value.
	'''

	upload_file = forms.FileField(required=False)
	'''
	Attached file.
	'''

	content = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={'rows': '4', 'cols': '5', 'class': 'spin-area', 'id': 'main-spin-area' ,'style': 'resize: none; width: 97%;'}))
	'''
	Text content in Spin
	'''


	class Meta:
		model = Spin
		exclude = ('author',)
		# widgets = {
		# 	'content' : forms.widgets.Textarea(attrs={'rows': '4', 'cols': '5', 'class': 'spin-area', 'id': 'main-spin-area' ,'style': 'resize: none; width: 97%;'}),
		# }

	class Media:
		js = ('js/spin-count.js', 'js/spin.js', )


	def clean(self):
		'''
		Cleans the submitted data.
		Raises:
			ValidationError
		'''
		cleaned = super(SpinForm, self).clean()
		# controllo sul file
		up_file = cleaned.get('upload_file', None)
		if up_file is not None:

			if up_file.size > self.max_upload_size: 
				raise forms.ValidationError( _('File size exceed the limit of %s. Current file size %s'\
					% (filesizeformat(self.max_upload_size), filesizeformat(up_file._size))))

			if up_file.content_type not in self.content_types['image'] and up_file.content_type not in self.content_types['video']:
				raise forms.ValidationError( _('Filetype not allowed'))
		return cleaned

	# def is_valid(self):
	# 	valid = super(SpinForm, self).is_valid()
	# 	if not valid:
	# 		try:
	# 			self.errors['__all__'].append(self.errors.get('content'))
	# 		except KeyError:
	# 			self.errors['__all__'] = self.errors.get('content')
	# 	return valid

	def save(self):
		'''
		Saves a Spin or a MultiSpin, handling the resize process.
		Returns:
			Spin. or MultiSpin.
		'''
	 	if self.cleaned_data.get('upload_file') is None:
	 		return super(SpinForm, self).save(commit=True)
	 	else:
	 		spin = super(SpinForm, self).save(commit=False)
	 		multi_spin = MultiSpin()
	 		multi_spin.author = spin.author
	 		multi_spin.content = spin.content
	 		multi_spin.multimedia_path = self.cleaned_data.get('upload_file')
	 		multi_spin.save()
	 		# create a resized image for multispin presentation
	 		img = Image.open(multi_spin.multimedia_path)
	 		#if img.size[0] > self.resize_width:
	 			# size[0] is the width, size[1] the height
 			resize_height = int(float(img.size[1]*self.resize_width/img.size[0]))
 			img = img.resize((self.resize_width, resize_height), Image.ANTIALIAS)
 			path = os.path.splitext(settings.MEDIA_ROOT + multi_spin.multimedia_path.name)
 			img.save(path[0] + 'resized_' + path[1], 'jpeg')
	 		return multi_spin


