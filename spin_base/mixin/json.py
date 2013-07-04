from django.utils import simplejson
import json
from django.core import serializers
from django.utils.encoding import force_text
from django.utils.functional import curry, Promise
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

class RenderToJSon(object):

	response_class = HttpResponse
	encoder = None
	decoder = None
	load = None

	def render_to_json_response(self, context, **kwargs):
		kwargs['content_type'] = 'application/json'
		return self.response_class(self.encode_to_json(context), **kwargs)

	def encode_to_json(self, context):
		
		if isinstance(context, Promise):
			return force_text(obj)

		return simplejson.dumps(context)


class AjaxFormResponseMixin(object):
	'''
	Mixin that renders the response in Json for build-in class-based views.
	'''

	def render_to_json_response(self, context, **response_kwargs):
		'''
		Kwargs:
			context: the context object to render in json
			response_kwargs: keyword arguments to put in HttpResponse

		Returns:
			HttpResponse.
		'''
		data = simplejson.dumps(context)
		response_kwargs['content_type'] = 'application/json'
		return HttpResponse(data, **response_kwargs)

	def form_invalid(self, form):
		'''
		Method that handles an invalid form. It renders the errors.

		Args:
			form: the form object containing the errors.

		Returns:
			HttpResponse. This contains json only if the request's been made with Ajax.
		'''
		response = super(AjaxFormResponseMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return self.render_to_json_response(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):
		'''
		Method that handles a valid form. It returns a dict with primary key of object and an url to redirect.

		Args:
			form: the form object.

		Returns:
			HttpResponse.
		'''
		# We make sure to call the parent's form_valid() method because
		# it might do some processing (in the case of CreateView, it will
		# call form.save() for example).
		response = super(AjaxFormResponseMixin, self).form_valid(form)
		if self.request.is_ajax():
			try:
				data = {
					'pk': self.object.pk,
					'redirect': self.get_success_url(),
				}
			except AttributeError:
				data ={
					'redirect': self.get_success_url(),
				}
			return self.render_to_json_response(data)
		else:
			return response