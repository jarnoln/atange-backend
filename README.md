# Atange backend

[![github](https://github.com/jarnoln/atange-backend/actions/workflows/django.yml/badge.svg)](https://github.com/jarnoln/atange-backend/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/jarnoln/atange-backend/branch/main/graph/badge.svg)](https://codecov.io/gh/jarnoln/atange-backend)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Backend for Atange

Created using:
* [Django](https://www.djangoproject.com/)(4.1)
* [Django REST framework](https://www.django-rest-framework.org/)
* [djoser](https://djoser.readthedocs.io)


Install
-------

Get sources:

    git clone https://github.com/jarnoln/atange-backend.git

Create virtual environment and install Python packages:

    mkvirtualenv -p /usr/bin/python3 atange
    pip install -r requirements.txt

Generate site configuration:

    python atange/generate_site_config.py atange/site_config.py

Initialize DB:

    python manage.py migrate
    python manage.py makemigrations collective
    python manage.py migrate collective

Run tests:

    python manage.py test

Run development server:

    python manage.py runserver



Deploy
------

[Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

    pip install -r requirements-deploy.txt

Edit `ansible/inventory.example`  with your actual host information and rename it to `ansible/inventory`. Then:

    ansible-playbook -i ansible/inventory ansible/provision-deb.yaml
    invoke deploy --user=[your_username] --host=[your_host]

This will create `atange/site_config.py`-file with default values, but they need to be replaced with
actual host-specific values (especially `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`)
