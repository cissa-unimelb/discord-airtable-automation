# discord-airtable-automation

Airtable integration for discord. Allows automated tasks to run based on airtable events (e.g record creation).

## Setup

### Running locally

#### Requirements:

- Python >= 3.7
- Libraries in ```requirements.txt```
- .env file containing various keys (specified below)
- Local instance of a PostgreSQL database

#### .env file

blah blah

#### Running for the first time

1. Perform all database migrations scripts under /migrations. In ```config.py```, toggle "local" flag to true to perform migrations on local database
2. Execute ```run.py```. This will start up a local flask server and create the appropriate webhooks.

**Warning**: By default, Airtable has a limit of 10 webhooks. This means local development might not be feasible as the number of automation tasks increase, since local development requires a new set of webhooks to be created. If this is the case, developers must develop directly in production environment.

### Deploying to cloud service

The project is configuered to deploy on Heroku. However, it can also be deployed on alternative cloud hosting providers. Here are a couple key points when deploying on alternative services:

- Environment must run a Linux-based OS (preferably Ubuntu, as Ubuntu has been tested to be compatible)
- Ensure the environment contains Python >= 3.7
- Install all libraries in ```requirements.txt```
- Ensure the environment allows incoming (and outgoing) HTTP/S requests
- Ensure the environment allows configuration of enviornment variables (do not use .env files in production environment)
- Configure the environment to execute ```run.py``` on start up

There also need to have a separate, production-ready instance of a PostgreSQL database set up and running.

## For developers

This section will detail how to add/remove/update automation tasks. Maintainers of this project must also read this section.

All tasks are located in ```/automation/handlers.py```.

### Adding tasks


