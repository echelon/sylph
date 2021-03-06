from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.endpoint.exceptions import ProtocolErrorException
from sylph.utils.comms import django_receive

import datetime

# ================ ENDPOINT INDEX =========================

def index(request):
	"""All endpoint-related communications will be through this one
	view, which will serve to dispatch to the appropriate handler."""

	# TODO: Make endpoint dispatcher here.
	# TODO: Will need endpoint dispatching library

	# * urls.py -> (dispatch to) -> views.py
	# * tasks.py
	# * keys.py -> (dispatch to) -> api.py
		# TODO: how is this affected by diff between push/pull? 


	# TODO: For the dispatcher, consider using a similar version of what Django
	# does. Check its internals. 

	# TODO: Non-keyed dispatch based on analysis of incoming payload. 
	# TODO: analyze diff between push/pull on both ends. 


	"""
	Dispatch Key, eg.

		* send_profile
		* send_post
		* send_reply
		* request_profile
		etc


	1. Edit profile locally
	2. Signal task via celery to tell friends (or subscribers)
	3. Job does work
		state = { pending | error | recieved }

	Is django dispatch appropriate?
	"""

	# TODO: Dispatch key needs to be embedded in RDF request... I think.
	if not request.POST or 'dispatch' not in request.POST:
		print "No dispatch postdata!"
		raise ProtocolErrorException, "No dispatch postdata!" # TODO

	dispatch = request.POST['dispatch']
	if type(dispatch) == list:
		dispatch = dispatch[0]

	# TODO: I need to write an actual dispatcher!!!

	request_msg = django_receive(request)

	# ======== Node Disptaching ===========================

	print "Attempting to dispatch: %s" %dispatch # TODO DEBUG

	# TODO: PING is about to no longer rely on HTTP POST... simple GET works
	if dispatch in ['ping', 'node_ping']:
		from sylph.core.node.api import ping_response
		return ping_response(request_msg)

	if dispatch == 'node_add':
		from sylph.core.node.api import add
		return add(request_msg)

	if dispatch == 'node_delete':
		from sylph.core.node.api import delete
		return delete(request_msg)

	if dispatch == 'node_ask_to_add':
		from sylph.core.node.api import ask_to_add
		return ask_to_add(request_msg)

	# ======== User Dispatching ===========================

	if dispatch in ['user_update', 'user_pull']: # TODO
		"""Simply ask for the user's profile, updates, etc."""
		from sylph.apps.user.api import get_profile
		return get_profile(request_msg)

	if dispatch == 'user_push':
		from sylph.apps.user.api import push_profile
		return push_profile(request_msg)

	if dispatch == 'user_get': # TODO
		"""Get a user profile from the user's URI."""
		from sylph.apps.user.api import get
		return get(request_msg)

	if dispatch == 'user_get_by_node': # TODO
		"""Look up a user for a node URI."""
		from sylph.core.user.api import get_by_node
		return get_by_node(request_msg)

	return HttpResponse('TODO')

