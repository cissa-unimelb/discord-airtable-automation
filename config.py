import os

IS_PROD = os.getenv('PROD', False) == 'true'
