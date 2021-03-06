from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.backend.views',
	# XXX: Index view is simply in the root urls.py

	# Reset database
	(r'reset/?$', 'reset'),

	# Process Jobs 
	# XXX: Also aliased in the root urls.py
	(r'runjobs/$', 'run_jobs'),

	# Markdown docs
	(r'about/$', 'view_about'),
	(r'readme/$', 'view_readme'),
	(r'todo/$', 'view_todo'),

	# Test pages 
	(r'test/?$', 'test'),
	(r'test2/?$', 'test2'),
)

