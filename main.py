from automations.controllers import automation
from airtable.web_requests import *
from api.controllers import controllers
from flask import Flask
from config import IS_PROD
from dotenv import load_dotenv
import os

if not IS_PROD:
    load_dotenv()
    HOST = os.getenv('LOCAL_HOST')
else:
    HOST = os.getenv('PROD_HOST')
BASE_ID = 'appq8cXX0yFGnGtpE'
TABLE_ID = 'tbl7HmvrdL6AA6l8k'

delete_webhook(BASE_ID, 'achrKUFKbHnNF6ZHx')
print(list_webhooks(BASE_ID))

app = Flask(__name__)
app.register_blueprint(controllers)

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
