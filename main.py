import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import time
    import random
    import matplotlib.pyplot as plt

    return plt, random, time


@app.cell
def _(random):
    random.seed(42)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Алгоритмы и анализ сложности
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Задание 1

    Необходимо вычислить `n`-й член последовательности Фиббоначи двумя методами:
    - Рекурсивный
    - Итерационный
    """)
    return


@app.function
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


@app.function
def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@app.cell
def _():
    print(f"index: recursive | iterative")
    for i in range(15 + 1):
        print(f"{i:5d}: {fib_recursive(i):9d} | {fib_iterative(i):9d}")
    return


@app.cell
def _(plt, time):
    def run_fibonacci_benchmark():
        n_values = list(range(1, 30))
        recursive_times = []
        iterative_times = []

        for n in n_values:
            start = time.time()
            fib_recursive(n)
            end = time.time()
            recursive_times.append(end - start)

            start = time.time()
            fib_iterative(n)
            end = time.time()
            iterative_times.append(end - start)

        plt.figure(figsize=(10, 6))
        plt.plot(n_values, recursive_times, label="Рекурсивная реализация", marker="o")
        plt.plot(n_values, iterative_times, label="Итеративная реализация", marker="x")
        plt.xlabel("n число Фибоначчи")
        plt.ylabel("Время (секунды)")
        plt.title("Сравнение")
        plt.legend()
        plt.grid(True)
        plt.show()

    run_fibonacci_benchmark()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Задание 2

    Необходимо сравнить три алгоритма сортировки:
    - Гномья сортировка
    - Пузырьковая сортировка
    - Insertion sort
    """)
    return


@app.function
def gnome_sort(arr):
    i = 0
    while i < len(arr):
        if i == 0 or arr[i] >= arr[i - 1]:
            i += 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1
    return arr


@app.function
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


@app.function
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


@app.cell
def _(plt, random, time):
    def run_sorting_algorithm_benchmark():
        sizes = [100, 200, 300, 400, 500, 750, 1000]
        gnome_times = []
        bubble_times = []
        insertion_times = []

        for size in sizes:
            arr = [random.randint(1, 1000) for _ in range(size)]

            arr_copy = arr.copy()
            start = time.time()
            gnome_sort(arr_copy)
            gnome_times.append(time.time() - start)

            arr_copy = arr.copy()
            start = time.time()
            bubble_sort(arr_copy)
            bubble_times.append(time.time() - start)

            arr_copy = arr.copy()
            start = time.time()
            insertion_sort(arr_copy)
            insertion_times.append(time.time() - start)

        plt.figure(figsize=(10, 6))
        plt.plot(sizes, gnome_times, label="Гномья сортировка", marker="o")
        plt.plot(sizes, bubble_times, label="Сортировка пузырьком", marker="x")
        plt.plot(sizes, insertion_times, label="Insertion Sort", marker="s")
        plt.xlabel("Размер массива")
        plt.ylabel("Время (секунды)")
        plt.title("Сравнение")
        plt.legend()
        plt.grid(True)
        plt.show()

    run_sorting_algorithm_benchmark()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Задание 3
    """)
    return


@app.cell
def _():
    def next_permutation(arr):
        i = len(arr) - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        if i == -1:
            return False
        j = len(arr) - 1
        while arr[j] <= arr[i]:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
        arr[i+1:] = reversed(arr[i+1:])
        return True

    arr = [1, 2, 3]
    perms = [arr.copy()]
    while next_permutation(arr):
        perms.append(arr.copy())

    print(perms)
    return (next_permutation,)


@app.cell
def _():
    def jt_permutation(n):
        arr = list(range(1, n+1))
        left = [-1]*n
        yield arr.copy()
    
        while True:
            mobile = -1
            for i in range(n):
                j = i + left[i]
                if 0 <= j < n and arr[i] > arr[j] and arr[i] > mobile:
                    mobile = arr[i]
                    index = i
            if mobile == -1:
                break
            j = index + left[index]
            arr[index], arr[j] = arr[j], arr[index]
            left[index], left[j] = left[j], left[index]
            for i in range(n):
                if arr[i] > mobile:
                    left[i] *= -1
            yield arr.copy()

    print(list(jt_permutation(3)))
    return (jt_permutation,)


@app.cell
def _(jt_permutation, next_permutation, time):
    def run_permutation_benchmark():
        for n in range(1, 9):
            arr = list(range(1, n+1))
        
            start = time.time()
            perms = [arr.copy()]
            while next_permutation(arr):
                perms.append(arr.copy())
            print(f"Lexicographic n={n} time: {time.time() - start:.6f}s")
        
            start = time.time()
            perms = list(jt_permutation(n))
            print(f"Johnson-Trotter n={n} time: {time.time() - start:.6f}s")

    run_permutation_benchmark()
    return


@app.cell
def _(plt, time):
    def run_permutations_benchmark():
        import itertools
        import copy
    
        def narayana_permutations(n):
            a = list(range(1, n + 1))
            result = [a[:]]
        
            while True:
                i = n - 2
                while i >= 0 and a[i] >= a[i + 1]:
                    i -= 1
                if i < 0:
                    break
            
                j = n - 1
                while a[j] <= a[i]:
                    j -= 1
            
                a[i], a[j] = a[j], a[i]
            
                a[i + 1:] = reversed(a[i + 1:])
            
                result.append(a[:])
        
            return result
    
    
        def johnson_trotter_permutations(n):
            perm = list(range(1, n + 1))
            directions = [-1] * n
            result = [perm[:]]
        
            while True:
                mobile = -1
                mobile_idx = -1
            
                for i in range(n):
                    neighbor = i + directions[i]
                    if 0 <= neighbor < n:
                        if perm[i] > perm[neighbor] and perm[i] > mobile:
                            mobile = perm[i]
                            mobile_idx = i
            
                if mobile_idx == -1:
                    break
            
                neighbor = mobile_idx + directions[mobile_idx]
                perm[mobile_idx], perm[neighbor] = perm[neighbor], perm[mobile_idx]
                directions[mobile_idx], directions[neighbor] = directions[neighbor], directions[mobile_idx]
                mobile_idx = neighbor
            
                for i in range(n):
                    if perm[i] > mobile:
                        directions[i] = -directions[i]
            
                result.append(perm[:])
        
            return result
    
    
        def inversion_vector_permutations(n):
            result = []
    
            inv = [0] * n
            total = 1
            for i in range(1, n + 1):
                total *= i
        
            for _ in range(total):
                perm = inversion_to_perm(inv, n)
                result.append(perm)
            
                k = n - 1
                while k >= 0:
                    inv[k] += 1
                    if inv[k] <= k:
                        break
                    inv[k] = 0
                    k -= 1
        
            return result
    
    
        def inversion_to_perm(inv, n):
            perm = []
            for i in range(n, 0, -1):
                pos = inv[i - 1]
                perm.insert(pos, i)
            return perm
    
    
        print("=" * 60)
        print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ ДЛЯ n=4")
        print("=" * 60)
    
        n = 4
    
        print(f"\n--- Алгоритм Нарайаны (n={n}) ---")
        perms_narayana = narayana_permutations(n)
        for p in perms_narayana:
            print(p)
        print(f"Всего: {len(perms_narayana)}")
    
        print(f"\n--- Алгоритм Джонсона-Троттера (n={n}) ---")
        perms_jt = johnson_trotter_permutations(n)
        for p in perms_jt:
            print(p)
        print(f"Всего: {len(perms_jt)}")
    
        print(f"\n--- Алгоритм вектора инверсий (n={n}) ---")
        perms_inv = inversion_vector_permutations(n)
        for p in perms_inv:
            print(p)
        print(f"Всего: {len(perms_inv)}")
    
    
        print("\n" + "=" * 60)
        print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ ВРЕМЕНИ РАБОТЫ")
        print("=" * 60)
    
        def benchmark_narayana(n):
            start = time.time()
            narayana_permutations(n)
            return time.time() - start
    
        def benchmark_jt(n):
            start = time.time()
            johnson_trotter_permutations(n)
            return time.time() - start
    
        def benchmark_inv(n):
            start = time.time()
            inversion_vector_permutations(n)
            return time.time() - start
    
        test_values_full = list(range(1, 11))
        times_narayana = []
        times_jt = []
        times_inv = []
    
        for n_val in test_values_full:
            t1 = benchmark_narayana(n_val)
            t2 = benchmark_jt(n_val)
            t3 = benchmark_inv(n_val)
            times_narayana.append(t1)
            times_jt.append(t2)
            times_inv.append(t3)
            print(f"n={n_val:2d} | Нарайана: {t1:.6f}с | Джонсон-Троттер: {t2:.6f}с | Вектор инверсий: {t3:.6f}с")
    
        plt.figure(figsize=(12, 6))
        plt.plot(test_values_full, times_narayana, 'b-o', label='Нарайана')
        plt.plot(test_values_full, times_jt, 'r-s', label='Джонсон-Троттер')
        plt.plot(test_values_full, times_inv, 'g-^', label='Вектор инверсий')
        plt.xlabel('n')
        plt.ylabel('Время (с)')
        plt.title('Сравнение алгоритмов генерации перестановок')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')
        plt.savefig('permutations_comparison.png', dpi=150)
        plt.show()

    run_permutations_benchmark()
    return


@app.cell
def _():
    from itertools import combinations


    def solve_stationery_problem(budget, shopping_list, price_list):
        available_items = {}
        for item, qty in shopping_list.items():
            if item in price_list:
                available_items[item] = {
                    'needed': qty,
                    'price': price_list[item],
                    'total_cost': qty * price_list[item]
                }
    
        print(f"\nБюджет: {budget} руб.")
        print(f"\nСписок покупок (доступные в магазине):")
        for item, info in available_items.items():
            print(f"  {item}: {info['needed']} шт. × {info['price']} руб. = {info['total_cost']} руб.")
    
        item_names = list(available_items.keys())
        n = len(item_names)
    
        best_purchase = {}
        best_names_count = 0
        best_total_cost = float('inf')
        best_total_items = 0
    
        for size in range(n, 0, -1):
            for combo in combinations(item_names, size):
                purchase = {}
                total_cost = 0
            
                full_cost = sum(
                    available_items[item]['needed'] * available_items[item]['price']
                    for item in combo
                )
            
                if full_cost <= budget:
                    for item in combo:
                        purchase[item] = available_items[item]['needed']
                    total_cost = full_cost
                else:
                    min_cost = sum(available_items[item]['price'] for item in combo)
                
                    if min_cost > budget:
                        continue
                
                    purchase = {item: 1 for item in combo}
                    total_cost = min_cost
                    remaining = budget - total_cost
                
                    changed = True
                    while changed:
                        changed = False
                        for item in sorted(combo, key=lambda x: available_items[x]['price']):
                            if purchase[item] < available_items[item]['needed']:
                                if available_items[item]['price'] <= remaining:
                                    purchase[item] += 1
                                    remaining -= available_items[item]['price']
                                    total_cost += available_items[item]['price']
                                    changed = True
            
                names_count = len(purchase)
                total_items = sum(purchase.values())
            
                if (names_count > best_names_count or
                    (names_count == best_names_count and total_items > best_total_items) or
                    (names_count == best_names_count and total_items == best_total_items 
                     and total_cost < best_total_cost)):
                    best_purchase = purchase.copy()
                    best_names_count = names_count
                    best_total_cost = total_cost
                    best_total_items = total_items
        
            if best_names_count == size:
                break
    
        return best_purchase, best_total_cost


    print("=" * 60)
    print("ЗАДАНИЕ 4: Покупка канцелярских принадлежностей")
    print("=" * 60)

    budget = 500

    shopping_list = {
        "тетрадь 48 л.": 5,
        "ручка шариковая": 3,
        "карандаш": 2,
        "ластик": 2,
        "линейка 30 см": 1,
        "маркер": 4,
        "папка": 2,
        "степлер": 1,
        "скрепки (уп.)": 1,
        "корректор": 1
    }

    price_list = {
        "тетрадь 48 л.": 45,
        "ручка шариковая": 25,
        "карандаш": 15,
        "ластик": 20,
        "линейка 30 см": 35,
        "маркер": 55,
        "папка": 40,
        "степлер": 150,
        "скрепки (уп.)": 30,
        "корректор": 60
    }

    purchase, total_cost = solve_stationery_problem(budget, shopping_list, price_list)

    print(f"\n{'=' * 50}")
    print("ОПТИМАЛЬНЫЙ НАБОР ПОКУПОК:")
    print(f"{'=' * 50}")
    print(f"{'Товар':<25} {'Кол-во':>8} {'Цена':>8} {'Сумма':>8}")
    print("-" * 50)

    for item, qty in sorted(purchase.items()):
        price = price_list[item]
        subtotal = qty * price
        needed = shopping_list[item]
        status = "✓" if qty == needed else f"(нужно {needed})"
        print(f"{item:<25} {qty:>5} шт. {price:>6} р. {subtotal:>6} р. {status}")

    print("-" * 50)
    print(f"{'ИТОГО:':<25} {sum(purchase.values()):>5} шт. {'':>8} {total_cost:>6} р.")
    print(f"{'Остаток:':<25} {'':>14} {budget - total_cost:>6} р.")
    print(f"Количество наименований: {len(purchase)} из {len(shopping_list)}")


    print("\n\n" + "=" * 60)
    print("ТЕСТ 2: Ограниченный бюджет (200 руб.)")
    print("=" * 60)

    purchase2, total_cost2 = solve_stationery_problem(200, shopping_list, price_list)

    print(f"\n{'=' * 50}")
    print("ОПТИМАЛЬНЫЙ НАБОР ПОКУПОК:")
    print(f"{'=' * 50}")
    for item, qty in sorted(purchase2.items()):
        price = price_list[item]
        print(f"  {item}: {qty} шт. × {price} р. = {qty * price} р.")
    print(f"\nИтого: {total_cost2} р. (бюджет: 200 р.)")
    print(f"Наименований: {len(purchase2)}")
    return


if __name__ == "__main__":
    app.run()
