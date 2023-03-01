# sharex-cdn
ShareX upload server written in Python using flask

## Setup
- Install all requirements using **pip install -r requirements.txt**
- Setup config found in **config/config.yaml**
- Edit **source.sql** to include your Discord ID (giving yourself admin)
- Install database files using **source source.sql**
- Setup for deploying via NGINX and Uwsgi can be found here: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04

## Notes
- This project was made as a paid product which is now updated and moved to a different language
- This project does take up physical storage and supports code (syntax highligting built-in)
- Uwsgi files and ini config is provided making it easy to host using nginx and a ubuntu service (preferred)
- This project can be hosted on cloud hosting and has been proven to work reliably, documentation for that is not provided here (a python node is needed)

