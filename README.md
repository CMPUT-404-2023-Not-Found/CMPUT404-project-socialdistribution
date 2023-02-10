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

## System

| Package | Version |
| - | - |
| Python | 3.8+ |
| python3.8-distutils | 3.8.16 |

## Python

| Package | Version |
| - | - |
| Django | 3.1.6 |
| python-dotenv | 0.21.1 |

## UI

| Package | Version |
| - | - |

# Environment Setup

***This project was developed with WSL Ubuntu 22.04.1 LTS and Mac OS, use other OS at your discretion.***

After installing the System packages above, setup a *[Python venv](https://docs.python.org/3/library/venv.html)*

    virtualenv venv --python=python3.8
    source venv/bin/activate
    which python
    # You should see something like: /<a_path>/CMPUT404-project-socialdistribution/venv/bin/python

Now install the Python packages from *`requirements.txt`*

    pip install -r requirements.txt

Create a *`.env`* file with the following content

    SECRET_KEY='a-really-long-key'

The value for *`SECRET_KEY`* can be found in our *Discord -> resources* channel

Now try turning on the Django backend, then in your browser go to: *<http://localhost:8000>*.

    python manage.py runserver

You should be presented with the default Django page & you are ready to begin work!
