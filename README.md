{% comment %}

# Django Layout

``django-layout`` provides sane defaults for new Django projects based on http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/ (more and more) and (initial version) `established best practices <http://lincolnloop.com/django-best-practices/>`__.

To use ``django-layout`` run the following command::

     django-admin.py startproject --template=https://github.com/benzkji/django-layout/zipball/master --extension=py,rst,md,rsh,txt,js,json,gitignore,conf your_project_name

Things to adapt right after:

- ``chmod u+x manage.py run-local.sh``
- check db settings
- check fabfile deployment settings
- check nginx site config: server_listen port
- if your project name is not equal to your system user, like /home/project_name/... does not work, further adapt nginx site config

When making changes to this repository, make sure at least to check the following:

- startproject with above command line
- `manage.py check`, `manage.py migrate`, `./run-local.sh` and open the /admin
- `fab bootstrap` and `fab deploy` still work
- gunicorn/nginx configs and scripts still work

.. note:: The text following this comment block will become the README.rst of the new project.


-----

..

{% endcomment %}
# {{ project_name }}


## Quickstart

To bootstrap the project on your machine::

    cd {{ project_name }}
    # check fabconf.py if env.is_python3 is true, if yes, add --python=python3
    mkvirtualenv {{ project_name }} 
    # without the venv-wrapper: virtualenv virtualenv {{ project_name }}
    # ditto: source virtualenv/{{ project_name }}/bin/activate
    # first time init of dependencies
    yarn install
    pip install pip-tools
    # calculates and pins and installls deps
    gulp pip-compile  
    # not first time users, install deps
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
    git push --set-upstream origin master

    fab bootstrap

have a look at fabfile.py

Tests
-----

If available: run `tox` command, or `./manage.py test`.
