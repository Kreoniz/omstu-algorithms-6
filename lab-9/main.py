import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Лабораторная работа 9
    ## Жадные алгоритмы. Раскраска графа

    ### Задача 1
    Распределить работы между механизмами так, чтобы общее время выполнения всех работ было минимальным.

    ### Задача 2
    Разместить грузы по контейнерам, если некоторые грузы нельзя помещать в один контейнер.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import random
    import time

    return plt, random, time


@app.cell
def _(mo):
    n_vertices = mo.ui.slider(4, 15, value=8, label="Количество работ / грузов")
    edge_probability = mo.ui.slider(0.1, 0.8, step=0.1, value=0.3, label="Вероятность конфликта")

    mo.vstack([n_vertices, edge_probability])
    return edge_probability, n_vertices


@app.cell
def _(edge_probability, mo, n_vertices):
    mo.vstack([f"n_vertices: {n_vertices.value}", f"edge_probability: {edge_probability.value}"])
    return


@app.cell(hide_code=True)
def _(random):
    def generate_graph(n, probability):
        graph = {i: set() for i in range(1, n + 1)}

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if random.random() < probability:
                    graph[i].add(j)
                    graph[j].add(i)

        return graph

    return (generate_graph,)


@app.function(hide_code=True)
def greedy_coloring(graph):
    colors = {}

    vertices = sorted(
        graph.keys(),
        key=lambda v: len(graph[v]),
        reverse=True
    )

    for vertex in vertices:
        used_colors = {
            colors[neighbor]
            for neighbor in graph[vertex]
            if neighbor in colors
        }

        color = 1

        while color in used_colors:
            color += 1

        colors[vertex] = color

    return colors


@app.function(hide_code=True)
def graph_edges(graph):
    edges = []

    for v in graph:
        for u in graph[v]:
            if v < u:
                edges.append({
                    "Вершина 1": v,
                    "Вершина 2": u,
                })

    return edges


@app.cell(hide_code=True)
def _(edge_probability, generate_graph, n_vertices, time):
    graph = generate_graph(n_vertices.value, edge_probability.value)

    start = time.perf_counter()
    colors = greedy_coloring(graph)
    elapsed = time.perf_counter() - start

    color_count = max(colors.values()) if colors else 0
    edges = graph_edges(graph)
    return color_count, colors, edges, elapsed, graph


@app.cell(hide_code=True)
def _(color_count, edges, elapsed, mo, n_vertices):
    mo.md(f"""
    ## Граф конфликтов

    Количество вершин: **{n_vertices.value}**

    Количество конфликтов: **{len(edges)}**

    Количество цветов: **{color_count}**

    Время выполнения: **{elapsed:.6f} сек**

    Сложность алгоритма: **O(V²)** или **O(V + E)** при работе со списками смежности
    """)
    return


@app.cell(hide_code=True)
def _(edges, mo):
    mo.ui.table(edges)
    return


@app.cell(hide_code=True)
def _(colors, mo):
    coloring_table = [
        {
            "Вершина": vertex,
            "Цвет / группа": color
        }
        for vertex, color in sorted(colors.items())
    ]

    mo.ui.table(coloring_table)
    return


@app.cell(hide_code=True)
def _(colors, mo):
    works_table = [
        {
            "Работа": f"v{vertex}",
            "Номер этапа выполнения": color
        }
        for vertex, color in sorted(colors.items())
    ]

    mo.md("""
    ## Задача 1. Распределение работ между механизмами

    Работы одного цвета можно выполнять одновременно,
    потому что между ними нет конфликтов по механизмам.
    """)
    return (works_table,)


@app.cell
def _(mo, works_table):
    mo.ui.table(works_table)
    return


@app.cell(hide_code=True)
def _(colors, mo):
    containers_table = [
        {
            "Груз": f"Груз {vertex}",
            "Контейнер": color
        }
        for vertex, color in sorted(colors.items())
    ]

    mo.md("""
    ## Задача 2. Размещение грузов по контейнерам

    Грузы одного цвета можно поместить в один контейнер,
    так как между ними нет запрещённого соседства.
    """)
    return (containers_table,)


@app.cell
def _(containers_table, mo):
    mo.ui.table(containers_table)
    return


@app.cell(hide_code=True)
def _(colors, mo):
    groups = {}

    for vertex, color in colors.items():
        groups.setdefault(color, []).append(vertex)

    group_table = [
        {
            "Цвет / номер группы": color,
            "Вершины": group
        }
        for color, group in sorted(groups.items())
    ]

    mo.ui.table(group_table)
    return (groups,)


@app.cell(hide_code=True)
def _(graph, plt):
    def plot1():
        positions = {}
    
        radius = 1
    
        for i, vertex in enumerate(graph.keys()):
            angle = 2 * 3.14159 * i / len(graph)
            positions[vertex] = (
                radius * __import__("math").cos(angle),
                radius * __import__("math").sin(angle)
            )
    
        fig, ax = plt.subplots()
    
        for v in graph:
            for u in graph[v]:
                if v < u:
                    x1, y1 = positions[v]
                    x2, y2 = positions[u]
                    ax.plot([x1, x2], [y1, y2])
    
        for vertex, (x, y) in positions.items():
            ax.scatter(x, y, s=700)
            ax.text(x, y, str(vertex), ha="center", va="center")
    
        ax.set_title("Граф конфликтов")
        ax.axis("off")
    
        plt.show()

    plot1()
    return


@app.cell
def _(groups, plt):
    group_numbers = list(groups.keys())
    group_sizes = [len(groups[g]) for g in group_numbers]

    fig, ax = plt.subplots()

    ax.bar(group_numbers, group_sizes)

    ax.set_title("Количество вершин в каждой группе")
    ax.set_xlabel("Цвет / группа")
    ax.set_ylabel("Количество вершин")

    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Вывод

    В лабораторной работе была рассмотрена раскраска графа жадным алгоритмом.

    Вершины графа соответствуют работам или грузам, а рёбра обозначают конфликт:
    работы нельзя выполнять одновременно или грузы нельзя помещать в один контейнер.

    Жадный алгоритм последовательно назначает каждой вершине минимальный доступный цвет.
    В результате вершины одного цвета не соединены ребром.

    Для задачи распределения работ количество цветов соответствует минимальному найденному числу этапов выполнения.

    Для задачи размещения грузов количество цветов соответствует количеству контейнеров.

    Сложность жадной раскраски при использовании списков смежности составляет примерно `O(V + E)`,
    а с учётом сортировки вершин по степени — `O(V log V + E)`.
    """)
    return


@app.cell
def _():
    
    return


if __name__ == "__main__":
    app.run()
