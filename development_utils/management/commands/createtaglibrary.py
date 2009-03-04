#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

from django.core.management.base import BaseCommand

from development_utils.shared import create_package_if_not_exists, get_app_directory

LIBRARY_FILE_TEMPLATE = """
from django import template

register = template.Library()

@register(name='filter_name')
def filter_name_filter(value, argument):
    return value

"""

class Command(BaseCommand):
    help = "Creates basic template library for a given app"
    args = "appname [libraryname ...]"

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)

        if len(args) < 2:
            print 'Arguments missing, specify app and tag library name(s)'
            return

        app_name = args[0]
        library_names = args[1:]

        if not app_name in sys.modules:
            print "Skipping app '%s': not in INSTALLED_APPS" % app_name
            return

        app_directory = get_app_directory(app_name)
        templatetag_directory = self._create_templatetag_structure(app_directory, verbosity)
        
        for library_name in library_names:
            self._create_library(templatetag_directory, library_name, verbosity)

    def _create_library(self, templatetag_directory, library_name, verbosity):
        if not library_name.endswith('.py'):
            library_name = library_name + '.py'
        library_filename = os.path.join(templatetag_directory, library_name)
        if os.path.exists(library_filename):
            if verbosity > 1:
                print "Skipping '%s': module already exists" % library_name
            return
        library_file = open(library_filename, 'w')
        library_file.write(LIBRARY_FILE_TEMPLATE)
        library_file.close()

    def _create_templatetag_structure(self, app_directory, verbosity):
        return create_package_if_not_exists(app_directory, 'templatetags', verbosity)

