Digital Buying Guide
====================

|Build Status| |Coverage Status|

Setup
-----

.. code:: bash

   createdb digitalbuyingguide
   npm install
   pip install -r requirements.txt
   ./manage.py migrate
   ./manage.py createsuperuser

Serve
-----

.. code:: bash

   ./manage.py runserver

In another shell session:

.. code:: bash

   npx gulp serve

Open http://localhost:8000

Build static files
------------------

.. code:: bash

   env NODE_ENV=production npx gulp build
   ./manage.py collectstatic

Test
----

Build static files, then:

.. code:: bash

   ./manage.py test

Translate
---------

.. code:: bash

   manage.py makemessages

Scheduled publishing
--------------------

If you set up the correct periodic task, or run that task manually, you can set a page, or group of pages to publish at a specific time.

You can dry run this task and it will print out what changes will be made:

.. code:: bash

   manage.py publish_scheduled_pages --dry-run

Otherwise running the below will trigger the changes set to have already published:

.. code:: bash

   manage.py publish_scheduled_pages

For more information on scheduling publishing this github comment is illuminating: https://github.com/wagtail/wagtail/issues/2366#issuecomment-197605338 Or the Wagtail docs: https://docs.wagtail.io/en/v2.0/reference/pages/theory.html#scheduled-publishing

.. |Build Status| image:: https://github.com/open-contracting/digital-buying-guide/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/open-contracting/digital-buying-guide/actions/workflows/ci.yml
.. |Coverage Status| image:: https://coveralls.io/repos/github/open-contracting/digital-buying-guide/badge.svg?branch=main
   :target: https://coveralls.io/github/open-contracting/digital-buying-guide?branch=main
