#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2008 by Steingrim Dovland <steingrd@ifi.uio.no>

import os, sys

def create_package(root, package_name, verbosity):
    package_directory = os.path.join(root, package_name)
    if os.path.exists(package_directory):
        if verbosity > 0:
            print "Skipping package %s, already exists" % package_directory
        return False
    os.mkdir(package_directory)
    fname = os.path.join(package_directory, '__init__.py')
    open(fname, 'w').close()
    return package_directory

def create_package_if_not_exists(root, package_name, verbosity):
    package_directory = os.path.join(root, package_name) 
    if not os.path.exists(package_directory):
        if verbosity > 1:
            print "Creating package '%s'" % package_directory
        os.mkdir(package_directory)
        fname = os.path.join(package_directory, '__init__.py')
        open(fname, 'w').close()
    return package_directory

def get_app_directory(app_name):
    module = sys.modules[app_name]
    return os.path.dirname(module.__file__)

def get_app_directory_by_app(app_object):
    return os.path.dirname(app_object.__file__)
