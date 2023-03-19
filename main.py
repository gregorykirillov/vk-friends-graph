import asyncio
import aiohttp
import networkx as nx
import time
import matplotlib.pyplot as plt
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
    plt.figure(figsize=(12, 12))
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


personsIds = set()
persons = {}
allPeople = set()
graph = nx.Graph()


async def main():
    tasks = []
    for classmateId in group_list:
        name = await get_user_name(classmateId)
        personsIds.add(classmateId)
        allPeople.add(classmateId)
        graph.add_node(classmateId, name=name)

        while True:
            try:
                friendFriends = await get_friends(classmateId)
                persons[classmateId] = friendFriends

                for friendId in friendFriends:
                    if (friendId not in personsIds):
                        allPeople.add(friendId)
                        graph.add_node(friendId, name='')
                        graph.add_edge(classmateId, friendId)
                        personsIds.add(classmateId)
                break
            except VkApiException as e:
                if e.code == 6:
                    print(
                        f'{name} - {e.message}. Sleeping for 1 second')
                    time.sleep(1)
                else:
                    print(f'{name} VK API error: {e}')
                    break

    await asyncio.gather(*tasks)
    remove_alone_friends(graph)
    print('Building graph')
    visualize(graph)

asyncio.run(main())
