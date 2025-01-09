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

.. |Build Status| image:: https://github.com/open-contracting/digitalbuying/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/open-contracting/digitalbuying/actions/workflows/ci.yml
.. |Coverage Status| image:: https://coveralls.io/repos/github/open-contracting/digitalbuying/badge.svg?branch=main
   :target: https://coveralls.io/github/open-contracting/digitalbuying?branch=main
