from config import IS_PROD
if not IS_PROD:
    from dotenv import load_dotenv
    load_dotenv()
from automations.handlers import automation
import subprocess

automation.create_mapping()

if not IS_PROD:
    subprocess.run("python main.py", shell=True)
else:
    subprocess.run("python -m gunicorn main:app", shell=True)

