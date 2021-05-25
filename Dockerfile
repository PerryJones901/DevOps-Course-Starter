FROM python:3.8-buster AS base
EXPOSE 5000

ENV PORT=5000
# Install Poetry
RUN pip install poetry

WORKDIR /app

# Update Packages
COPY pyproject.toml pyproject.toml
RUN poetry install


FROM base AS production
# COPY across Config
COPY gunicorn.conf.py gunicorn.conf.py

# COPY across app code
COPY app.py app.py
COPY api api
COPY models models
COPY templates templates
COPY run-prod.sh run-prod.sh
RUN chmod +x run-prod.sh

# Defining default execution behaviour
ENTRYPOINT [ "./run-prod.sh" ]

FROM base AS development
# Poetry Run
ENTRYPOINT poetry run flask run --host 0.0.0.0


FROM base AS test
# COPY across app code
COPY app.py app.py
COPY api api
COPY models models
COPY templates templates

# COPY across test code
COPY tests tests
COPY tests_e2e tests_e2e
COPY pytest.ini pytest.ini

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
 rm /var/lib/apt/lists/* -vf &&\
 apt-get clean &&\
 apt-get update &&\
 apt-get upgrade -y &&\
 apt-get install ./chrome.deb -y &&\
 rm ./chrome.deb
# Install Chromium WebDriver
RUN echo "Installing chromium webdriver version 90.0.4430.24" &&\
 curl -sSL https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
 apt-get install unzip -y &&\
 unzip ./chromedriver_linux64.zip
ENTRYPOINT [ "poetry", "run", "pytest" ]
