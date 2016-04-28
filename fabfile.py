import os
import sys

from fabric.api import task, env, run, roles, cd, execute, hide, puts
from fabric.operations import get
from fabric.contrib import django


# hm. https://github.com/fabric/fabric/issues/256
sys.path.insert(0, sys.path[0])


env.forward_agent = True
env.project_name = '{{project_name}}'
env.repository = 'git@bitbucket.org:bnzk/{project_name}.git'.format(**env)
env.local_branch = 'master'
env.sites = ('{{ project_name }}', )
env.remote_ref = 'origin/master'
# these will be checked for changes
env.requirements_files = ['requirements/deploy.txt', 'requirements/basics.txt', ]
# this is used with pip install -r
env.requirements_file = env.requirements_files[0]


# ==============================================================================
# Tasks which set up deployment environments
# ==============================================================================

@task
def live():
    """
    Use the live deployment environment.
    """
    env.env_prefix = 'live'
    env.main_user = '{project_name}'.format(**env)
    server = '{main_user}@s20.wservices.ch'.format(**env)
    env.roledefs = {
        'web': [server],
        'db': [server],
    }
    generic_env_settings()


@task
def stage():
    """
    Use the sandbox deployment environment on xy.bnzk.ch.
    """
    env.env_prefix = 'stage'
    env.main_user = '{project_name}'.format(**env)
    server = '{main_user}@s20.wservices.ch'.format(**env)
    env.roledefs = {
        'web': [server],
        'db': [server],
    }
    generic_env_settings()


def generic_env_settings():
    env.system_users = {"server": env.main_user}  # not used yet!
    env.project_dir = '/home/{main_user}/sites/{project_name}-{env_prefix}'.format(**env)
    env.virtualenv_dir = '{project_dir}/virtualenv'.format(**env)
    env.gunicorn_restart_command = '~/init/{site_name}.{env_prefix}.sh restart'
    env.nginx_restart_command = '~/init/nginx.sh restart'
    env.uwsgi_restart_command = 'touch $HOME/uwsgi.d/{site_name}.{env_prefix}.ini'
    env.project_conf = 'project.settings._{project_name}_{env_prefix}'.format(**env)


# Set the default environment.
stage()


# ==============================================================================
# Actual tasks
# ==============================================================================

@task
@roles('web', 'db')
def create_virtualenv():
    """
    Bootstrap the environment.
    """
    with hide('running', 'stdout'):
        exists = run('if [ -d "{virtualenv_dir}" ]; then echo 1; fi'.format(**env))
    if exists:
        puts('Assuming virtualenv {virtualenv_dir} has already been created '
             'since this directory exists. You\' need to manually delete this '
             'folder, if you really need to'.format(**env))
        return
    run('virtualenv {virtualenv_dir} --no-site-packages'.format(**env))
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
    settings = get_settings()
    db_settings = settings.DATABASES
    run("echo \"CREATE DATABASE {dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
        "\" | mysql -u {dbuser} --password={dbpassword}".format(
            dbuser=db_settings["default"]["USER"],
            dbpassword=db_settings["default"]["PASSWORD"],
            dbname=db_settings["default"]["NAME"],
        ))


@task
@roles('web', 'db')
def bootstrap():
    clone_repos()
    # create_nginx_folders()  # only on request, so we dont overwrite existing settings.
    create_virtualenv()
    create_database()
    puts('Bootstrapped {project_name} on {host} (cloned repos, created venv and db).'.format(**env))


@task
@roles('web', 'db')
def create_nginx_folders():
    """
    do it.
    """
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
    puts('created ~/nginx & co.'.format(**env))


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
    copy_restart_gunicorn()
    copy_restart_nginx()
    # copy_restart_uwsgi()


def copy_restart_gunicorn():
    for site_name in env.sites:
        run(
            'cp {project_dir}/deployment/gunicorn/{site_name}.{env_prefix}.sh'
            ' $HOME/init/.'.format(site_name=site_name, **env)
        )
        run(
            'cp {project_dir}/deployment/nginx/{site_name}.{env_prefix}.txt'
            ' $HOME/nginx/conf/sites/.'.format(site_name=site_name, **env)
        )
        run('chmod u+x $HOME/init/{site_name}.{env_prefix}.sh'.format(site_name=site_name, **env))
        run(env.gunicorn_restart_command.format(site_name=site_name, **env))


def copy_restart_nginx():
    # nginx main, may be optional!
    run('cp {project_dir}/deployment/nginx/nginx.conf'
        ' $HOME/nginx/conf/.'.format(**env))
    run('cp {project_dir}/deployment/nginx/nginx.sh $HOME/init/.'.format(**env))
    run('chmod u+x $HOME/init/nginx.sh')
    run(env.nginx_restart_command)


def copy_restart_uwsgi():
    for site_name in env.sites:
        run(
            'cp {project_dir}/deployment/uwsgi/{site_name}.{env_prefix}.ini'
            ' $HOME/nginx/conf/sites/.'.format(site_name=site_name, **env)
        )
        run(env.uwsgi_restart_command.format(site_name=site_name, **env))


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
@roles('db')
def get_db():
    """
    dump db on server, import to local mysql
    """
    settings = get_settings()
    db_settings = settings.DATABASES
    dump_name = 'dump_%s.sql' % env.env_prefix
    dump_file = os.path.join(env.project_dir, dump_name)
    local_dump_file = './%s' % dump_name
    run('mysqldump --user={user} --password={password} {database} > {file}'.format(
        user= db_settings["default"]["USER"],
        password=db_settings["default"]["PASSWORD"],
        database=db_settings["default"]["NAME"],
        file=dump_file,
    ))
    get(remote_path=dump_file, local_path=local_dump_file)
    run('rm %s' % dump_file)
    local('mysql -u root %s < %s' % (env.project_name, local_dump_file))


@task
@roles('web')
def get_media():
    """
    get media files. path by convention, adapt if needed.
    """
    get(os.path.join(env.project_dir, 'public', 'media'), 'public/media')


def get_settings():
    # do this here. django settings cannot be imported more than once...probably.
    # still dont really get the mess here.
    django.settings_module(env.project_conf)
    from django.conf import settings
    return settings


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
    virtualenv('{project_dir}/manage.py {dj_command} '
               '--settings {project_conf}'.format(dj_command=command, **env))
    # run('{virtualenv_dir}/bin/manage.py {dj_command} '
    #    '--settings {project_conf}'.format(dj_command=command, **env))


def fix_permissions(path='.'):
    """
    Fix the file permissions. what a hack.
    """
    puts("no need for fixing permissions yet!")
    return
