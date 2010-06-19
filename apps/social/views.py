from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

from models import ProfilePost
from sylph.apps.user.models import User
from sylph.utils.uri import generate_uuid


def profile_post_index(request, user_id):
	"""Show all the profile posts for a user."""
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		raise Http404

	posts = []
	try:
		posts = ProfilePost.objects.filter(for_user=user)
	except:
		pass

	return render_to_response('apps/social/profile_post/index.html', {
									'user': user,
									'posts': posts,
								},
								context_instance=RequestContext(request))

def profile_post_view(request, post_id):
	pass

def profile_post_create(request, user_id):
	"""Create a new profile post on a given user."""
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		raise Http404

	class NewProfilePostForm(forms.ModelForm):
		"""Form for creating a new profile post."""
		class Meta:
			model = ProfilePost
			fields = [
				'contents',
			]

	if request.method == 'POST':
		form = NewProfilePostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.uri = generate_uuid()
			post.for_user = user
			post.author = User.objects.get(pk=1)
			post.save()

			return HttpResponseRedirect('/user/view/%d/'%user.id)

	else:
		form = NewProfilePostForm()

	return render_to_response('apps/social/profile_post/create.html', {
									'form': form,
								},
								context_instance=RequestContext(request))

def profile_post_delete(request, post_id):
	pass

def profile_post_edit(request, post_id):
	pass


