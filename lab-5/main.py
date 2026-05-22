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
    # Лабораторная работа 5
    ## Алгоритмы работы со строками

    ### Задача
    Выполнить сравнительный анализ алгоритмов поиска подстроки в строке:

    1. Наивный метод
    2. Алгоритм Бойера-Мура
    3. Алгоритм Рабина-Карпа
    4. Алгоритм Кнута-Морриса-Пратта
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import time
    import random
    import string

    return plt, random, string, time


@app.cell
def _(mo):
    text_length = mo.ui.slider(
        1000,
        100000,
        step=1000,
        value=20000,
        label="Длина текста"
    )

    pattern_length = mo.ui.slider(
        3,
        30,
        value=10,
        label="Длина подстроки"
    )

    mo.vstack([text_length, pattern_length])
    return pattern_length, text_length


@app.cell
def _(mo, pattern_length, text_length):
    mo.vstack([f"text_length: {text_length.value}", f"pattern_length: {pattern_length.value}"])
    return


@app.cell(hide_code=True)
def _(random, string):
    def generate_text_and_pattern(text_length, pattern_length):
        alphabet = string.ascii_lowercase

        text = "".join(random.choice(alphabet) for _ in range(text_length))

        start_index = random.randint(0, text_length - pattern_length)

        pattern = text[start_index:start_index + pattern_length]

        return text, pattern

    return (generate_text_and_pattern,)


@app.function(hide_code=True)
def naive_search(text, pattern):
    result = []

    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        match = True

        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break

        if match:
            result.append(i)

    return result


@app.function(hide_code=True)
def boyer_moore_search(text, pattern):
    result = []

    n = len(text)
    m = len(pattern)

    if m == 0:
        return result

    bad_char = {}

    for i in range(m):
        bad_char[pattern[i]] = i

    shift = 0

    while shift <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            result.append(shift)

            if shift + m < n:
                shift += m - bad_char.get(text[shift + m], -1)
            else:
                shift += 1
        else:
            shift += max(1, j - bad_char.get(text[shift + j], -1))

    return result


@app.function(hide_code=True)
def rabin_karp_search(text, pattern):
    result = []

    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return result

    base = 256
    mod = 101

    pattern_hash = 0
    text_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % mod

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        text_hash = (base * text_hash + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                result.append(i)

        if i < n - m:
            text_hash = (
                base * (text_hash - ord(text[i]) * h)
                + ord(text[i + m])
            ) % mod

            if text_hash < 0:
                text_hash += mod

    return result


@app.cell(hide_code=True)
def _():
    def compute_lps(pattern):
        m = len(pattern)

        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps


    def kmp_search(text, pattern):
        result = []

        n = len(text)
        m = len(pattern)

        if m == 0:
            return result

        lps = compute_lps(pattern)

        i = 0
        j = 0

        while i < n:
            if text[i] == pattern[j]:
                i += 1
                j += 1

            if j == m:
                result.append(i - j)
                j = lps[j - 1]

            elif i < n and text[i] != pattern[j]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return result

    return (kmp_search,)


@app.cell(hide_code=True)
def _(
    generate_text_and_pattern,
    kmp_search,
    mo,
    pattern_length,
    text_length,
    time,
):
    text, pattern = generate_text_and_pattern(
        text_length.value,
        pattern_length.value
    )

    algorithms = {
        "Наивный метод": naive_search,
        "Бойер-Мур": boyer_moore_search,
        "Рабин-Карп": rabin_karp_search,
        "Кнут-Моррис-Пратт": kmp_search,
    }

    results = []

    for name, func in algorithms.items():
        start = time.perf_counter()

        positions = func(text, pattern)

        elapsed = time.perf_counter() - start

        if name == "Наивный метод":
            complexity = "O(n · m)"
        elif name == "Бойер-Мур":
            complexity = "O(n / m) в лучшем, O(n · m) в худшем"
        else:
            complexity = "O(n + m)"

        results.append({
            "Алгоритм": name,
            "Время": elapsed,
            "Количество вхождений": len(positions),
            "Позиции": positions[:10],
            "Сложность": complexity,
        })

    mo.md(f"""
    ## Тестовые данные

    Длина текста: **{len(text)}**

    Длина подстроки: **{len(pattern)}**

    Искомая подстрока: `{pattern}`
    """)
    return (results,)


@app.cell
def _(mo, results):
    mo.ui.table(results)
    return


@app.cell
def _(plt, results):
    names = [item["Алгоритм"] for item in results]
    times = [item["Время"] for item in results]

    fig, ax = plt.subplots()

    ax.bar(names, times)

    ax.set_title("Сравнение времени поиска подстроки")
    ax.set_xlabel("Алгоритм")
    ax.set_ylabel("Время, сек")

    plt.xticks(rotation=15)

    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Вывод

    В ходе лабораторной работы были реализованы и сравнены четыре алгоритма поиска подстроки в строке.

    Наивный алгоритм прост в реализации, но при больших строках может работать медленно, так как имеет сложность `O(n · m)`.

    Алгоритм Бойера-Мура часто работает быстрее на практике, поскольку выполняет сдвиги по строке и не проверяет каждый символ.

    Алгоритм Рабина-Карпа использует хеширование и имеет среднюю сложность `O(n + m)`.

    Алгоритм Кнута-Морриса-Пратта предварительно строит таблицу префиксов и также работает за `O(n + m)`.

    На больших входных данных наиболее эффективными обычно являются алгоритмы Бойера-Мура, Рабина-Карпа и Кнута-Морриса-Пратта.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
