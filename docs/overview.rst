========================
django-development-utils
========================

django-development-utils provides simple extension commands for
developing Django projects. The commands integrate with the management
framework and are invoked using the standard ``manage.py`` script.

Tip: install Python Docutils_ and run rst2html.py on this file.

.. _Django: http://www.djangoproject.com/
.. _Docutils: http://docutils.sourceforge.net/

.. contents::

Basic use
=========

Ensure that django-development-utils is installed correctly, see
``INSTALL.rst``.

The commands in django-development-utils extend the management framework
that comes with Django. This means that you use the standard
``manage.py`` tool to invoke the commands described below. Before you
can use the commands however, you need to add ``development_utils`` to
the ``INSTALLED_APPS`` variable in ``settings.py``::

  INSTALLED_APPS = (
      # other apps

      # add this line use development_utils commands
      'development_utils',
  )

This is necessary so that Django can recognize the application commands
as extensions to ``manage.py``.

When the application is installed in your project you can invoke the
commands ``manage.py``::

  $ ./manage.py createadmin myapp

The commands are document in the next section.

Commands
========

django-development-utils comes with the following commands:

 * createadmin -- creates a skeleton ``admin.py`` module for a given
   application.

 * createapp -- creates a functional application in a specified
   directory.

 * createcommand -- creates the packages necessary for management
   commands and a command module, given an application and command name.

 * createtaglibrary -- creates the packages necessary for custom
   template tags and a template tag library, given an application and
   library name.

This section describes the parameters and the results of these commands.

createadmin
-----------

The ``createadmin`` command creates a skeleton ``admin.py`` when given
one or more application names::

  $ ./manage.py createadmin app1 app2

If app1 and app2 contains any models and does not already have an admin
module, a skeleton ``admin.py`` is created for each of the model classes
in the respective applications.

Example generated ``admin.py`` for an application with only one model
class, Article::

  from django.contrib.admin import site, ModelAdmin

  from models import Article

  class ArticleAdmin(ModelAdmin):
      pass

  site.register(Article, ArticleAdmin)


createapp
---------

The ``createapp`` command creates a functional Django application in a
specified directory. It replaces the standard ``startapp`` command but
creates a functional application with example models and views and it
adds an option to have the application created in a specified directory.

It takes a optional parameter ``--directory`` which defaults to the
current directory and one or more application names::

  $ ./manage.py createapp --directory=python/ robots

This creates an application in the directory ``python/`` (a subdirectory
of the current directory) with the following structure::

  myapp/
    __init.py__
    models.py
    views.py
    urls.py
    

createcommand
-------------

The ``createcommand`` command creates a skeleton management command
module when given an application name and one or more command names::

  $ ./manage.py createcommand myapp kill_all_humans

If necessary this creates the directory structure needed for management
commands::

  myapp/
    __init.py__
    models.py
    ... 
    management/
      __init__.py
      commands/
        __init__.py
        kill_all_humans.py

The skeleton command module created::

  from django.core.management.base import BaseCommand

  class Command(BaseCommand):
      def handle(self, *args, **options):
          verbosity = options.get('verbosity', 1)
          print 'Command not implemented'


createtaglibrary
----------------

The ``createtaglibrary`` command creates a skeleton template tag library
module when given an application name and one or more library names::

  $ ./manage.py createtaglibrary myapp myapp_tags

If necessary this creates the directory structure needed for template
tag libraries::

  myapp/
      __init__.py
      models.py
      ...
      templatetags/
          __init__.py
          myapp_tags.py

The skeleton tag library created::

  from django import template

  register = template.Library()

  @register(name='filter_name')
  def filter_name_filter(value, argument):
      return value


