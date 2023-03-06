import networkx as nx
import vk_api
import matplotlib.pyplot as plt
from group_list import *
from config import VK_TOKEN

vk = vk_api.VkApi(token=VK_TOKEN)


def get_user_name(id):
    userInfo = vk.method('users.get', {'user_ids': id})[0]
    return f"{userInfo['first_name']} {userInfo['last_name']}"


def visualize(graph):
    pos = nx.spring_layout(graph, k=0.3, iterations=50)
    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(graph, pos, node_size=50, alpha=0.5, node_color='lightblue')
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    nx.draw_networkx_labels(graph, pos, labels={node: graph.nodes[node]['name'] for node in graph.nodes()}, font_size=10)
    plt.axis('off')
    plt.show()

def remove_alone_friends(graph):
    to_remove = [node for node in graph.nodes() if graph.degree[node] == 1]
    graph.remove_nodes_from(to_remove)

personsIds = set()
persons = {}
allPeople = set()
graph = nx.Graph()


def main():
    for classmateId in group_list:
        print(f'Parsing {classmateId} classmate')
        name = get_user_name(classmateId)
        personsIds.add(classmateId)
        allPeople.add(classmateId)
        graph.add_node(classmateId, name=name)

        try:
            response = vk.method('friends.get', {'user_id': classmateId})
            friendFriends = response['items']
            persons[classmateId] = friendFriends

            for friendId in friendFriends:
                if (friendId not in personsIds):
                    allPeople.add(friendId)
                    graph.add_node(friendId, name='')
                    graph.add_edge(classmateId, friendId)
                    personsIds.add(classmateId)
        except Exception as e:
            print(f'{name} is private or deleted')
            print(e)

    remove_alone_friends(graph)
    visualize(graph)


main()
