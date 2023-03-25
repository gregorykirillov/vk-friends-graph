from datetime import timedelta

from dotenv import dotenv_values

config = dotenv_values(".env")

VK_TOKEN = config['VK_TOKEN']
API_VERSION = 5.131
FRIENDS_DEPTH = 2

REQUESTS_PER_SECOND = 20

TIME_TO_SLEEP = 1 / REQUESTS_PER_SECOND
