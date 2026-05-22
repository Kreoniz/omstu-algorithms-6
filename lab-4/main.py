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
    # Лабораторная работа 4
    ## Генерация перестановок

    ### Задача 1
    Сгенерировать перестановки значений 1..n с использованием кода Грэя.

    ### Задача 2
    Сравнить алгоритмы генерации случайных перестановок.
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
    n = mo.ui.slider(2, 8, value=4, label="n")
    count = mo.ui.slider(100, 5000, step=100, value=1000, label="Количество случайных перестановок")

    mo.vstack([n, count])
    return count, n


@app.cell
def _(count, mo, n):
    mo.vstack([f"n: {n.value}", f"count: {count.value}"])
    return


@app.function(hide_code=True)
def gray_permutations(n):
    perm = list(range(1, n + 1))
    direction = [-1] * n

    result = [perm.copy()]

    while True:
        mobile_index = -1
        mobile_value = -1

        for i in range(n):
            next_i = i + direction[i]

            if 0 <= next_i < n and perm[i] > perm[next_i]:
                if perm[i] > mobile_value:
                    mobile_value = perm[i]
                    mobile_index = i

        if mobile_index == -1:
            break

        swap_i = mobile_index + direction[mobile_index]

        perm[mobile_index], perm[swap_i] = (
            perm[swap_i],
            perm[mobile_index],
        )

        direction[mobile_index], direction[swap_i] = (
            direction[swap_i],
            direction[mobile_index],
        )

        moved_value = perm[swap_i]

        for i in range(n):
            if perm[i] > moved_value:
                direction[i] *= -1

        result.append(perm.copy())

    return result


@app.cell(hide_code=True)
def _(mo, n, time):
    start = time.perf_counter()

    perms = gray_permutations(n.value)

    gray_time = time.perf_counter() - start

    mo.md(f"""
    ## Результат генерации

    Количество перестановок: **{len(perms)}**

    Время выполнения: **{gray_time:.6f} сек**
    """)
    return (perms,)


@app.cell
def _(mo, perms):
    mo.ui.table(
        [
            {
                "№": i + 1,
                "Перестановка": str(p)
            }
            for i, p in enumerate(perms)
        ]
    )
    return


@app.cell(hide_code=True)
def _(random):
    def fisher_yates(n, count):
        result = []

        for _ in range(count):
            arr = list(range(1, n + 1))

            for i in range(n - 1, 0, -1):
                j = random.randint(0, i)
                arr[i], arr[j] = arr[j], arr[i]

            result.append(arr)

        return result


    def builtin_shuffle(n, count):
        result = []

        for _ in range(count):
            arr = list(range(1, n + 1))
            random.shuffle(arr)
            result.append(arr)

        return result


    def random_sort(n, count):
        result = []

        for _ in range(count):
            arr = list(range(1, n + 1))
            arr.sort(key=lambda _: random.random())
            result.append(arr)

        return result

    return builtin_shuffle, fisher_yates, random_sort


@app.cell(hide_code=True)
def _(builtin_shuffle, count, fisher_yates, n, random_sort, time):
    def get_results():
        algorithms = {
            "Фишер-Йетс": fisher_yates,
            "random.shuffle": builtin_shuffle,
            "Случайная сортировка": random_sort,
        }
    
        results = []
    
        for name, func in algorithms.items():
    
            start = time.perf_counter()
    
            func(n.value, count.value)
    
            elapsed = time.perf_counter() - start
    
            if name == "Случайная сортировка":
                complexity = "O(k · n log n)"
            else:
                complexity = "O(k · n)"
    
            results.append({
                "Алгоритм": name,
                "Время": elapsed,
                "Сложность": complexity,
            })
    
        return results

    results = get_results()
    return (results,)


@app.cell
def _(mo, results):
    mo.ui.table(results)
    return


@app.cell
def _(plt, results):
    names = [x["Алгоритм"] for x in results]
    times = [x["Время"] for x in results]

    fig, ax = plt.subplots()

    ax.bar(names, times)

    ax.set_title("Сравнение алгоритмов")
    ax.set_xlabel("Алгоритм")
    ax.set_ylabel("Время (сек)")

    plt.xticks(rotation=10)

    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Вывод

    Алгоритм Джонсона-Троттера позволяет генерировать перестановки
    в порядке минимального изменения.

    Наиболее эффективными алгоритмами генерации случайных
    перестановок являются алгоритм Фишера-Йетса и встроенная
    функция random.shuffle.

    Метод случайной сортировки работает медленнее,
    так как использует сортировку массива.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
