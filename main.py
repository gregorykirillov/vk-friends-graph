import networkx as nx
import vk_api
import aiovk
import matplotlib.pyplot as plt
from group_list import *

from config import VK_TOKEN

vk = vk_api.VkApi(token=VK_TOKEN)


def getUserName(id):
    # userInfo = avk.users.get(user_ids=id)
    userInfo = vk.method(
        'users.get', {'user_ids': id})[0]

    return f"{userInfo['first_name']} {userInfo['last_name']}"


def visualize(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(graph, pos, node_size=50, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    nx.draw_networkx_labels(
        graph, pos, labels={node: graph.nodes[node]['name'] for node in graph.nodes()}, font_size=10)
    plt.axis('off')
    plt.show()


personsIds = []
graph = nx.Graph()


def main():
    for classmateId in group_list:
        print(111)
        name = getUserName(classmateId)
        personsIds.append(classmateId)

        graph.add_node(classmateId, name=name)

        try:
            response = vk.method(
                'friends.get', {'user_id': classmateId})
            friendFriends = response['items']

            for friendId in friendFriends:
                if (friendId not in personsIds):
                    graph.add_node(friendId, name='')
                    graph.add_edge(classmateId, friendId)
                    personsIds.append(classmateId)
        except Exception as e:
            print(f'{name} is private or deleted')
            print(e)

    visualize(graph)


main()
