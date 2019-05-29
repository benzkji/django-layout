# chrischiweber web

Quickstart
----------

To bootstrap the project on your machine::

    cd chrischiweber
    # check fabconf.py if env.is_python3 is true, if yes, add --python=python3
    mkvirtualenv chrischiweber 
    # without the venv-wrapper: virtualenv virtualenv chrischiweber
    # ditto: source virtualenv/chrischiweber/bin/activate
    # first time init of dependencies
    yarn install
    pip install pip-tools
    # calculates and pins and installls deps
    gulp pip-compile  
    # not first time users, install deps
    pip install -r requirements/dev.txt
    # django works
    manage.py syncdb --migrate
    manage.py createsuperuser
    manage.py runserver

To bootstrap/deploy on remote server::

    git init
    git add .
    git commit -a -m'initial'
    git add remote origin git@bitbucket.org:bnzk/{{project_name}}
    git push --set-upstream origin master

    fab bootstrap

have a look at fabfile.py

Tests
-----

If available: run `tox` command, or `./manage.py test`.
