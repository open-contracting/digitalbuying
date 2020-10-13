# ICT Commissioning Guidelines - Readme
-----

## Prerequisites
* Node and npm (use nvm for managing multiple node versions)
* Gulp: `npm install -g gulp`
* PostgresQL
* Python 3
* Pip

## Usage
1. Clone the repository
2. Create a blank data postgres database and update the connection details in `settings/base.py`
3. run the following commands
   `pip install dev-requirements.txt` 
   `python manage.py migrate` 
   `python manage.py createsuperuser` 
4. In a separate terminal window run `npm install` to install dependencies.
3. Run `npm run start` this will  build the frontend assets and watch for changes
3. In your original terminal window run  `python manage.py runserver` the application should now be running on and accessible at `http://localhost:8000`

## Assets
Frontend assets should be stored in the /frontend directory.
When the `npm run start` command is run it will run `npm run-script build` as a sub command which will compile assets and deploy them to `/ictcg/assets`

## Build
To build production version of the frontend assets run `npm run build`

## Linting
To run linting on CSS and JS `npm run linting`

## Deployment
The Digital Buying Guide is currently deployed on [GOVUK PaaS](https://www.cloud.service.gov.uk/)

The following environment variables should be supplied in the manifest before performing a `cf push`:
```
  ANALYTICS_ID: [UA-some-ga-token-1]
  BLOCK_SEARCH_ENGINES: (true/false)
  DJANGO_DEBUG: (true/false)
  DJANGO_SECRET_KEY: [SOME KEY]
```

The application requires a
[Postgres backing service](https://docs.cloud.service.gov.uk/deploying_services/postgresql/#set-up-a-postgresql-service)
and an
[AWS s3 backing service](https://docs.cloud.service.gov.uk/deploying_services/s3/#amazon-s3)

```
cf create-service aws-s3-bucket default [service-name] -c '{"public_bucket":true}'
cf create-service postgres [plan-name] [service-name]
```

The Postgres service can be populated from a SQL db dump
```
cf conduit [service-name] -- psql [dump-filename].sql
```

The S3 service can be populated from a local directory

First create a key:
```
cf csk [service-name] [some-key-name] -c '{"allow_external_access": true}'
cf service-key [service-name] [some-key-name]
```
Then populate your `~/.aws/credentials` file with an entry with the `aws_access_key_id` and `aws_secret_access_key`
```
# [some-key-name]
# aws_access_key_id = access-key
# aws_secret_access_key = secret-key
```

Next, using the bucket name from the `cf service-key` step above:
```
AWS_PROFILE=[some-key-name] aws s3 sync [directory] s3://[bucket-name]
```

Finally:
```
cf delete-service-key [service-name] [some-key-name]
```

## Translation
Most transations occur within the CMS itself however there are a number of words/sentences which require manual translation using the translation feature provided by Django.  

To generate the transation .po files run:
`python manage.py makemessages -i env`

After generating the .po file, add the translated content here.  
Po files can be found in the `/locale/language/LC_MESSAGES/django.po`

Once completed the file must be compiled
`python manage.py compilemessages -i env`

## Scheduled publishing

If you set up the correct periodic task, or run that task manually,
you can set a page, or group of pages to publish at a specific time.

You can dry run this task and it will print out what changes will be made:
```
cf run-task dbg-[DEPLOYMENT]-app --command "python manage.py publish_scheduled_pages --dry-run"
cf logs dbg-[DEPLOYMENT]-app
```

Otherwise running the below will trigger the changes set to have already published:
```
cf run-task dbg-[DEPLOYMENT]-app --command "python manage.py publish_scheduled_pages"
cf logs dbg-[DEPLOYMENT]-app
```

For more information on scheduling publishing this github comment is illuminating:
https://github.com/wagtail/wagtail/issues/2366#issuecomment-197605338
Or the Wagtail docs:
https://docs.wagtail.io/en/v2.0/reference/pages/theory.html#scheduled-publishing
