from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from models import *

from datetime import datetime
import hashlib


# ============ Node Index ===============================

def index(request):
	nodes = Node.objects.all()
	return render_to_response('core/node/index.html', {
									'nodes': nodes,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Edit Node ==================================

def edit_own_node(request):
	node = None
	try:
		node = Node.objects.get(pk=1)
	except Node.DoesNotExist:
		raise Http404 # TODO: This is actually a core system failure!

	class EditNodeForm(forms.ModelForm):
		"""Form for editing one's own node"""
		class Meta:
			model = Node
			fields = ['uri', # TODO: Should we let them edit URI this way?
					  'name', 'description']

	if request.method == 'POST':
		form = EditNodeForm(request.POST, instance=node)
		if form.is_valid():
			n = form.save(commit=False)
			n.datetime_edited = datetime.today()
			n.save()
			return HttpResponseRedirect('/node/view/1/')

	else:
		form = EditNodeForm(instance=node)

	return render_to_response('core/node/edit_own.html',
							  {'form': form}, 
							  context_instance=RequestContext(request))


# ============ View Node ===============================

def view_node(request, node_id):
	"""View a node status page"""
	node = None
	try:
		node = Node.objects.get(pk=node_id)
	except Node.DoesNotExist:
		raise Http404

	return render_to_response('core/node/view.html', {
									'node': node,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Add Node ===================================

#@login_required
def add_node(request):
	"""Create a new post."""
	# TODO: Try Celery to asynch request/poll the node. 

	class AddNodeForm(forms.ModelForm):
		"""Form for adding nodes"""
		class Meta:
			model = Node
			fields = ['uri', 'own_description']

	if request.method == 'POST':
		form = AddNodeForm(request.POST)
		if form.is_valid():
			node = form.save(commit=False)
			node.datetime_added = datetime.today()
			node.is_yet_to_resolve = True
			node.status = 'U'

			node.save()
			return HttpResponseRedirect('/node/')
	else:
		form = AddNodeForm()

	return render_to_response('core/node/add.html', {
								'form': form
							  }, 
							  context_instance=RequestContext(request))

