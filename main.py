import networkx as nx
import vk_api
import matplotlib.pyplot as plt
from group_list import *

from config import VK_TOKEN

# Authenticate with VK API using user credentials
vk_session = vk_api.VkApi(token=VK_TOKEN)

# Retrieve the user ID of the target user
target_user = '169871363'
response = vk_session.method('users.get', {'user_ids': target_user})

# Retrieve the list of friends/followers of the target user
response = vk_session.method('friends.get', {'user_id': target_user})

# Retrieve additional information about each friend/follower
friends = []
for friend_id in group_list:
    response = vk_session.method(
        'users.get', {'user_ids': friend_id, 'fields': 'photo_100'})
    friend_data = response[0]
    friends.append({'id': friend_data['id'], 'name': friend_data['first_name'] +
                   ' ' + friend_data['last_name'], 'photo': friend_data['photo_100']})

# Create a networkx graph object and add nodes for each friend/follower
G = nx.Graph()
for friend in friends:
    G.add_node(friend['id'], name=friend['name'], photo=friend['photo'])

# Add edges between friends/followers
for friend in friends:
    try:
        response = vk_session.method('friends.get', {'user_id': friend['id']})
        friend_friends = response['items']
        for friend_id in friend_friends:
            if friend_id in group_list:
                G.add_edge(friend['id'], friend_id)
    except:
        print(f"id {friend} is gay")

        # Draw the social graph using matplotlib
pos = nx.spring_layout(G)
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='blue', alpha=0.5)
nx.draw_networkx_edges(G, pos, alpha=0.1)
nx.draw_networkx_labels(
    G, pos, labels={node: G.nodes[node]['name'] for node in G.nodes()}, font_size=10)
plt.axis('off')
plt.show()
