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



## TOC

- [Changelog](CHANGELOG.md)
- [Versions](#versions)
- [Checklist](#checklist)
- [General Docs](#docs)
- [Quickstart / Bootstrap](#quick)
- [Tests](#tests)

## Versions <a name="versions"></a>

- Python PYTHON_VERSION 
- PostgreSQL PG_VERSION
- NODE NODE_VERSION

## Checklist <a name="checklist"></a>

### Administrative

- [ ] customer has access with own account, in panel.djangoeurope.com
- [ ] if bnzk pays hosting, it's in the support invoice, of not, it's not

### Technical

- [ ] spf / email sending checked
- [ ] project uptime monitoring setup in glitchtip.bnzk.ch
- [ ] project setup and tested in glitchtip.bnzk.ch (or sentry)
- [ ] pre-commit is setup
- [ ] project log rotation working, including complete removal of old logs
- [ ] dependencies up to date, no pip-audit complaints
- [ ] npm run watch (preferred) or gulp watch still working with current node version
- [ ] project runs with fabric_bnzk 
- [ ] project runs with supervisord
- [ ] project runs with .env files and ansible-vault (legacy projects may ignore)
- [ ] easy thumbnails with cached dimensions setup (THUMBNAIL_CACHE_DIMENSIONS = True)


## Docs & Specials <a name="docs"></a>

### XY Integration

Uses API XY. Has SDK, is a mess.


## Quickstart <a name="quick"></a>

To bootstrap the project on your machine:

    git clone
    cd {{ project_name }}
    mkvirtualenv {{ project_name }}
    # install node things, install basics like pip-tools and pre-commit
    npm install
    npm run init-dev  # installs/upgrades pip wheel setuptools pip-tools fab-classic fabric-bnzk
    # run fabric for local dependency resolution/calculation
    fab pip_compile  # fab pip_compile:true  # for upgrade mode 
    # not first time users can install deps directly:
    pip install -r requirements/dev.txt
    # django works?
    manage.py check
    manage.py migrate
    manage.py createsuperuser
    manage.py runserver

To bootstrap/deploy on remote server::

    fab bootstrap
    fab deploy

have a look at fabfile.py

## Tests <a name="tests"></a>

If available: run `tox` command, or `./manage.py test`.
