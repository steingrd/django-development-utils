#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='django-development-utils',
      version='0.1',
      author='Steingrim Dovland',
      author_email='steingrd@ifi.uio.no',
      url='http://prettyprinted.net/code/django-development-utils/',
      packages=['development_utils', 
                'development_utils.management', 
                'development_utils.management.commands'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python',
                   'Topic :: Utilities'])
