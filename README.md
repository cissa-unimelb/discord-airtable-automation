
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

- ACCESS_TOKEN: Airtable API token
- BASE_ID: Airtable base ID
- DATABASE_URL: PostgreSQL DB URL
- DISCORD_GUILD_ID: Discord server guild ID
- DISCORD_TOKEN: Discord bot access token
- HOST: Host of server (The host of https://www.example.com is example.com)
- PROD: Is the application running in production (False if running locally)
- PUBLICITY_HOOK_URL: Discord webhook URL for publicity notification channel
- TABLE_ID: Airtable table ID
- UMSU_HOOK_URL: Discord webhook URL for for umsu notification channel

#### Running for the first time

1. Perform all database migrations scripts under /migrations. In ```config.py```, toggle "local" flag to true to perform migrations on local database
2. Execute ```run.py```. This will start up a local flask server and create the appropriate webhooks.

**Warning**: By default, Airtable has a limit of 10 webhooks. This means local development might not be feasible as the number of automation tasks increase, since local development requires a new set of webhooks to be created. If this is the case, developers must develop directly in production environment.

### Deploying to cloud service

The project is configured to deploy on Heroku. However, it can also be deployed on alternative cloud hosting providers. Here are a couple key points when deploying on alternative services:

- Environment must run a Linux-based OS (preferably Ubuntu, as Ubuntu has been tested to be compatible)
- Ensure the environment contains Python >= 3.7
- Install all libraries in ```requirements.txt```
- Ensure the environment allows incoming (and outgoing) HTTP/S requests
- Ensure the environment allows configuration of environment variables (do not use .env files in production environment)
- Configure the environment to execute ```run.py``` on start up

There also need to have a separate, production-ready instance of a PostgreSQL database set up and running.

## For developers

This section will detail how to add/remove/update automation tasks. Maintainers of this project must also read this section.

All tasks are located in ```/automation/handlers.py```.

### Adding tasks

Each automation task is represented via a function of type ```(webhook_id: str, payloads: [WebhookPayload]) -> None```.  The function can be thought of as a "handler" for when an automation triggers, it performs certain actions in response to the automation being triggered, receiving a list of ```WebhookPayload``` (data in a record).

In order to register an automation, use the ```Automation.automation(fields: [str], includes: [str])``` decorator. The decorator controls which fields the automation "watches" (the automation triggers if a watched field's data of a given record changes), and which auxiliary fields to include (these field data will always be included regardless if they are changed).
- ```fields``` : List of field IDs that the automation watches. For any record, if the data in any of the watched fields changes, the automation gets triggered.
- ```includes```: List of field IDs that the automation includes. Every time the automation runs, the data in these fields will always be included alongside.

Examples of existing automations can be found in ```/automation/handlers.py```. All automations must be declared in the same file (attempts to declare automations in other files will likely result in circular imports due to the way files are imported in this project).

### Modifying tasks

Existing automations can be modified directly by editing the content of its function, without modifying anything else.

If any of the watched/included fields needs to be changed (e.g automation needs to watch additional fields), the airtable wehbhook needs to be rebuilt. In order to do that, the **function name needs to be changed and it must be unique**. The service maps airtable webhooks to python functions via its name, so it'll treat any functions with a new name as a new webhook. 

### Deleting tasks

Tasks can be deleted by simply deleting its respective python function. 

## For Maintainers

This section will detail how to maintain the project and a low level overview of how the project functions. Read this section if you intend on maintaining the project long term.

### Airtable (/airtable)

Contains functionalities related to the airtable API. Functions/classes in this folder are primarily responsible for interacting with the airtable API and parsing data returned from the API. These are likely to remain unchanged unless there is a change in the airtable API itself.

#### `types.py`

Contains data types for the airtable API. Most of the types can be mapped 1 to 1 to the API's return types. 

#### `utils.py`

Contains miscellaneous functions that modifies airtable data types. 

#### `web_requests.py`

Contains functions that calls airtable's web API and parsing return values into appropriate data types.

### API (/api)

Contains functionalities related to the HTTP API of the automation.

#### `controllers.py`

Contains HTTP endpoints of the API. Also acts as handlers for airtable webhooks.

### Automations (/automations)

Contains bulk of the business logic of the application. Most of the functionalities pertaining to the actions executed in automations, registering/de-registering automations are in this folder.

#### `handlers.py`

See **For Developers** section for more details. Contains all task handlers for each airtable automation.

#### `types.py`

Contains the main `Automation` class, which is responsible for registering and de-registering airtable webhooks, and linking airtable webhooks to its respective automation handler. 

#### `utils.py`

Contains helper functions for automation task handlers.

### Discord API (/discord_api)

Contains functionalities related to the discord web API.

#### `types.py`

Contains data types for the discord API.

#### `web_requests.py`

Contains function that calls the discord web API and parses return data into its respective data types.

### Migrations (/migrations)

Contains database migrations that create/modify/delete tables on the database.
