Digital Buying Guide
====================

|Build Status| |Coverage Status|

Setup
-----

.. code:: bash

   mysql -u root -e "create database digitalbuying"
   pnpm install
   pip install -r requirements.txt
   ./manage.py migrate
   ./manage.py createsuperuser

Serve
-----

.. code:: bash

   ./manage.py runserver

In another shell session, rebuild the JavaScript and CSS on change:

.. code:: bash

   node build.js --watch

Open http://localhost:8000

Build static files
------------------

.. code:: bash

   env NODE_ENV=production node build.js
   ./manage.py collectstatic

Test
----

Build static files, then:

.. code:: bash

   ./manage.py test

.. |Build Status| image:: https://github.com/open-contracting/digitalbuying/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/open-contracting/digitalbuying/actions/workflows/ci.yml
.. |Coverage Status| image:: https://codecov.io/github/open-contracting/digitalbuying/graph/badge.svg
   :target: https://codecov.io/github/open-contracting/digitalbuying
