import os

from invoke import task
from fabric import Connection


# REPO_URL = "git@github.com:jarnoln/atange-backend.git"
REPO_URL = "git@gitlab.com:jarnoln/atange-backend.git"


@task
def deploy(context, user, host):
    print("Deploying to {}@{}".format(user, host))
    # site_name = "backend.atange.com"
    site_name = host
    site_folder = "/home/{}/sites/{}".format(user, site_name)
    source_folder = os.path.join(site_folder, "source")
    virtualenv = os.path.join(site_folder, "virtualenv")
    python = virtualenv + "/bin/python"
    pip = virtualenv + "/bin/pip"
    aws_key_file_path = os.environ.get("AWS_KEY_FILE_PATH", '')
    if aws_key_file_path:
        connection = Connection(host=host, user=user, connect_kwargs={'key_filename': aws_key_file_path})
    else:
        connection = Connection(host=host, user=user)
    _create_directory_structure_if_necessary(connection, site_folder)
    _init_virtualenv(connection, site_folder)
    _get_latest_source(connection, source_folder)
    _install_virtualenv_libraries(connection, source_folder, pip)
    _check_secret_key(connection, source_folder, python)
    _update_database(connection, source_folder, python)
    _update_static_files(connection, source_folder)
    _run_remote_unit_tests(connection, source_folder, python)
    _check_settings(connection, source_folder, python)
    _restart_gunicorn(connection)
    _restart_nginx(connection)


def _create_directory_structure_if_necessary(c, site_folder):
    c.run("mkdir -p %s" % site_folder)
    for sub_folder in ("database", "log", "static", "db"):
        c.run("mkdir -p %s/%s" % (site_folder, sub_folder))
    c.run("sudo mkdir -p /var/log/gunicorn")


def _init_virtualenv(c, site_folder):
    virtualenv_path = site_folder + "/virtualenv"
    # if not exists(site_folder + '/virtualenv'):
    if c.run("test -d {}".format(virtualenv_path), warn=True).failed:
        c.run("cd {} && virtualenv --python=python3 virtualenv".format(site_folder))


def _get_latest_source(c, source_folder):
    git_folder = "{}/.git".format(source_folder)
    if c.run("test -d {}".format(git_folder), warn=True).failed:
        c.run("git clone {} {}".format(REPO_URL, source_folder))
        # Note: This may fail until cloned once manually
        c.run("cd {} && git config pull.rebase false".format(source_folder))
    else:
        c.run("cd {} && git pull origin main".format(source_folder))


def _install_virtualenv_libraries(c, source_folder, pip):
    # TODO: Check Python version. For now assume version 3.9.
    c.run("cd {} && {} install -r requirements.txt".format(source_folder, pip))
    c.run("cd {} && {} install -r requirements-server.txt".format(source_folder, pip))


def _check_secret_key(c, source_folder, python):
    settings_folder = os.path.join(source_folder, "atange")
    site_config_file = os.path.join(settings_folder, "site_config.py")
    if c.run("test -f {}".format(site_config_file), warn=True).failed:
        c.run(
            "{} {}/generate_site_config.py {}".format(
                python, settings_folder, site_config_file
            )
        )


def _update_database(c, source_folder, python):
    c.run("cd {} && {} manage.py makemigrations".format(source_folder, python))
    c.run("cd {} && {} manage.py migrate".format(source_folder, python))
    c.run(
        "cd {} && {} manage.py makemigrations collective".format(source_folder, python)
    )
    c.run("cd {} && {} manage.py migrate collective".format(source_folder, python))


def _update_static_files(c, source_folder):
    c.run(
        "cd {} && ../virtualenv/bin/python manage.py collectstatic --noinput".format(
            source_folder
        )
    )


def _run_remote_unit_tests(c, source_folder, python):
    print("*** Run remote unit tests")
    c.run(
        "cd {} && {} manage.py test --settings=atange.settings".format(
            source_folder, python
        )
    )


def _check_settings(c, source_folder, python):
    print("*** Run remote unit tests")
    c.run(
        "cd {} && {} manage.py check --deploy --settings=atange.settings".format(
            source_folder, python
        )
    )


def _restart_gunicorn(c):
    c.run("sudo systemctl restart atange.gunicorn")


def _restart_nginx(c):
    c.run("sudo service nginx restart")
