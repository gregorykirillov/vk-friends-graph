# vk-friends-graph

Парсинг друзей осуществлён путем отправки асинхронных запросов к VK API.

Скорость запросов в секунду настраивается в файле [config.py](https://github.com/gregorykirillov/vk-friends-graph/blob/master/config.py)

## Время

Парсинг друзей-друзей одногруппников занимает 240 секунд в дневное время с ограничением в 20 запросов в секунду.

Построение графа занимает ~21 секунду

Визуализация графа занимает ~12000 секунд

## Показатели

Размер графа - 654842 ноды и 1371382 связи.
После удаления зонтиков (людей с 1 другом):
100033 ноды и 816573 связи

## Метрики

diameter: 6
radius: 3
central_vertices: [220270939]
max_degree_centrality: 0.05094590940501347
max_proximity_centrality: 0.43510336052429754
max_eigenvector_centrality: 0.08829209780528526

![Screenshot_78](https://user-images.githubusercontent.com/33432290/227708460-3d80a7d1-2e6b-479b-bdec-a191f6086893.png)
![Screenshot_79](https://user-images.githubusercontent.com/33432290/227708469-b2fb844d-ea6e-47ff-8adb-78ee21ad2d16.png)
