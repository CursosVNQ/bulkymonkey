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
    $ export DJANGO_MANDRILL_API_KEY=yourapikey


Features
--------

* Built for Django 1.6 with bleeding-edge packages
* Email campaign management (upload your emails in HTML)
* Integration with Mandrill
* Admin interface
