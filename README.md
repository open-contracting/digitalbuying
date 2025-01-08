# Digital Buying Guide

## Setup

```bash
createdb digitalbuyingguide
npm install
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
```

## Serve

```bash
./manage.py runserver
```

In another shell session:

```bash
npx gulp serve
```

Open http://localhost:8000

## Build static files

```bash
env NODE_ENV=production npx gulp build
./manage.py collectstatic
```

## Test

Build static files, then:

```bash
npx gulp linting
jest --verbose --coverage
./manage.py test
```

## Translate

```bash
manage.py makemessages
```

```bash
manage.py compilemessages
```

## Scheduled publishing

If you set up the correct periodic task, or run that task manually,
you can set a page, or group of pages to publish at a specific time.

You can dry run this task and it will print out what changes will be made:

```bash
manage.py publish_scheduled_pages --dry-run
```

Otherwise running the below will trigger the changes set to have already published:

```bash
manage.py publish_scheduled_pages
```

For more information on scheduling publishing this github comment is illuminating:
https://github.com/wagtail/wagtail/issues/2366#issuecomment-197605338
Or the Wagtail docs:
https://docs.wagtail.io/en/v2.0/reference/pages/theory.html#scheduled-publishing
