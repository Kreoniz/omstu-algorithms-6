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
    # Лабораторная работа 6
    ## Жадные алгоритмы

    ### Задача 1
    На прямой даны `n` отрезков. Нужно выбрать максимальное по размеру подмножество непересекающихся.

    ### Задача 2
    Для аудитории есть заявки с временем начала и окончания работы. Нужно вернуть максимальное количество допустимых заявок.

    ### Задача 3
    Даны отрезки `[li, ri]`, которые покрывают интервал `[L, R]`. Нужно выбрать наименьшее множество отрезков, чтобы они всё ещё покрывали интервал.
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
    n_segments = mo.ui.slider(5, 50, value=15, label="Количество отрезков")
    left_limit = mo.ui.slider(0, 20, value=0, label="L")
    right_limit = mo.ui.slider(20, 100, value=50, label="R")

    mo.vstack([n_segments, left_limit, right_limit])
    return left_limit, n_segments, right_limit


@app.cell
def _(left_limit, mo, n_segments, right_limit):
    mo.vstack([f"n_segments: {n_segments.value}", f"L: {left_limit.value}", f"R: {right_limit.value}"])
    return


@app.cell(hide_code=True)
def _(random):
    def generate_segments(n, L, R):
        segments = []

        for i in range(n):
            a = random.randint(L, R - 1)
            b = random.randint(a + 1, R)

            segments.append({
                "№": i + 1,
                "Начало": a,
                "Конец": b,
            })

        return segments

    return (generate_segments,)


@app.function(hide_code=True)
def max_non_overlapping_segments(segments, allow_touch=True):
    """
    Выбирает максимальное количество непересекающихся интервалов.

    allow_touch=True:
        [1, 3] и [3, 5] считаются совместимыми.
        Это обычно подходит для расписаний.

    allow_touch=False:
        [1, 3] и [3, 5] считаются пересекающимися,
        потому что имеют общую точку 3.
    """

    sorted_segments = sorted(segments, key=lambda x: x["Конец"])

    result = []
    current_end = float("-inf")

    for segment in sorted_segments:
        if allow_touch:
            can_take = segment["Начало"] >= current_end
        else:
            can_take = segment["Начало"] > current_end

        if can_take:
            result.append(segment)
            current_end = segment["Конец"]

    return result


@app.function(hide_code=True)
def max_requests(requests):
    sorted_requests = sorted(requests, key=lambda x: x["Конец"])

    result = []
    current_end = float("-inf")

    for request in sorted_requests:
        if request["Начало"] >= current_end:
            result.append(request)
            current_end = request["Конец"]

    return result


@app.cell(hide_code=True)
def _(random):
    def generate_cover_segments(n, L, R):
        segments = []
        current = L

        index = 1

        while current < R:
            start = random.randint(max(L, current - 5), current)
            end = random.randint(current + 1, min(R, current + 15))

            segments.append({
                "№": index,
                "Начало": start,
                "Конец": end,
            })

            current = end
            index += 1

        while len(segments) < n:
            a = random.randint(L, R - 1)
            b = random.randint(a + 1, R)

            segments.append({
                "№": index,
                "Начало": a,
                "Конец": b,
            })

            index += 1

        random.shuffle(segments)

        for i, segment in enumerate(segments, 1):
            segment["№"] = i

        return segments

    return (generate_cover_segments,)


@app.function(hide_code=True)
def min_cover_segments(segments, L, R):
    sorted_segments = sorted(segments, key=lambda x: x["Начало"])

    result = []
    steps = []

    current = L
    i = 0
    step = 1

    while current < R:
        best_segment = None
        best_reach = current

        while i < len(sorted_segments) and sorted_segments[i]["Начало"] <= current:
            if sorted_segments[i]["Конец"] > best_reach:
                best_reach = sorted_segments[i]["Конец"]
                best_segment = sorted_segments[i]

            i += 1

        if best_segment is None:
            return None, steps

        result.append(best_segment)

        steps.append({
            "Шаг": step,
            "№ отрезка": best_segment["№"],
            "Отрезок": f'[{best_segment["Начало"]}, {best_segment["Конец"]}]',
            "Покрыто до выбора": current,
            "Покрыто после выбора": best_reach,
        })

        current = best_reach
        step += 1

    return result, steps


@app.cell(hide_code=True)
def _(
    generate_cover_segments,
    generate_segments,
    left_limit,
    n_segments,
    right_limit,
    time,
):
    segments = generate_segments(
        n_segments.value,
        left_limit.value,
        right_limit.value
    )

    cover_segments = generate_cover_segments(
        n_segments.value,
        left_limit.value,
        right_limit.value
    )

    start = time.perf_counter()
    answer_task_1 = answer_task_1 = max_non_overlapping_segments(segments, allow_touch=False)
    time_task_1 = time.perf_counter() - start

    start = time.perf_counter()
    answer_task_2 = max_requests(segments)
    time_task_2 = time.perf_counter() - start

    start = time.perf_counter()
    answer_task_3, steps_task_3 = min_cover_segments(
        cover_segments,
        left_limit.value,
        right_limit.value
    )
    time_task_3 = time.perf_counter() - start
    return (
        answer_task_1,
        answer_task_2,
        answer_task_3,
        cover_segments,
        segments,
        time_task_1,
        time_task_2,
        time_task_3,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Исходные отрезки для задач 1 и 2
    """)
    return


@app.cell
def _(mo, segments):
    mo.ui.table(segments)
    return


@app.cell(hide_code=True)
def _(answer_task_1, mo, time_task_1):
    mo.md(f"""
    ## Задача 1

    Выбрано непересекающихся отрезков: **{len(answer_task_1)}**

    Время выполнения: **{time_task_1:.6f} сек**

    Сложность алгоритма: **O(n log n)**
    """)
    return


@app.cell
def _(answer_task_1, mo):
    mo.ui.table(answer_task_1)
    return


@app.cell(hide_code=True)
def _(answer_task_2, mo, time_task_2):
    mo.md(f"""
    ## Задача 2

    Максимальное количество допустимых заявок: **{len(answer_task_2)}**

    Время выполнения: **{time_task_2:.6f} сек**

    Сложность алгоритма: **O(n log n)**
    """)
    return


@app.cell
def _(answer_task_2, mo):
    mo.ui.table(answer_task_2)
    return


@app.cell(hide_code=True)
def _(left_limit, mo, right_limit):
    mo.md(f"""
    ## Исходные отрезки для задачи 3

    Нужно покрыть интервал: **[{left_limit.value}, {right_limit.value}]**
    """)
    return


@app.cell
def _(cover_segments, mo):
    mo.ui.table(cover_segments)
    return


@app.cell(hide_code=True)
def _(answer_task_3, mo, time_task_3):
    mo.md(f"""
    ## Задача 3

    Минимальное количество отрезков для покрытия: **{len(answer_task_3)}**

    Время выполнения: **{time_task_3:.6f} сек**

    Сложность алгоритма: **O(n log n)**
    """)
    return


@app.cell
def _(answer_task_3, mo):
    mo.ui.table(answer_task_3)
    return


@app.cell(hide_code=True)
def _(answer_task_1, plt, segments):
    def plot_task1():
        fig, ax = plt.subplots(figsize=(10, 6))
    
        selected_ids = {segment["№"] for segment in answer_task_1}
    
        for i, segment in enumerate(segments):
            y = i + 1
    
            if segment["№"] in selected_ids:
                linewidth = 5
                label = f'№{segment["№"]} выбран'
            else:
                linewidth = 2
                label = f'№{segment["№"]}'
    
            ax.plot(
                [segment["Начало"], segment["Конец"]],
                [y, y],
                linewidth=linewidth
            )
    
            ax.text(
                segment["Начало"],
                y + 0.15,
                label,
                fontsize=8
            )
    
        ax.set_title("Задача 1: максимум непересекающихся отрезков")
        ax.set_xlabel("Координата")
        ax.set_ylabel("Номер строки")
    
        ax.grid(True, axis="x", alpha=0.3)
    
        plt.show()
    
    plot_task1()
    return


@app.cell(hide_code=True)
def _(answer_task_3, cover_segments, left_limit, plt, right_limit):
    def plot_task2():
        fig, ax = plt.subplots()
    
        for i, segment in enumerate(cover_segments):
            ax.plot(
                [segment["Начало"], segment["Конец"]],
                [i, i],
                linewidth=2
            )
    
        if answer_task_3 is not None:
            selected_sorted = sorted(answer_task_3, key=lambda x: x["Начало"])
    
            selected_y = -2
    
            for segment in selected_sorted:
                ax.plot(
                    [segment["Начало"], segment["Конец"]],
                    [selected_y, selected_y],
                    linewidth=6
                )
    
                ax.text(
                    (segment["Начало"] + segment["Конец"]) / 2,
                    selected_y - 0.5,
                    f'{segment["№"]}',
                    ha="center"
                )
    
        ax.axvline(left_limit.value, linestyle="--")
        ax.axvline(right_limit.value, linestyle="--")
    
        ax.set_title("Задача 3: минимальное покрытие интервала")
        ax.set_xlabel("Координата")
        ax.set_ylabel("Отрезок")
    
        plt.show()

    plot_task2()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Вывод

    В лабораторной работе были рассмотрены жадные алгоритмы для задач с отрезками.

    В задачах 1 и 2 оптимальная стратегия состоит в том, чтобы сортировать отрезки или заявки по времени окончания и каждый раз выбирать тот вариант, который заканчивается раньше.

    В задаче 3 используется другой жадный подход: среди всех отрезков, начинающихся не правее текущей покрытой точки, выбирается тот, который продвигает покрытие дальше всего вправо.

    Во всех трёх задачах основная сложность связана с сортировкой, поэтому итоговая сложность алгоритмов составляет `O(n log n)`.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
