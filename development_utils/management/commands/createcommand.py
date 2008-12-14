#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

from django.core.management.base import BaseCommand

from development_utils.shared import create_package_if_not_exists, get_app_directory

COMMAND_FILE_TEMPLATE = """
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)

        print 'Command not implemented'

"""

class Command(BaseCommand):
    help = "Creates basic management command(s) for a given app"
    args = 'appname [commandname ...]'

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        
        if len(args) < 2:
            print 'Arguments missing, specify app and command name(s)'
            return

        app_name = args[0]
        command_names = args[1:]

        if not app_name in sys.modules:
            print "Skipping app '%s': not in INSTALLED_APPS" % app_name
            return

        app_directory = get_app_directory(app_name)
        commands_directory = self._create_management_structure(app_directory, verbosity)
        
        for command_name in command_names:
            self._create_command(commands_directory, command_name, verbosity)

    def _create_command(self, commands_directory, command_name, verbosity):
        if not command_name.endswith('.py'):
            command_name = command_name + '.py'
        command_filename = os.path.join(commands_directory, command_name)
        if os.path.exists(command_filename):
            if verbosity > 1:
                print "Skipping '%s': module already exists" % command_name
            return
        command_file = open(command_filename, 'w')
        command_file.write(COMMAND_FILE_TEMPLATE)
        command_file.close()

    def _create_management_structure(self, app_directory, verbosity):
        m = create_package_if_not_exists(app_directory, 'management', verbosity)
        return create_package_if_not_exists(m, 'commands', verbosity)

        
            
    
