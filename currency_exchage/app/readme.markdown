## Configuration
The following environment variables can be set to configure the app

**DEBUG (bool)**: enable debugging. (defaults to ```True```)

**ALLOWED_HOSTS (list)**: when DEBUG=False, a list of comma separated hostnames/IPs to access the server. (defaults to [])

**SECRET_KEY (string)**: Django specific secret key used for security features.

**FIXER_ACCESS_KEY (string)**: Fixer.io Access Key (**required**)

**STATIC_ROOT (string)**: Directory where the static files wiil be copied (Production only)


## Installation
1) Create a new virtualenv

    python3 -m venv env

2) Activate it

    source env/bin/activate

3) Install requirements

    pip install -r requirements.txt

4) Either run the server or run the tests with:

    python manage.py tests

    python manage.py runserver

## Deployment
Deployment process varies from organization but these prior deployment this are some of the tasks that should be performed:

* Copy static files using

    python manage.py collecstatics

* Minimization of CSS and JS files

* Copy minified files to the webserver resource folder

* gunicorn is already installed in the environment and can be used to run the app
