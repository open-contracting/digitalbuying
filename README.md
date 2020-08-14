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
Frontend assets can be be found in the /frontend directory.  
When running the build job the generated assets will be deployed to /ictcg/assets/

DO NOT STORE STATIC ASSETS IN /ictcg/assets/javascipts or /ictcg/assets/stylesheets.  
ALL THE FILES IN THESE DIRECTORIES WILL BE CLEAN/DELETED ON EACH BUILD AND ANY STATIC FILES WILL BE LOST.

## Build
To build production version of the frontend assets run `npm run build`

## Linting
To run linting on CSS and JS `npm run linting`

## Translation
Most transations occur within the CMS itself however there are a number of words/sentences which require manual translation using the translation feature provided by Django.  

To generate the transation .po files run:
`python manage.py makemessages -i env`

After generating the .po file, add the translated content here.  
Po files can be found in the `/locale/language/LC_MESSAGES/django.po`

Once completed the file must be compiled
`python manage.py compilemessages -i env`
