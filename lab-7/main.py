from dataclasses import dataclass
from typing import List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import box

console = Console()


@dataclass
class Order:
    name: str
    deadline: int
    profit: int


def schedule_orders_greedy(orders: List[Order]) -> Tuple[List[Order], int]:
    if not orders:
        return [], 0

    max_deadline = max(order.deadline for order in orders)
    slots: List[Order | None] = [None] * max_deadline

    for order in sorted(orders, key=lambda x: x.profit, reverse=True):
        for day in range(order.deadline - 1, -1, -1):
            if slots[day] is None:
                slots[day] = order
                break

    selected = [order for order in slots if order is not None]
    total_profit = sum(order.profit for order in selected)
    return selected, total_profit


def render_orders_input(orders: List[Order], title: str) -> None:
    table = Table(title=title, box=box.ROUNDED, show_lines=True)
    table.add_column("Заказ", justify="center", style="cyan", no_wrap=True)
    table.add_column("Дедлайн", justify="center", style="magenta")
    table.add_column("Стоимость", justify="center", style="green")

    for order in orders:
        table.add_row(order.name, str(order.deadline), str(order.profit))

    console.print(table)


def render_orders_result(selected: List[Order], total_profit: int) -> None:
    table = Table(
        title="Оптимальное расписание заказов", box=box.ROUNDED, show_lines=True
    )
    table.add_column("День", justify="center", style="yellow")
    table.add_column("Заказ", justify="center", style="cyan")
    table.add_column("Стоимость", justify="center", style="green")
    table.add_column("Дедлайн", justify="center", style="magenta")

    for idx, order in enumerate(selected, start=1):
        table.add_row(str(idx), order.name, str(order.profit), str(order.deadline))

    console.print(table)
    console.print(
        Panel.fit(
            f"[bold green]Суммарная стоимость:[/bold green] {total_profit}",
            title="Результат",
            border_style="green",
        )
    )


def manual_input_task_1() -> None:
    console.print(Panel.fit("Задача 1 — ручной ввод", border_style="blue"))

    n = IntPrompt.ask("Введите количество заказов", default=5)
    orders: List[Order] = []

    for i in range(1, n + 1):
        console.print(f"\n[bold]Заказ {i}[/bold]")
        name = Prompt.ask("Номер/имя заказа", default=f"Z{i}")
        deadline = IntPrompt.ask("Дедлайн (день)", default=1)
        profit = IntPrompt.ask("Стоимость", default=10)
        orders.append(Order(name=name, deadline=deadline, profit=profit))

    console.print()
    render_orders_input(orders, "Введённые данные")
    selected, total_profit = schedule_orders_greedy(orders)
    render_orders_result(selected, total_profit)


def demo_task_1() -> None:
    orders = [
        Order("A", 2, 40),
        Order("B", 1, 25),
        Order("C", 2, 30),
        Order("D", 1, 15),
        Order("E", 3, 20),
    ]

    console.print(Panel.fit("Задача 1 — фиксированные значения", border_style="blue"))
    render_orders_input(orders, "Исходные данные из примера")
    selected, total_profit = schedule_orders_greedy(orders)
    render_orders_result(selected, total_profit)


@dataclass
class Child:
    number: str
    age: int


def group_children_greedy(children: List[Child]) -> List[List[Child]]:
    if not children:
        return []

    children_sorted = sorted(children, key=lambda x: x.age)
    groups: List[List[Child]] = []
    i = 0

    while i < len(children_sorted):
        start_age = children_sorted[i].age
        group = [children_sorted[i]]
        i += 1

        while i < len(children_sorted) and children_sorted[i].age <= start_age + 2:
            group.append(children_sorted[i])
            i += 1

        groups.append(group)

    return groups


def render_children_input(children: List[Child], title: str) -> None:
    table = Table(title=title, box=box.ROUNDED, show_lines=True)
    table.add_column("Ребёнок", justify="center", style="cyan")
    table.add_column("Возраст", justify="center", style="green")

    for child in children:
        table.add_row(child.number, str(child.age))

    console.print(table)


def render_groups(groups: List[List[Child]]) -> None:
    table = Table(title="Сформированные группы", box=box.ROUNDED, show_lines=True)
    table.add_column("Группа", justify="center", style="yellow")
    table.add_column("Дети", style="cyan")
    table.add_column("Возрасты", style="green")
    table.add_column("Разброс", justify="center", style="magenta")

    for idx, group in enumerate(groups, start=1):
        children_names = ", ".join(child.number for child in group)
        ages = [child.age for child in group]
        ages_text = ", ".join(map(str, ages))
        spread = max(ages) - min(ages)
        table.add_row(str(idx), children_names, ages_text, str(spread))

    console.print(table)
    console.print(
        Panel.fit(
            f"[bold green]Минимальное количество групп:[/bold green] {len(groups)}",
            title="Результат",
            border_style="green",
        )
    )


def manual_input_task_2() -> None:
    console.print(Panel.fit("Задача 2 — ручной ввод", border_style="blue"))

    n = IntPrompt.ask("Введите количество детей", default=6)
    children: List[Child] = []

    for i in range(1, n + 1):
        console.print(f"\n[bold]Ребёнок {i}[/bold]")
        number = Prompt.ask("Номер ребёнка", default=str(i))
        age = IntPrompt.ask("Возраст", default=6)
        children.append(Child(number=number, age=age))

    console.print()
    render_children_input(children, "Введённые данные")
    groups = group_children_greedy(children)
    render_groups(groups)


def demo_task_2() -> None:
    children = [
        Child("1", 5),
        Child("2", 7),
        Child("3", 6),
        Child("4", 10),
        Child("5", 8),
        Child("6", 11),
        Child("7", 12),
        Child("8", 4),
    ]

    console.print(Panel.fit("Задача 2 — фиксированные значения", border_style="blue"))
    render_children_input(children, "Исходные данные")
    groups = group_children_greedy(children)
    render_groups(groups)


def print_main_menu() -> None:
    menu = Table(
        title="Лабораторная работа 7 — Жадные алгоритмы",
        box=box.DOUBLE_EDGE,
        show_header=False,
    )
    menu.add_column("Пункт", style="yellow", justify="center", width=8)
    menu.add_column("Описание", style="white")

    menu.add_row("1", "Задача 1 — ручной ввод")
    menu.add_row("2", "Задача 1 — фиксированные значения")
    menu.add_row("3", "Задача 2 — ручной ввод")
    menu.add_row("4", "Задача 2 — фиксированные значения")
    menu.add_row("5", "Запустить оба задания на фиксированных значениях")
    menu.add_row("0", "Выход")

    console.print(menu)


def main() -> None:
    console.print(
        Panel.fit(
            "[bold]Лабораторная работа 7[/bold]\n"
            "«АЛГОРИТМЫ И АНАЛИЗ СЛОЖНОСТИ»\n"
            "[bold]ЖАДНЫЕ АЛГОРИТМЫ[/bold]",
            border_style="bright_blue",
        )
    )

    while True:
        print_main_menu()
        choice = Prompt.ask(
            "Выберите пункт меню",
            choices=["0", "1", "2", "3", "4", "5"],
            default="5",
        )
        console.print()

        if choice == "1":
            manual_input_task_1()
        elif choice == "2":
            demo_task_1()
        elif choice == "3":
            manual_input_task_2()
        elif choice == "4":
            demo_task_2()
        elif choice == "5":
            demo_task_1()
            console.print()
            demo_task_2()
        elif choice == "0":
            console.print(Panel.fit("Работа программы завершена.", border_style="red"))
            break

        console.print("\n" + "─" * 70 + "\n")


if __name__ == "__main__":
    main()
