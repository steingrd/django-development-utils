#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from optparse import make_option

from django.core.management.base import BaseCommand
from django.template import Context, Template

from development_utils.shared import create_package

class Command(BaseCommand):
    help = "Creates an application in a given directory"
    args = 'appname [options] [appname ...]'
    option_list = BaseCommand.option_list + (
        make_option('--directory', default='.', dest='directory',
           help='Specifies the root directory for the new app.'),
    )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        directory = options.get('directory', '.')

        for appname in args:
            target_directory = create_package(directory, appname, verbosity)
            if not target_directory:
                continue
            create_models(target_directory, appname)
            create_views(target_directory, appname)
            create_urls(target_directory, appname)
            if verbosity > 0:
                print 'Application %s created, remember to install it in INSTALLED_APPS' % appname

def create_models(directory, appname):
    template = """
from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.title
"""
    return render_to_file(template, os.path.join(directory, 'models.py'), appname)

def create_views(directory, appname):
    template = """
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse

def {{ appname }}_index(request):
    return HttpResponse('Hello, {{ appname }}')

"""
    return render_to_file(template, os.path.join(directory, 'views.py'), appname)

def create_urls(directory, appname):
    template = """
from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^$', '{{ appname }}.views.{{ appname }}_index', name='{{ appname }}_index'),
)

"""
    return render_to_file(template, os.path.join(directory, 'urls.py'), appname)

def render_to_file(template_string, target_filename, appname):
    template = Template(template_string)
    context = Context({'appname':appname})
    target_file = open(target_filename, 'w')
    target_file.write(template.render(context))
    target_file.close()
