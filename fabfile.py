import datetime
import os
import sys

from fabric.api import task, run, roles, cd, execute, hide, puts
from fabric.contrib.console import confirm
from fabric.operations import get, local, put
from fabric.contrib.project import rsync_project
from fabric.contrib import django

from fabconf import env, stage, live  # noqa


# hm. https://github.com/fabric/fabric/issues/256
sys.path.insert(0, sys.path[0])

# set some basic things, that are just needed.
env.forward_agent = True

# Set the default environment.
stage()

# check for some defaults to be set?
# in a method, to be called after each setup? ie at the end of stage/live?
# def check_setup():
#     if not getattr(env, 'project_name'):
#         exit("env.project_name must be set!")
# project_name
# repository
# sites
# is_postgresql
# is_nginx_gunicorn
# needs_main_nginx_files
# is_uwsgi
# remote_ref
# requirements_files
# requirements_file
# is_python3
# deploy_crontab
# roledefs
# project_dir = '/home/{main_user}/sites/{project_name}-{env_prefix}'.format(**env)
# virtualenv_dir = '{project_dir}/virtualenv'.format(**env)
# gunicorn_restart_command = '~/init/{site_name}.{env_prefix}.sh restart'
# nginx_restart_command = '~/init/nginx.sh restart'
# uwsgi_restart_command = 'touch $HOME/uwsgi.d/{site_name}.{env_prefix}.ini'
# project_conf = 'project.settings._{project_name}_{env_prefix}'.format(**env)


# ==============================================================================
# Actual tasks
# ==============================================================================


@task
@roles('web', 'db')
def create_virtualenv(force=False):
    """
    Bootstrap the environment.
    """
    with hide('running', 'stdout'):
        exists = run('if [ -d "{virtualenv_dir}" ]; then echo 1; fi'.format(**env))
    if exists:
        if not force:
            puts('Assuming virtualenv {virtualenv_dir} has already been created '
                 'since this directory exists.'
                 'If you need, you can force a recreation.'.format(**env))
            return
        else:
            run('rm -rf {virtualenv_dir}'.format(**env))
    venv_command = 'virtualenv {virtualenv_dir} --no-site-packages'.format(**env)
    if getattr(env, 'is_python3', None):
        venv_command += ' --python=python3'
    run(venv_command)
    requirements()
    puts('Created virtualenv at {virtualenv_dir}.'.format(**env))


@task
@roles('web', 'db')
def clone_repos():
    """
    clone the repository.
    """
    with hide('running', 'stdout'):
        exists = run('if [ -d "{project_dir}" ]; then echo 1; fi'.format(**env))
    if exists:
        puts('Assuming {repository} has already been cloned since '
             '{project_dir} exists.'.format(**env))
        return
    run('git clone {repository} {project_dir}'.format(**env))
    puts('cloned {repository} to {project_dir}.'.format(**env))


@task
@roles('web', 'db')
def create_database():
    # this will fail straight if the database already exists.
    if env.is_postgresql:
        puts('PostgreSQL db must be created manually.')
    else:
        create_mycnf()
        settings = _get_settings()
        db_settings = settings.DATABASES
        run("echo \"CREATE DATABASE {dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
            "\" | mysql ".format(dbname=db_settings["default"]["NAME"], )
        )


@task
@roles('web', 'db')
def bootstrap():
    clone_repos()
    create_nginx_folders()
    create_virtualenv()
    create_database()
    puts('Bootstrapped {project_name} on {host} (cloned repos, created venv and db).'.format(**env))


@task
@roles('web', 'db')
def create_nginx_folders():
    """
    do it.
    """
    if getattr(env, 'needs_main_nginx_files', None):
        with hide('running', 'stdout'):
            exists = run('if [ -d "~/nginx" ]; then echo 1; fi')
        if exists:
            puts('nginx dir already exists. manual action needed, if really...')
            return
        run('mkdir ~/nginx')
        run('mkdir ~/nginx/conf')
        run('mkdir ~/nginx/conf/sites')
        run('mkdir ~/nginx/temp')
        run('mkdir ~/nginx/logs')
        run('mkdir ~/nginx/logs/archive')
        puts('created ~/nginx & co.'.format(**env))
    else:
        puts('no nginx files created, check "needs_main_nginx_files" in env.')


@task
def deploy(verbosity='noisy'):
    """
    Full server deploy.
    Updates the repository (server-side), synchronizes the database, collects
    static files and then restarts the web service.
    """
    if verbosity == 'noisy':
        hide_args = []
    else:
        hide_args = ['running', 'stdout']
    with hide(*hide_args):
        puts('Updating repository...')
        execute(update)
        puts('Collecting static files...')
        execute(collectstatic)
        puts('Synchronizing database...')
        execute(migrate)
        puts('Restarting web server...')
        execute(restart)
        puts('Installing crontab...')
        execute(crontab)


@task
@roles('web', 'db')
def update(action='check', tag=None):
    """
    Update the repository (server-side).

    By default, if the requirements file changed in the repository then the
    requirements will be updated. Use ``action='force'`` to force
    updating requirements. Anything else other than ``'check'`` will avoid
    updating requirements at all.
    """
    with cd(env.project_dir):
        remote, dest_branch = env.remote_ref.split('/', 1)
        run('git fetch {remote}'.format(remote=remote,
                                        dest_branch=dest_branch, **env))
        with hide('running', 'stdout'):
            changed_files = run('git diff-index --cached --name-only '
                                '{remote_ref}'.format(**env)).splitlines()
        if not changed_files and action != 'force':
            # No changes, we can exit now.
            return
        reqs_changed = False
        if action == 'check':
            for file in env.requirements_files:
                if file in changed_files:
                    reqs_changed = True
                    break
        # before. run('git merge {remote_ref}'.format(**env))
        if tag:
            run('git checkout tags/{tag}'.format(tag=tag, **env))
        else:
            run('git checkout {dest_branch}'.format(dest_branch=dest_branch, **env))
            run('git pull'.format(dest_branch=dest_branch, **env))
        run('find -name "*.pyc" -delete')
        run('git clean -df')
        # run('git clean -df {project_name} docs requirements public/static '.format(**env))
        # fix_permissions()
    if action == 'force' or reqs_changed:
        # Not using execute() because we don't want to run multiple times for
        # each role (since this task gets run per role).
        requirements()


@task
@roles('web')
def crontab():
    """
    install crontab
    """
    if env.deploy_crontab:
        if getattr(env, 'contab_file', None):
            crontab_file = env.crontab_file
        else:
            crontab_file = 'deployment/crontab.txt'
        with cd(env.project_dir):
            run('crontab {}'.format(crontab_file))
    else:
        puts('not deploying crontab to %s!' % env.env_prefix)


@task
@roles('web')
def collectstatic():
    """
    Collect static files from apps and other locations in a single location.
    """
    dj('collectstatic --link --noinput')


@task
@roles('db')
def migrate(sync=True, migrate=True):
    """
    Synchronize the database.
    """
    dj('migrate --noinput')
    # needed when using django-modeltranslation
    # with third party apps
    # make it configurable?!
    # dj('sync_translation_fields')


@task
@roles('db')
def createsuperuser():
    """
    Create super user.
    """
    dj('createsuperuser')


@task
@roles('web')
def restart():
    """
    Copy gunicorn & nginx config, restart them.
    """
    if env.is_nginx_gunicorn:
        copy_restart_gunicorn()
        copy_restart_nginx()
    if env.is_uwsgi:
        copy_restart_uwsgi()
    if env.is_apache:
        exit("apache restart not implemented!")


def stop_gunicorn():
    for site_name in env.sites:
        run(env.gunicorn_stop_command.format(site_name=site_name, **env))


def copy_restart_gunicorn():
    for site in env.sites:
        run(
            'cp {project_dir}/deployment/gunicorn/{site}-{env_prefix}.sh'
            ' $HOME/init/.'.format(site=site, **env)
        )
        run('chmod u+x $HOME/init/{site}-{env_prefix}.sh'.format(site=site, **env))
        run(env.gunicorn_restart_command.format(site=site, **env))


def copy_restart_nginx():
    for site in env.sites:
        run(
            'cp {project_dir}/deployment/nginx/{site}-{env_prefix}.txt'
            ' $HOME/nginx/conf/sites/.'.format(site=site, **env)
        )
    # nginx main, may be optional!
    if env.needs_main_nginx_files:
        run('cp {project_dir}/deployment/nginx/logrotate.conf'
            ' $HOME/nginx/conf/.'.format(**env))
        run('cp {project_dir}/deployment/nginx/nginx.conf'
            ' $HOME/nginx/conf/.'.format(**env))
        run('cp {project_dir}/deployment/nginx/nginx.sh $HOME/init/.'.format(**env))
        run('chmod u+x $HOME/init/nginx.sh')
    run(env.nginx_restart_command)


def copy_restart_uwsgi():
    for site in env.sites:
        run(
            'cp {project_dir}/deployment/uwsgi/{site}-{env_prefix}.ini'
            ' $HOME/uwsgi.d/.'.format(site=site, **env)
        )
        # cp does the touch already!
        # run(env.uwsgi_restart_command.format(site=site, **env))


@task
@roles('web', 'db')
def requirements():
    """
    Update the requirements.
    """
    # let it get some more older
    # virtualenv('pip-sync {project_dir}/{requirements_file}'.format(**env))
    virtualenv('pip install -r {project_dir}/{requirements_file}'.format(**env))


@task
@roles('web')
def get_version():
    """
    Get installed version from each server.
    """
    with cd(env.project_dir):
        run('git describe --tags')
        run('git log --graph --pretty=oneline -n20')


@task
@roles('db')
def get_db(dump_only=False):
    local_db_name = _get_local_db_name()
    remote_db_name = _get_remote_db_name()
    if env.is_postgresql:
        get_db_postgresql(local_db_name, remote_db_name, dump_only, )
    else:
        get_db_mysql(local_db_name, remote_db_name, dump_only, )


@task
@roles('db')
def put_db(local_db_name=False):
    yes_no1 = confirm(
        "This will erase your remote DB! Continue?",
        default=False,
    )
    if not yes_no1:
        return
    yes_no2 = confirm("Are you sure?", default=False)
    if not yes_no2:
        return

    remote_db_name = _get_remote_db_name()
    if not local_db_name:
        local_db_name = _get_local_db_name()
    # go for it!
    if env.is_postgresql:
        put_db_postgresql(local_db_name, remote_db_name)
    else:
        put_db_mysql(local_db_name, remote_db_name)


def get_db_mysql(local_db_name, remote_db_name, dump_only=False):
    """
    dump db on server, import to local mysql (must exist)
    """
    create_mycnf()
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    dump_name = 'dump_%s_%s-%s.sql' % (env.project_name, env.env_prefix, date)
    remote_dump_file = os.path.join(env.project_dir, dump_name)
    local_dump_file = './%s' % dump_name
    run(
        'mysqldump '
        # for pg conversion!
        # ' --compatible=postgresql'
        # ' --default-character-set=utf8'
        ' {database} > {file}'.format(
            database=remote_db_name,
            file=remote_dump_file,
        )
    )
    get(remote_path=remote_dump_file, local_path=local_dump_file)
    run('rm %s' % remote_dump_file)
    if not dump_only:
        local('mysql -u root %s < %s' % (local_db_name, local_dump_file))
        local('rm %s' % local_dump_file)


def put_db_mysql(local_db_name, remote_db_name):
    """
    dump local db, import on server database (must exist)
    """
    create_mycnf()
    dump_name = 'dump_for_%s.sql' % env.env_prefix
    local_dump_file = './%s' % dump_name
    local('mysqldump --user=root {database} > {file}'.format(
        database=local_db_name,
        file=local_dump_file,
    ))
    remote_dump_file = os.path.join(env.project_dir, dump_name)
    put(remote_path=remote_dump_file, local_path=local_dump_file)
    local('rm %s' % local_dump_file)
    run('mysql {database} < {file}'.format(
        database=remote_db_name,
        file=remote_dump_file,
    ))
    run('rm %s' % remote_dump_file)


@task
@roles('db')
def create_mycnf(force=False):
    with hide('running', 'stdout'):
        exists = run('if [ -f ".my.cnf" ]; then echo 1; fi'.format(**env))
    if force or not exists:
        settings = _get_settings()
        db_settings = settings.DATABASES
        if exists:
            run('rm .my.cnf')
        local('echo "[client]" >> .my.cnf')
        local('echo "# User/PW will be sent to all standard MySQL clients" >> .my.cnf')
        local('echo "password = \"{pw}\"" >> .my.cnf'.format(pw=db_settings["default"]["PASSWORD"]))
        local('echo "user = \"{user}\"" >> .my.cnf'.format(user=db_settings["default"]["USER"]))
        put('.my.cnf')
        local('rm .my.cnf')


def get_db_postgresql(local_db_name, remote_db_name, dump_only=False):
    """
    dump db on server, import to local mysql (must exist)
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    dump_name = 'dump_%s_%s-%s.sql' % (env.project_name, env.env_prefix, date)
    remote_dump_file = os.path.join(env.project_dir, dump_name)
    local_dump_file = './%s' % dump_name
    run('pg_dump -cO {database} > {file}'.format(
        database=remote_db_name,
        file=remote_dump_file,
    ))
    get(remote_path=remote_dump_file, local_path=local_dump_file)
    run('rm %s' % remote_dump_file)
    if not dump_only:
        # local('dropdb %s_dev' % env.project_name)
        # local('createdb %s_dev' % env.project_name)
        local('psql %s < %s' % (local_db_name, local_dump_file))
        local('rm %s' % local_dump_file)


def put_db_postgresql(local_db_name, remote_db_name):
    """
    dump local db, import on server database (must exist)
    """
    if not local_db_name:
        local_db_name = env.project_name
    dump_name = 'dump_for_%s.sql' % env.env_prefix
    local_dump_file = './%s' % dump_name
    local('pg_dump -cO {database} > {file}'.format(
        database=local_db_name,
        file=local_dump_file,
    ))
    remote_dump_file = os.path.join(env.project_dir, dump_name)
    put(remote_path=remote_dump_file, local_path=local_dump_file)
    local('rm %s' % local_dump_file)
    # run('dropdb %s' % remote_db_name)
    # run('createdb %s' % remote_db_name)
    run('psql  {database} < {file}'.format(
        database=remote_db_name,
        file=remote_dump_file,
    ))
    run('rm %s' % remote_dump_file)


@task
@roles('web')
def get_media():
    """
    get media files. path by convention, adapt if needed.
    """
    # trivial version
    # get(os.path.join(env.project_dir, 'public', 'media'), 'public/media')
    if getattr(env, 'custom_media_root', None):
        remote_dir = env.custom_media_root
        if remote_dir[-1] == '/':
            # cannot end with a slash! rsync is not working!
            remote_dir = remote_dir[0:-1]
    else:
        remote_dir = os.path.join(env.project_dir, 'public', 'media', )
    local_dir = os.path.join('public')
    extra_opts = ""
    # extra_opts = "--dry-run"
    rsync_project(
        remote_dir=remote_dir,
        local_dir=local_dir,
        upload=False,
        delete=True,
        extra_opts=extra_opts,
    )


@task
@roles('web')
def put_media():
    """
    put media files. path by convention, adapt if needed.
    """
    yes_no1 = confirm(
        "Will overwrite your remote media files! Continue?",
        default=False,
    )
    if not yes_no1:
        return
    yes_no2 = confirm("Are you sure?", default=False)
    if not yes_no2:
        return

    # go for it!
    if getattr(env, 'custom_media_root', None):
        cust = env.custom_media_root
        remote_dir, to_remove = os.path.split(env.custom_media_root)
        if not to_remove:
            # custom media root ended with a slash - let's do it again!
            remote_dir, to_remove = os.path.split(cust)
    else:
        remote_dir = os.path.join(env.project_dir, 'public', )
    local_dir = os.path.join('public', 'media')
    extra_opts = ""
    # extra_opts = "--dry-run"
    rsync_project(
        remote_dir=remote_dir,
        local_dir=local_dir,
        upload=True,
        delete=True,
        extra_opts=extra_opts,
    )


# ==============================================================================
# Helper functions
# ==============================================================================

def virtualenv(command):
    """
    Run a command in the virtualenv. This prefixes the command with the source
    command.
    Usage:
        virtualenv('pip install django')
    """
    source = 'source {virtualenv_dir}/bin/activate && '.format(**env)
    run(source + command)


@task
@roles('web')
def dj(command):
    """
    Run a Django manage.py command on the server.
    """
    cmd_prefix = 'cd {project_dir}'.format(**env)
    if getattr(env, 'custom_manage_py_root', None):
        cmd_prefix = 'cd {}'.format(env.custom_manage_py_root)
    virtualenv(
        '{cmd_prefix} && ./manage.py {dj_command} --settings {project_conf}'.format(
            dj_command=command,
            cmd_prefix=cmd_prefix,
            **env
        )
    )


def fix_permissions(path='.'):
    """
    Fix the file permissions. what a hack.
    """
    puts("no need for fixing permissions yet!")
    return


def _get_settings(conf=None):
    # do this here. django settings cannot be imported more than once...probably.
    # still dont really get the mess here.
    if not conf:
        conf = env.project_conf
    django.settings_module(conf)
    from django.conf import settings
    return settings


def _get_local_db_name():
    local_db_name = getattr(env, 'local_db_name', None)
    if not local_db_name:
        local_db_name = env.project_name
    return local_db_name


def _get_remote_db_name():
    remote_db_name = getattr(env, 'remote_db_name', None)
    if not remote_db_name:
        settings = _get_settings()
        db_settings = settings.DATABASES
        remote_db_name = db_settings['default']['NAME']
    return remote_db_name
