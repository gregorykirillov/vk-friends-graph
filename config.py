from dotenv import dotenv_values

config = dotenv_values(".env")

VK_TOKEN = config['VK_TOKEN']
API_VERSION = 5.131
FRIENDS_DEPTH = 2
