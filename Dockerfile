FROM python:3.8-buster AS base
EXPOSE 5000

# Install Poetry
ENV POETRY_VERSION=1.1.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Update Packages
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install


FROM base AS production
# COPY across Config
COPY gunicorn.conf.py gunicorn.conf.py

# COPY across app code
COPY app.py app.py
COPY api api
COPY models models
COPY templates templates

# Defining default execution behaviour
ENTRYPOINT poetry run gunicorn -w 4 'app:create_app()' --bind 0.0.0.0:5000 --access-logfile gunicorn.log


FROM base AS development
# Poetry Run
ENTRYPOINT poetry run flask run --host 0.0.0.0
