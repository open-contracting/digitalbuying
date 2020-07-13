# ICT Commissioning Guidelines - Readme
-----

## Prerequisites
* Node and npm (use nvm for managing multiple node versions)
* Gulp: `npm install -g gulp`

## Usage
1. Clone the repository.
2. Inside the directory, run `npm install` to install dependencies.
3. To begin development task, run `npm start`.

## Assets
Frontend assets can be be found in the /frontend directory.  
When running the build job the generated assets will be deployed to /ictcg/assets/

DO NOT STORE STATIC ASSETS IN /ictcg/assets/javascipts or /ictcg/assets/stylesheets.  
ALL THE FILES IN THESE DIRECTORIES WILL BE CLEAN/DELETED ON EACH BUILD AND ANY STATIC FILES WILL BE LOST.

## Build
To build production version run `npm run build`

## Linting
To run linting on CSS and JS `npm run linting`

## Translation
Most transations occur within the CMS itself however there are a number of words/sentences which require manual translation using the translation feature provided by Django.  

To generate the transation .po files run:
`python manage.py makemessages -l 'es' -i env` - Spanish being the language in this example

After generating the .po file, add the translated content here.  
Po files can be found in the `/locale/language/LC_MESSAGES/django.po`

Once completed the file must be compiled
`python manage.py compilemessages -i env`

## Deployments commands

* Private Beta / Dev (ictcg-beta-app) - uses the V2 version of the Cloud Foundry API 

cf push ictcg-beta-app

* Public beta (ictcg-public-beta-app) - uses the V3 version of the Cloud Foundry API 

cf v3-zdt-push ictcg-public-beta-app --wait-for-deploy-complete
