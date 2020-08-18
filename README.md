# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

### Environment Variables
Create a file named .env at the root directory with the following variables:
 * FLASK_APP=app
 * FLASK_ENV=development
 * SECRET_KEY=secret-key
 * TRELLO_API_KEY=???
 * TRELLO_API_TOKEN=???
 * TRELLO_BOARD_ID=???
 * TRELLO_BASE_URL=https://api.trello.com/1
where the variables with ??? values should be assigned appropriately.

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Running Tests

#### Test Environment Variables
Create a .env.test in the /tests directory with the same field names as the .env file, but with appropriate amendments.
#### Geckodriver
You will need to download [geckodriver v0.27.0](https://github.com/mozilla/geckodriver/releases/tag/v0.27.0), and place the geckodriver.exe file at the root directory.