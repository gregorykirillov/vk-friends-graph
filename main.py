import matplotlib.pyplot as plt
from datetime import datetime
import networkx as nx
import asyncio
import aiohttp
import time

from helpers import Timings, PersonTypes
from helpers.remove_alone_friends import remove_alone_friends
from helpers.dumps import load_dump, save_dump

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


last_time = datetime.now()
timings = Timings.Timings()


async def get_friends(id):
    await timings.sleep()

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


async def parse_friends(persons, classmate_id, classmate_name, main_friend_id, depth=FRIENDS_DEPTH):
    print(
        f'Parsing {classmate_id}. Friend of {main_friend_id}. Persons length: {len(persons)}')
    while True:
        try:
            friendFriends = await get_friends(classmate_id)
            persons[classmate_id] = friendFriends

            personTypes.inc_normal()

            if depth > 1:
                for friend_id in friendFriends:
                    if friend_id not in persons:
                        await parse_friends(persons, friend_id, friend_id, main_friend_id, depth-1)
            break
        except VkApiException as e:
            if e.code == 6:
                print(
                    f'{classmate_name} - {e.message}. Too many requests. Sleeping for 1 second')
                time.sleep(1)
            elif e.code == 18:
                personTypes.inc_deleted()
                break
            elif e.code == 30:
                personTypes.inc_private()
                break
            else:
                print(f'{classmate_name} VK API error: {e}')
                break
    return persons


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

    plt.savefig(f'graph {datetime.now().strftime("%Y-%m-%d:%H:%M:%S")}')
    plt.show()


addedPersons = set()


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
    save_dump('buildedGraph', graph)

    end_time = datetime.now()
    print(
        f"Graph was built in {(end_time - start_time).total_seconds()} seconds. {graph}")

    return graph


personTypes = PersonTypes.PersonTypes()


async def parse():
    start_time = datetime.now()
    persons = {}
    for classmate in group_list:
        classmate_id = classmate["id"]
        classmate_name = classmate["name"]
        print(f'Parsing {classmate_name}')

        persons = await parse_friends(persons, classmate_id, classmate_name, classmate_id)
    end_time = datetime.now()
    print(
        f"Users was parsed in {(end_time - start_time).total_seconds()} seconds")

    return persons


async def main():
    persons = load_dump('persons')
    graph = load_dump('buildedGraph')

    if (len(persons) == 0):
        persons = await parse()
        save_dump('persons', persons)
        print(f'Deleted or banned persons: {personTypes.get_deleted()}')
        print(f'Private persons: {personTypes.get_private()}')
        print(f'Normal persons: {personTypes.get_normal()}')

    if (len(graph) == 0):
        graph = build_graph(graph, persons)

    graph = remove_alone_friends(graph)

    visualize(graph)


asyncio.run(main())
