from itertools import permutations
from random import randint, shuffle
from time import perf_counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def timer(func, *args):
    start = perf_counter()
    result = func(*args)
    end = perf_counter()
    return result, end - start


# ---------------- ЗАДАЧА 1 ----------------
# Генерация перестановок 1..n с минимальным изменением:
# алгоритм Джонсона-Троттера, аналог "кода Грэя" для перестановок


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

        perm[mobile_index], perm[swap_i] = perm[swap_i], perm[mobile_index]
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


# ---------------- ЗАДАЧА 2 ----------------
# Сравнение алгоритмов генерации случайных перестановок


def fisher_yates(n, count):
    result = []

    for _ in range(count):
        arr = list(range(1, n + 1))

        for i in range(n - 1, 0, -1):
            j = randint(0, i)
            arr[i], arr[j] = arr[j], arr[i]

        result.append(arr)

    return result


def builtin_shuffle(n, count):
    result = []

    for _ in range(count):
        arr = list(range(1, n + 1))
        shuffle(arr)
        result.append(arr)

    return result


def random_sort(n, count):
    import random

    result = []

    for _ in range(count):
        arr = list(range(1, n + 1))
        arr.sort(key=lambda _: random.random())
        result.append(arr)

    return result


def show_permutations(perms):
    table = Table(title="Перестановки в порядке кода Грэя")

    table.add_column("№", justify="right")
    table.add_column("Перестановка", justify="center")

    for i, p in enumerate(perms, 1):
        table.add_row(str(i), str(p))

    console.print(table)


def compare_algorithms(n, count):
    algorithms = [
        ("Фишер-Йетс", fisher_yates),
        ("Встроенный shuffle", builtin_shuffle),
        ("Случайная сортировка", random_sort),
    ]

    table = Table(title="Сравнение алгоритмов генерации случайных перестановок")

    table.add_column("Алгоритм")
    table.add_column("Количество перестановок", justify="right")
    table.add_column("n", justify="right")
    table.add_column("Время, сек", justify="right")
    table.add_column("Асимптотика")

    for name, func in algorithms:
        _, elapsed = timer(func, n, count)

        if name == "Случайная сортировка":
            complexity = "O(k · n log n)"
        else:
            complexity = "O(k · n)"

        table.add_row(name, str(count), str(n), f"{elapsed:.6f}", complexity)

    console.print(table)


def main():
    console.print(
        Panel.fit(
            "[bold cyan]Лабораторная работа 4[/bold cyan]\n"
            "Генерация перестановок и анализ времени выполнения"
        )
    )

    n = int(input("Введите n для генерации перестановок кодом Грэя: "))

    perms, elapsed = timer(gray_permutations, n)

    show_permutations(perms)

    console.print(
        f"[green]Всего перестановок:[/green] {len(perms)}\n"
        f"[green]Время генерации:[/green] {elapsed:.6f} сек\n"
        f"[green]Сложность:[/green] O(n!) перестановок, каждая требует до O(n)"
    )

    console.print("\n[bold]Задача 2. Сравнение случайных перестановок[/bold]")

    n_random = int(input("Введите n для случайных перестановок: "))
    count = int(input("Введите количество перестановок: "))

    compare_algorithms(n_random, count)


if __name__ == "__main__":
    main()
