.. {% comment %}

===============
Django Layout
===============

``django-layout`` provides sane defaults for new Django projects based on `established best practices <http://lincolnloop.com/django-best-practices/>`__. To use ``django-layout`` run the following command::

     django-admin.py startproject --template=https://github.com/lincolnloop/django-layout/zipball/master --extension=py,rst,gitignore,example project_name

.. note:: The text following this comment block will become the README.rst of the new project.

-----

.. {% endcomment %}

{{ project_name }}
======================

Quickstart
----------

To bootstrap the project on your machine:

    cd {{ project_name }}
    mkvirtualenv --no-site-packages {{ project_name }}
    # without the venv-wrapper: virtualenv virtualenv {{ project_name }}
    # ditto: source virtualenv/{{ project_name }}/bin/activate
    pip install -r requirements/dev.txt
    manage.py syncdb --migrate

To bootstrap/deploy:

    git init
    git add .
    git commit -a -m'initial'
    git add remote origin git@bitbucket.org:bnzk/{{project_name}}
    git push --set-upstream origin master

    fab bootstrap
    # after bootstrap, must manualy create db for now
    fab deploy

Documentation
-------------

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.
