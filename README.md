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

Generate password:

    python atange/generate_passwords.py cvdb/passwords.py

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

Add your host to ansible/inventory. Then:

    ansible-playbook -i ansible/inventory ansible/provision-deb.yaml
    invoke deploy --user=[your_username] --host=[your_host]
