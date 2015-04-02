.. {% comment %}

===============
Django Layout
===============

``django-layout`` provides sane defaults for new Django projects based on http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/ (more and more) and (initial version) `established best practices <http://lincolnloop.com/django-best-practices/>`__. To use ``django-layout`` run the following command::
http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/
     django-admin.py startproject --template=https://github.com/benzkji/django-layout/zipball/master --extension=py,rst,sh,txt,gitignore,ruby-version,example project_name

Things to adapt right after:

- check db settings
- check fabfile deployment settings
- chmod u+x manage.py run-local.sh

When making changes, make sure at least to check the following:

- startproject with above command line
- check that `fab bootstrap` and `fab deploy` still work
- check gunicorn/nginx configs and scripts still work

.. note:: The text following this comment block will become the README.rst of the new project.


-----

.. {% endcomment %}

{{ project_name }}
======================

Quickstart
----------

To bootstrap the project on your machine::

    cd {{ project_name }}
    mkvirtualenv --no-site-packages {{ project_name }}
    # without the venv-wrapper: virtualenv virtualenv {{ project_name }}
    # ditto: source virtualenv/{{ project_name }}/bin/activate
    pip install -r requirements/dev.txt
    manage.py syncdb --migrate

To bootstrap/deploy on remote server::

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
