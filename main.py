from config import IS_PROD
if not IS_PROD:
    from dotenv import load_dotenv
    load_dotenv()

from automations.handlers import *
from api.controllers import controllers
from flask import Flask
import os

BASE_ID = os.getenv('BASE_ID')
TABLE_ID = os.getenv('TABLE_ID')

app = Flask(__name__)
app.register_blueprint(controllers)
app.run(host='localhost', port=3000)
