import vk_api

from group_list import *
from config import VK_TOKEN


vk = vk_api.VkApi(token=VK_TOKEN)
friends_list = {}

for id in group_list:
    try:
        res = vk.method("friends.get", values={"user_id": id})
        friends_list[id] = res['items']
    except Exception as e:
        print(id, e)

print(friends_list)
