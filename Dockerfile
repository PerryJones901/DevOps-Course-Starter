FROM python:3.8-buster

EXPOSE 5000

# Install Poetry
# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV POETRY_VERSION=1.1.2
RUN pip install "poetry==$POETRY_VERSION"

# COPY across Config
COPY env_vars.py env_vars.py
COPY gunicorn.conf.py gunicorn.conf.py

# Update Packages
COPY pyproject.toml pyproject.toml
RUN poetry install

# COPY across app code
COPY app.py app.py
COPY /api /api
COPY /models /models
COPY /templates /templates

# Defining default execution behaviour
ENTRYPOINT poetry run gunicorn -w 4 'app:create_app()' --bind 0.0.0.0:5000 --access-logfile gunicorn.log
