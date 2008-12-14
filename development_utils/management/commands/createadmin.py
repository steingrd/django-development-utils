#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.core.management.base import AppCommand, BaseCommand
from django.db.models.loading import get_models
from django.template import Context, Template

from development_utils.shared import get_app_directory_by_app

ADMIN_FILE_TEMPLATE = """
from django.contrib.admin import site, ModelAdmin

{% for model in models %}from models import {{ model }}
{% endfor %}
{% for model in models %} 
class {{ model }}Admin(ModelAdmin):
    pass

{% endfor %}
{% for model in models %}site.register({{ model }}, {{ model }}Admin)
{% endfor %}
"""

class Command(AppCommand):
    help = "Creates admin.py for given apps"
    args = "[appname ...]"

    def handle_app(self, app, **options):
        verbosity = options.get('verbosity', 1)
        
        models = get_models(app)
        if not models:
            if verbosity > 1:
                print 'Skipping %s, could not find any models' % app.__name__
            return

        app_directory = get_app_directory_by_app(app)
        admin_directory = os.path.join(app_directory, 'admin')
        admin_filename = os.path.join(app_directory, 'admin.py')

        if os.path.exists(admin_directory) or os.path.exists(admin_filename):
            if verbosity > 0:
                print 'Skipping %s, admin module already exists' % app.__name__
            return

        if verbosity > 0:
            print 'Creating template admin.py for %s' % app.__name__

        models = [ cls.__name__ for cls in models ]

        contents = self._render_contents(models)
        admin_file = open(admin_filename, 'w')
        admin_file.write(contents)
        admin_file.close()
            
    def _render_contents(self, models):
        template = Template(ADMIN_FILE_TEMPLATE)
        return template.render(Context({ 'models' : models }))

