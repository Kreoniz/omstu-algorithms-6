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
    # Лабораторная работа 8
    ## Жадные алгоритмы

    ### Задача о рюкзаке

    Дана последовательность элементов с заданным весом и стоимостью.
    Каждый элемент может встречаться только один раз.

    Необходимо заполнить рюкзак предметами так, чтобы суммарная стоимость была как можно большей,
    а грузоподъёмность рюкзака не превышала `W`.

    Решение выполняется двумя способами:

    1. Полный перебор
    2. Жадный алгоритм
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import random
    import time
    from itertools import combinations

    return combinations, plt, random, time


@app.cell
def _(mo):
    n_items = mo.ui.slider(3, 20, value=8, label="Количество предметов")
    capacity = mo.ui.slider(5, 100, value=35, label="Грузоподъёмность W")

    mo.vstack([n_items, capacity])
    return capacity, n_items


@app.cell
def _(capacity, mo, n_items):
    mo.vstack([f"n_items: {n_items.value}", f"W: {capacity.value}"])
    return


@app.cell(hide_code=True)
def _(random):
    def generate_items(n):
        items = []

        for i in range(1, n + 1):
            weight = random.randint(1, 20)
            price = random.randint(10, 100)

            items.append({
                "№": i,
                "Вес": weight,
                "Стоимость": price,
                "Стоимость / вес": round(price / weight, 2),
            })

        return items

    return (generate_items,)


@app.cell(hide_code=True)
def _(combinations):
    def brute_force_knapsack(items, W):
        best_set = []
        best_price = 0
        best_weight = 0

        n = len(items)

        for r in range(n + 1):
            for subset in combinations(items, r):
                total_weight = sum(item["Вес"] for item in subset)
                total_price = sum(item["Стоимость"] for item in subset)

                if total_weight <= W and total_price > best_price:
                    best_set = list(subset)
                    best_price = total_price
                    best_weight = total_weight

        return best_set, best_weight, best_price

    return (brute_force_knapsack,)


@app.function(hide_code=True)
def greedy_knapsack(items, W):
    sorted_items = sorted(
        items,
        key=lambda item: item["Стоимость / вес"],
        reverse=True
    )

    selected = []
    total_weight = 0
    total_price = 0

    for item in sorted_items:
        if total_weight + item["Вес"] <= W:
            selected.append(item)
            total_weight += item["Вес"]
            total_price += item["Стоимость"]

    return selected, total_weight, total_price


@app.cell(hide_code=True)
def _(brute_force_knapsack, capacity, generate_items, n_items, time):
    items = generate_items(n_items.value)

    start = time.perf_counter()
    brute_items, brute_weight, brute_price = brute_force_knapsack(
        items,
        capacity.value
    )
    brute_time = time.perf_counter() - start

    start = time.perf_counter()
    greedy_items, greedy_weight, greedy_price = greedy_knapsack(
        items,
        capacity.value
    )
    greedy_time = time.perf_counter() - start
    return (
        brute_items,
        brute_price,
        brute_time,
        brute_weight,
        greedy_items,
        greedy_price,
        greedy_time,
        greedy_weight,
        items,
    )


@app.cell(hide_code=True)
def _(capacity, mo, n_items):
    mo.md(f"""
    ## Исходные данные

    Грузоподъёмность рюкзака: **{capacity.value}**

    Количество предметов: **{n_items.value}**
    """)
    return


@app.cell
def _(items, mo):
    mo.ui.table(items)
    return


@app.cell(hide_code=True)
def _(brute_price, brute_time, brute_weight, mo):
    mo.md(f"""
    ## Полный перебор

    Суммарный вес: **{brute_weight}**

    Суммарная стоимость: **{brute_price}**

    Время выполнения: **{brute_time:.6f} сек**

    Сложность: **O(2ⁿ)**
    """)
    return


@app.cell
def _(brute_items, mo):
    mo.ui.table(brute_items)
    return


@app.cell(hide_code=True)
def _(greedy_price, greedy_time, greedy_weight, mo):
    mo.md(f"""
    ## Жадный алгоритм

    Суммарный вес: **{greedy_weight}**

    Суммарная стоимость: **{greedy_price}**

    Время выполнения: **{greedy_time:.6f} сек**

    Сложность: **O(n log n)**
    """)
    return


@app.cell
def _(greedy_items, mo):
    mo.ui.table(greedy_items)
    return


@app.cell
def _(
    brute_price,
    brute_time,
    brute_weight,
    greedy_price,
    greedy_time,
    greedy_weight,
    mo,
):
    comparison = [
        {
            "Метод": "Полный перебор",
            "Вес": brute_weight,
            "Стоимость": brute_price,
            "Время": brute_time,
            "Сложность": "O(2ⁿ)",
        },
        {
            "Метод": "Жадный алгоритм",
            "Вес": greedy_weight,
            "Стоимость": greedy_price,
            "Время": greedy_time,
            "Сложность": "O(n log n)",
        },
    ]

    mo.ui.table(comparison)
    return (comparison,)


@app.cell
def _(comparison, plt):
    def display_sum():
        methods = [item["Метод"] for item in comparison]
        prices = [item["Стоимость"] for item in comparison]
    
        fig, ax = plt.subplots()
    
        ax.bar(methods, prices)
    
        ax.set_title("Сравнение суммарной стоимости")
        ax.set_xlabel("Метод")
        ax.set_ylabel("Стоимость")
    
        plt.show()

    display_sum()
    return


@app.cell
def _(comparison, plt):
    def display_time():
        methods = [item["Метод"] for item in comparison]
        times = [item["Время"] for item in comparison]
    
        fig, ax = plt.subplots()
    
        ax.bar(methods, times)
    
        ax.set_title("Сравнение времени выполнения")
        ax.set_xlabel("Метод")
        ax.set_ylabel("Время, сек")
    
        plt.show()
    
    display_time()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Вывод

    В лабораторной работе была рассмотрена задача о рюкзаке.

    Полный перебор проверяет все возможные подмножества предметов, поэтому находит оптимальное решение,
    но имеет экспоненциальную сложность `O(2ⁿ)`.

    Жадный алгоритм сортирует предметы по отношению стоимости к весу и выбирает наиболее выгодные предметы,
    которые помещаются в рюкзак. Его сложность составляет `O(n log n)`.

    Жадный алгоритм работает быстрее, но не всегда гарантирует оптимальное решение для задачи о рюкзаке 0/1.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
