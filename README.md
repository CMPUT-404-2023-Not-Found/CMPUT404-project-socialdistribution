CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

Contributing
============

Send a pull request and be sure to update this file with your name.

Contributors / Licensing
========================
    avahmed
    shihao8
    jx15
    marquezp
    gurveers

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma
    Nhan Nguyen 

# Dependencies

***This project was developed with WSL Ubuntu 22.04.1 LTS and Mac OS, use other OS at your discretion.***

There are 3 sections, System, Python, and UI. Each section has the explict dependencies required to use this repo.

## System

| Package               | Version   | Usage                         | Reference                                         |
| -                     | -         | -                             | -                                                 |
| heroku                | 7.68.0    | Heroku CLI                    | <https://devcenter.heroku.com/articles/heroku-cli>|
| libpq-dev             | 14.6-0    | PostgreSQL libraries          | |
| node                  | 18.14.0   | Frontend javascript engine    | <https://nodejs.org/en/>                          |
| npm                   | 9.3.1     | Node package manager          | |
| npx                   | 9.3.1     | Node package manager          | |
| nvm                   | 0.39.3    | Node version manager          | <https://github.com/nvm-sh/nvm>                   |
| pip                   | 22.0.2    | Python package manager        | |
| python3.8             | 3.8+      | Backend source code           | <https://www.python.org>                          |
| python3.8-dev         | 3.8.16    | Python Headers                | |
| python3.8-distutils   | 3.8.16    | Backend source code           | |

## Python

| Package               | Version   | Usage                                 | Reference                                         |
| -                     | -         | -                                     | -                                                 |
| django                | 3.1.6     | Backend source code                   | |
| dj-database-url       | 0.5.0     | Django database connection utility    | <https://pypi.org/project/dj-database-url/>       |
| django-cors-headers   | 3.5.0     | Django app for CORS support           | <https://pypi.org/project/django-cors-headers/>   |
| django-heroku         | 0.3.1     | Django & Heroku deployment utility    | <https://pypi.org/project/django-heroku/>         |
| djangorestframework   | 3.12.2    | Django toolkit for building Web APIs  | <https://www.django-rest-framework.org>           |
| gunicorn              | 20.0.4    | Inter web server & app communication  | <https://pypi.org/project/gunicorn/>              |
| psycopg2              | 2.8.6     | PostgreSQL database adapter           | <https://pypi.org/project/psycopg2/>              |
| psycopg2-binary       | 2.8.6     | PostgreSQL database adapter           | <https://pypi.org/project/psycopg2-binary/>       |
| python-dotenv         | 0.21.1    | Environment control                   | <https://pypi.org/project/python-dotenv/>         |
| whitenoise            | 5.2.0     | Static file web server                | <https://pypi.org/project/whitenoise/>            |

## UI

| Package               | Version   | Usage                                 | Reference                                         |
| -                     | -         | -                                     | -                                                 |
| axios                 | 0.21.0    | Javascript HTTP client                | <https://www.npmjs.com/package/axios>             |
| create-react-app      | 5.0.1     | React Boiler template engine          | <https://www.npmjs.com/package/create-react-app>  |

# Environment Setup

***This project was developed with WSL Ubuntu 22.04.1 LTS and Mac OS, use other OS at your discretion.***

Two sections are listed here: Backend & Frontend. Depending on which part of the repo you are developing, follow the appropriate steps. 
> Or be a real developer & setup both.

## Backend

After installing the System packages above, setup a *[Python venv](https://docs.python.org/3/library/venv.html)*

    virtualenv venv --python=python3.8
    source venv/bin/activate
    which python
    # You should see something like: /<a_path>/CMPUT404-project-socialdistribution/venv/bin/python

Now install the Python packages from *`requirements.txt`*
    
    pip install -r api/requirements.txt

Create a *`.env`* file and place in the *`api/`* directory. You can use the *`api/blank-env.txt`* file as a base.
> The value for SECRET_KEY can be found in our 'Discord -> resources' channel

Now try turning on the Django backend, then in your browser go to: *<http://localhost:8000>*

    python api/manage.py runserver

You should be presented with the default Django page & you are ready to begin work!

You can also try going to: *<http://localhost:8000/health>*. This is a *hello world* like page to ensure the API is working. It returns the conent of *`api/health/ver.txt`*

## Frontend

If you do not have node installed then follow these steps, or else skip to *installing node packages* steps.

Install nvm. This is a node version manager & is helpful for managing multiple isntances of node installations.

    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    exit

Open a new terminal & install the correct version of node found above in System section.

    nvm install v<VER_NUM>
    node --version
    # You should see something like: v<VER_NUM>

Now go the *`ui/`* and install the node packages.
    
    cd ui
    npm install 
    
You should end up with a *`ui/node_modules`* folder with all node packages.

Now from the *`ui/`* directory, turn on the React frontend then in your browser go to: *<http://localhost:3000>*.
    
    npm start

You should be presented with the default React page & your are ready to begin work!

# References
Rahiman M. 2020. Deploying React-Django App using Heroku. Retrieved from https://dev.to/mdrhmn/deploying-react-django-app-using-heroku-2gfa

this is a test