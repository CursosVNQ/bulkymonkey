=============================
Bulky Monkey
=============================

A Django Project to send mass email via Mandrill

.. image:: https://raw.github.com/cursosvnq/bulkymonkey/master/assets/shot1.png

.. image:: https://raw.github.com/cursosvnq/bulkymonkey/master/assets/shot2.png

.. image:: https://raw.github.com/cursosvnq/bulkymonkey/master/assets/shot3.png

Quickstart
----------

Requirements
++++++++++++++++

.. code-block :: bash

    $ sudo apt-get install memcached nginx build-essential


Installation
++++++++++++++++

.. code-block :: bash

    $ cd yourfavdir
    $ git clone git@github.com:CursosVNQ/bulkymonkey.git
    $ cd bulkymonkey
    $ mkvirtualenv bulkymonkey
    $ pip install -r requirements.txt
    $ python bulkymonkey/manage.py syncdb


Configuration
++++++++++++++++++

BulkyMonkey uses `django-configurations` and the easiest way to configure this project is using `envdir`:

.. code-block :: bash

    $ sudo pip install envdir
    $ cd yourfavdir
    $ mkdir bulkymonkey_env
    $ cd bulkymonkey_env
    $ echo "Prod" > DJANGO_CONFIGURATION
    $ echo "mysecretkey" > DJANGO_SECRET_KEY
    $ echo "postgres://user:password@localhost/bulkymonkey" > DJANGO_DATABASE_URL
    $ echo "mandrllsecretkey" > DJANGO_MANDRILL_API_KEY


Features
--------

* Built for Django 1.6 with bleeding-edge packages
* Email campaign management (upload your emails in HTML)
* Integration with Mandrill
* Celery for background tasks
* Admin interface
