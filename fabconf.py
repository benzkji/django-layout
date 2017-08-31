
from fabric.api import task, env


env.project_name = '{{project_name}}'
env.repository = 'git@bitbucket.org:bnzk/{project_name}.git'.format(**env)
env.sites = ('{{ project_name }}', )
env.is_postgresql = True  # False for mysql! only used for put/get_db
env.needs_main_nginx_files = True
env.is_nginx_gunicorn = True
env.is_uwsgi = False
env.remote_ref = 'origin/master'
# these will be checked for changes
env.requirements_files = ['requirements/deploy.txt', ]
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
    env.deploy_crontab = True
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
    env.deploy_crontab = False
    env.roledefs = {
        'web': [server],
        'db': [server],
    }
    generic_env_settings()


def generic_env_settings():
    if not getattr(env, 'deploy_crontab', None):
        env.deploy_crontab = False
    env.project_dir = '/home/{main_user}/sites/{project_name}-{env_prefix}'.format(**env)
    env.virtualenv_dir = '{project_dir}/virtualenv'.format(**env)
    env.gunicorn_restart_command = '~/init/{site_name}.{env_prefix}.sh restart'
    env.nginx_restart_command = '~/init/nginx.sh restart'
    env.uwsgi_restart_command = 'touch $HOME/uwsgi.d/{site_name}.{env_prefix}.ini'
    env.project_conf = 'project.settings._{project_name}_{env_prefix}'.format(**env)