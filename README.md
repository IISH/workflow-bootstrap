## installatie

    $ pip install --upgrade pip
    $ virtualenv p3venv
    $ ./p3venv/bin/python -m pip install --upgrade pip
    $ ./p3venv/bin/pip3 install --require-virtualenv --requirement requirements.txt

# Start in development (automatische herstart na code wijzigingen)

    $ ./p3venv/bin/python ./p3venv/bin/flask --app main.py --debug run

# Start in productie

    $ ./p3venv/bin/gunicorn --workers 1 --bind 127.0.0.1:8000 main:app