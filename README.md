{% comment %}

# Django Layout

``django-layout`` provides sane defaults for new Django projects based on http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/ (more and more) and (initial version) `established best practices <http://lincolnloop.com/django-best-practices/>`__.

To use ``django-layout`` run the following command::

     django-admin startproject --template=https://github.com/benzkji/django-layout/zipball/master --extension=py,rst,md,sh,txt,js,json,gitignore,conf your_project_name

Things to adapt right after:

- create .env file, from project/env-dev-example
- check fabfile deployment settings
- check nginx site config: server_listen port

When making changes to this (django-layout) repository, make sure at least to check the following:

- startproject with above command line
- `manage.py check`, `manage.py migrate`, `./run-local.sh` and open the /admin
- `fab bootstrap` and `fab deploy` still work
- gunicorn/nginx configs and scripts still work

.. note:: The text following this comment block will become the README.rst of the new project.


-----

..

{% endcomment %}
# {{ project_name }}

Python [version], PostgreSQL [version]

## Quickstart

To bootstrap the project on your machine::

    cd {{ project_name }}
    mkvirtualenv {{ project_name }}
    # upgrade pip, setuptools and wheel, and installl basic basics, like pip-tools and pre-commit
    npm run init-dev
    # calculates and pins dependencies
    npm run pip-compile  # initial build and install dependencies  
    # not first time users can install deps directly:
    pip install -r requirements/dev.txt
    # django works?
    manage.py check
    manage.py migrate
    manage.py createsuperuser
    manage.py runserver

To bootstrap/deploy on remote server::

    git init
    git add .
    git commit -a -m'initial'
    git add remote origin ssh://git@yourgitprovider.com/org/{{project_name}}.git
    git push --set-upstream origin main

    fab bootstrap

have a look at fabfile.py

Tests
-----

If available: run `tox` command, or `./manage.py test`.
