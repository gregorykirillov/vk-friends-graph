import matplotlib.pyplot as plt
from datetime import datetime
import networkx as nx
import asyncio
import aiohttp
import pickle
import time

from config import FRIENDS_DEPTH
from routes import get_users_URL, get_friends_URL
from Exceptions.VkApiException import VkApiException

from group_list import *


async def get_user_name(id):
    async with aiohttp.ClientSession() as session:
        url = get_users_URL(id)
        async with session.get(url) as response:
            response = await response.json()
            userInfo = response['response'][0]
            return f"{userInfo['first_name']} {userInfo['last_name']}"


async def get_friends(id):
    async with aiohttp.ClientSession() as session:
        url = get_friends_URL(id)
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
    start_time = datetime.now()
    print(f"Visualizing graph. Size: {graph.size()}")
    pos = nx.spring_layout(graph, k=0.3, iterations=50)
    plt.figure(figsize=(20, 12))
    nx.draw_networkx_nodes(graph, pos, node_size=50,
                           alpha=0.5, node_color='lightblue')
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    # nx.draw_networkx_labels(graph, pos, labels={
    #     node: graph.nodes[node]['name'] for node in graph.nodes()}, font_size=10)
    plt.axis('off')
    end_time = datetime.now()
    print(
        f"Was visualized in {(end_time - start_time).total_seconds()} seconds")

    saveDump('visualizedGraph', graph)

    plt.show()


def build_graph(graph, persons):
    start_time = datetime.now()
    for classmate in group_list:
        classmate_id = classmate["id"]
        classmate_name = classmate["name"]
        print(classmate_name)

        graph.add_node(classmate_id, name=classmate_name)
        addedPersons.add(classmate_id)

        for personId in persons:
            if (personId in addedPersons):
                continue
            personFriends = persons[personId]
            for friendId in personFriends:
                if (friendId not in addedPersons):
                    graph.add_node(friendId, name='')
                graph.add_edge(personId, friendId)
    saveDump('buildedGraph', graph)

    end_time = datetime.now()
    print(
        f"Graph was built in {(end_time - start_time).total_seconds()} seconds. {graph}")

    return graph


def remove_alone_friends(graph):
    to_remove = [node for node in graph.nodes() if graph.degree[node] < 2]
    graph.remove_nodes_from(to_remove)

    print('After deleting with alone friends', graph)

    return graph


addedPersons = set()


def saveDump(file_name, variable):
    with open(f'{file_name}.pickle', 'wb') as f:
        pickle.dump(variable, f)


def loadDump(file_name):
    try:
        with open(f'{file_name}.pickle', 'rb') as f:
            response = pickle.load(f)
            print(f'Loading {file_name} from dump. Length: {len(response)}')

            return response
    except:
        return nx.Graph()


async def parseFriends(persons, classmate_id, classmate_name, main_friend_id, depth=FRIENDS_DEPTH):
    # print(
    #     f'Parsing friends of{classmate_id}. Friend of {main_friend_id}. Length: {len(persons)}')
    while True:
        try:
            friendFriends = await get_friends(classmate_id)
            persons[classmate_id] = friendFriends

            if depth > 1:
                for friend_id in friendFriends:
                    if friend_id not in persons:
                        await parseFriends(persons, friend_id, "", main_friend_id, depth-1)

            break
        except VkApiException as e:
            if e.code == 6:
                print(
                    f'{classmate_name} - {e.message}. Sleeping for 1 second')
                time.sleep(1)
            else:
                print(f'{classmate_name} VK API error: {e}')
                break
    return persons


async def parse():
    start_time = datetime.now()
    persons = {}
    for classmate in group_list:
        classmate_id = classmate["id"]
        classmate_name = classmate["name"]

        persons = await parseFriends(persons, classmate_id, classmate_name, classmate_id)
    end_time = datetime.now()
    print(
        f"Users was parsed in {(end_time - start_time).total_seconds()} seconds")

    return persons


async def main():
    persons = loadDump('persons')
    graph = loadDump('graph')

    if (len(persons) == 0):
        persons = await parse()
        saveDump('persons', persons)

    if (len(graph) == 0):
        graph = build_graph(graph, persons)
        graph = remove_alone_friends(graph)

    visualize(graph)


asyncio.run(main())
