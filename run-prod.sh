#!/bin/bash
set -ev

poetry install
poetry run gunicorn -w 4 'app:create_app()' --bind 0.0.0.0:$PORT --access-logfile gunicorn.log