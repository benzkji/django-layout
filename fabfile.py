from fabric.api import task, env, run, local, roles, cd, execute, hide, puts,\
    sudo
from fabric.contrib import django as fab_django

import posixpath
import re

env.forward_agent = True
env.project_name = '{{project_name}}'
env.repository = 'git@bitbucket.org:bnzk/{project_name}.git'.format(**env)
env.local_branch = 'master'
env.remote_ref = 'origin/master'
# these will be checked for changes
env.requirements_files = ['requirements/deploy.txt', 'requirements/basics.txt', ]
# this is used with pip install -r
env.requirements_file = env.requirements_files[0]

#==============================================================================
# Tasks which set up deployment environments
#==============================================================================

@task
def live():
    """
    Use the live deployment environment.
    """
    env.env_prefix = 'live'
    server = '{project_name}@s10.wservices.ch'.format(**env)
    env.roledefs = {
        'web': [server],
        'db': [server],
    }
    env.main_user = '{project_name}'.format(**env)
    generic_env_settings()

@task
def stage():
    """
    Use the sandbox deployment environment on xy.bnzk.ch.
    """
    env.env_prefix = 'stage'
    server = '{project_name}@s19.wservices.ch'.format(**env)
    env.roledefs = {
        'web': [server],
        'db': [server],
    }
    env.main_user = '{project_name}'
    generic_env_settings()

def generic_env_settings():
    env.system_users = {"server": env.main_user} # not used yet!
    env.project_dir = '/home/{main_user}/sites/{project_name}-{env_prefix}'.format(**env)
    env.virtualenv_dir = '{project_dir}/virtualenv'.format(**env)
    env.restart_command = '~/init/{project_name}.{env_prefix}.sh restart && ~/init/nginx restart'.format(**env)
    env.project_conf = '{project_name}.settings._{env_prefix}'.format(**env)
    # set django settings on env, with fab django helper
    fab_django.settings_module(env['project_conf'])
    from django.conf import settings
    # access them, 'cause they are lazy load (I guess?! doesnt work otherwise!)
    settings.DATABASES
    env.settings = settings

# Set the default environment.
stage()



#==============================================================================
# Actual tasks
#==============================================================================

@task
@roles('web', 'db')
def create_virtualenv():
    """
    Bootstrap the environment.
    """
    with hide('running', 'stdout'):
        exists = run('if [ -d "{virtualenv_dir}" ]; then echo 1; fi'\
            .format(**env))
    if exists:
        puts('Assuming virtualenv {virtualenv_dir} has already been created '
             'since this directory exists. You\' need to manually delete this '
             'folder, if you really need to'.format(**env))
        return
    run('virtualenv {virtualenv_dir} --no-site-packages'.format(**env))
    requirements()
    puts('Created virtualenv at {virtualenv_dir}.'\
        .format(**env))

@task
@roles('web', 'db')
def clone_repos():
    """
    clone the repository.
    """
    with hide('running', 'stdout'):
        exists = run('if [ -d "{project_dir}" ]; then echo 1; fi'\
            .format(**env))
    if exists:
        puts('Assuming {repository} has already been cloned since '
            '{project_dir} exists.'.format(**env))
        return
    run('git clone {repository} {project_dir}'.format(**env))
    puts('cloned {repository} to {project_dir}.'\
        .format(**env))

@task
@roles('web', 'db')
def create_database():
    # this will fail straight if the database already exists.
    run("echo \"CREATE DATABASE {dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
        "\" | mysql -u {dbuser} --password={dbpassword}".format(
            dbuser=env.settings.DATABASES["default"]["USER"],
            dbpassword=env.settings.DATABASES["default"]["PASSWORD"],
            dbname=env.settings.DATABASES["default"]["NAME"],
        )
    )

@task
@roles('web', 'db')
def bootstrap():
    clone_repos()
    create_virtualenv()
    bootstrap_database()
    puts('Bootstrapped {project_name} on {host} - database creation needs to be done manually.'\
        .format(**env))

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
        execute(syncdb)
        puts('Restarting web server...')
        execute(restart)


@task
@roles('web', 'db')
def update(action='check'):
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
        run('git merge {remote_ref}'.format(**env))
        run('find -name "*.pyc" -delete')
        run('git clean -df')
        # run('git clean -df {project_name} docs requirements public/static deployment'.format(**env))
        #fix_permissions()
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
def syncdb(sync=True, migrate=True):
    """
    Synchronize the database.
    """
    dj('syncdb --migrate --noinput')
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
    run('cp {project_dir}/deployment/gunicorn/{project_name}.{env_prefix}.sh $HOME/init/.'.format(**env))
    run('cp {project_dir}/deployment/nginx/{project_name}.{env_prefix}.txt $HOME/nginx/conf/sites/.'.format(**env))
    run('chmod u+x $HOME/init/{project_name}.{env_prefix}.sh'.format(**env))
    run(env.restart_command)

@task
@roles('web', 'db')
def requirements():
    """
    Update the requirements.
    """
    run('{virtualenv_dir}/bin/pip install -r {project_dir}/{requirements_file}'\
        .format(**env))
    # TODO: check if this is really necessary!? keep it clean...
    #with cd('{virtualenv_dir}/src'.format(**env)):
    #    with hide('running', 'stdout', 'stderr'):
    #        dirs = []
    #        for path in run('ls -db1 -- */').splitlines():
    #            full_path = posixpath.normpath(posixpath.join(env.cwd, path))
    #            if full_path != env.project_dir:
    #                dirs.append(path)
    #    if dirs:
    #        fix_permissions(' '.join(dirs))
    #with cd(env.virtualenv_dir):
    #    with hide('running', 'stdout'):
    #        match = re.search(r'\d+\.\d+', run('bin/python --version'))
    #    if match:
    #        with cd('lib/python{0}/site-packages'.format(match.group())):
    #            fix_permissions()


#==============================================================================
# Helper functions
#==============================================================================

def virtualenv(command):
    """
    Run a command in the virtualenv. This prefixes the command with the source
    command.
    Usage:
        virtualenv('pip install django')
    """
    source = 'source {virtualenv_dir}/bin/activate && '.format(**env)
    run(source + command)


def dj(command):
    """
    Run a Django manage.py command on the server.
    """
    virtualenv('{project_dir}/manage.py {dj_command} '
               '--settings {project_conf}'.format(dj_command=command, **env))
    #run('{virtualenv_dir}/bin/manage.py {dj_command} '
    #    '--settings {project_conf}'.format(dj_command=command, **env))


def fix_permissions(path='.'):
    """
    Fix the file permissions. what a hack.
    """
    puts("no need for fixing permissions yet!")
    return



