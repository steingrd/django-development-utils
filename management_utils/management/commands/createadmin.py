#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import AppCommand

ADMIN_FILE_TEMPLATE = """from django.contrib import admin
from {{ app }} import {{ models|join:", " }}

# The following classes define the admin interface for your models.
# See http://docs.djangoproject.com/en/dev/ref/contrib/admin/ for
# a full list of the options you can use in these classes.
{% for model in models %}
class {{ model }}Admin(admin.ModelAdmin):
    pass

{% endfor %}
# Each of these lines registers the admin interface for one model. If
# you don't want the admin interface for a particular model, remove
# the line which registers it.
{% for model in models %}admin.site.register({{ model }}, {{ model }}Admin)
{% endfor %}
"""

class Command(AppCommand):
    help = "Creates a basic admin.py file for the given app name(s)."
    args = '[appname ...]'

    def handle_app(self, app, **options):
        import os.path
        from django import template
        from django.db.models import get_models
        
        verbosity = options.get('verbosity', 1)
        app_name = app.__name__.split('.')[-2]
        if verbosity > 0:
           print "Handling app '%s'" % app_name
        
        models = get_models(app)
        
        if not models:
            if verbosity > 1:
                print "Skipping app '%s': no models defined in this app" % app_name
            return
        admin_filename = os.path.join(os.path.dirname(app.__file__), 'admin.py')
        if not os.path.exists(admin_filename):
            t = template.Template(ADMIN_FILE_TEMPLATE)
            c = template.Context({ 'app': app.__name__, 'models': [m._meta.object_name for m in models] })

            admin_file = open(admin_filename, 'w')
            admin_file.write(t.render(c))
            admin_file.close()
        else:
            if verbosity > 1:
                print "Skipping app '%s': admin.py file already exists" % app_name
