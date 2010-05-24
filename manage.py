#!/usr/bin/env python
from django.core.management import execute_manager

try:
	import settings
except ImportError:
	import sys
	sys.stderr.write("Settings.py not found\n")
	sys.exit(1)

if __name__ == '__main__':
	execute_manager(settings)
