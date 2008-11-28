#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2008 by Steingrim Dovland <steingrd@ifi.uio.no>

import os

def create_package_if_not_exists(self, root, package_name, verbosity):
    package_directory = os.path.join(root, package_name) 
    if not os.path.exists(package_directory):
        if verbosity > 1:
            print "Creating package '%s'" % package_directory
        os.mkdir(package_directory)
        fname = os.path.join(package_directory, '__init__.py')
        open(fname, 'w').close()
    return package_directory

def get_app_directory(self, app_name):
    module = sys.modules[app_name]
    return os.path.dirname(module.__file__)
