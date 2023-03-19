import matplotlib.pyplot as plt
import networkx as nx
import asyncio
import aiohttp
import time

from Exceptions.VkApiException import VkApiException

from group_list import *
from config import VK_TOKEN


async def get_user_name(id):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.vk.com/method/users.get?user_ids={id}&access_token={VK_TOKEN}&v=5.131"
        async with session.get(url) as response:
            response = await response.json()
            userInfo = response['response'][0]
            return f"{userInfo['first_name']} {userInfo['last_name']}"


async def get_friends(user_id):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.vk.com/method/friends.get?user_id={user_id}&access_token={VK_TOKEN}&v=5.131"
        async with session.get(url) as response:
            json = await response.json()

            if 'response' in json:
                jsonResponse = json['response']
                if 'items' in jsonResponse:
                    return jsonResponse['items']
                else:
                    pass
            elif 'error' in json:
                error = json['error']
                error_code = error['error_code']
                error_msg = error['error_msg']

                raise VkApiException(error_code, error_msg)


def visualize(graph):
    pos = nx.spring_layout(graph, k=0.3, iterations=50)
    plt.figure(figsize=(20, 20))
    nx.draw_networkx_nodes(graph, pos, node_size=50,
                           alpha=0.5, node_color='lightblue')
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    nx.draw_networkx_labels(graph, pos, labels={
                            node: graph.nodes[node]['name'] for node in graph.nodes()}, font_size=10)
    plt.axis('off')
    plt.show()


def remove_alone_friends(graph):
    to_remove = [node for node in graph.nodes() if graph.degree[node] == 1]
    graph.remove_nodes_from(to_remove)


persons = {}
addedPersons = set()
graph = nx.Graph()


async def parse():
    for classmate in group_list:
        classmate_id = classmate["id"]
        classname_name = classmate["name"]

        while True:
            try:
                friendFriends = await get_friends(classmate_id)
                persons[classmate_id] = friendFriends
                break
            except VkApiException as e:
                if e.code == 6:
                    print(
                        f'{classname_name} - {e.message}. Sleeping for 1 second')
                    time.sleep(1)
                else:
                    print(f'{classname_name} VK API error: {e}')
                    break


def build_graph():
    for classmate in group_list:
        classmate_id = classmate["id"]
        classmate_name = classmate["name"]

        graph.add_node(classmate_id, name=classmate_name)
        addedPersons.add(classmate_id)

        for personId in persons:
            if (personId in addedPersons):
                continue

            personFriends = persons[personId]
            for friendId in personFriends:
                if (len(personFriends) < 2):
                    continue

                if (friendId not in addedPersons):
                    graph.add_node(friendId, name='')
                graph.add_edge(personId, friendId)


async def main():
    await parse()
    build_graph()
    remove_alone_friends(graph)

    print('Visualizing graph')
    visualize(graph)


asyncio.run(main())
