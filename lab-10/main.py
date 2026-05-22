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
    # Лабораторная работа 10
    ## Код Хаффмана

    ### Задача

    На вход программы подаётся текст.

    Необходимо:

    1. Выполнить кодировку текста.
    2. Выдать словарь, в котором каждому символу соответствует код.
    3. Проверить условие Фано.
    4. Закодировать текст минимально возможной последовательностью нулей и единиц.
    5. Выполнить восстановление исходного текста.
    6. Оценить сложность работы алгоритма.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import heapq
    import time
    from collections import Counter

    return Counter, heapq, plt, time


@app.cell(hide_code=True)
def _(mo):
    text_input = mo.ui.text_area(
        value="пример текста для кодирования алгоритмом хаффмана",
        label="Введите текст",
        rows=4
    )

    text_input
    return (text_input,)


@app.class_definition(hide_code=True)
class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


@app.cell(hide_code=True)
def _(Counter, heapq):
    def build_huffman_tree(text):
        frequencies = Counter(text)

        heap = []

        for char, freq in frequencies.items():
            heapq.heappush(heap, HuffmanNode(char=char, freq=freq))

        if len(heap) == 1:
            only_node = heapq.heappop(heap)
            return HuffmanNode(freq=only_node.freq, left=only_node)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = HuffmanNode(
                freq=left.freq + right.freq,
                left=left,
                right=right
            )

            heapq.heappush(heap, merged)

        return heap[0]

    return (build_huffman_tree,)


@app.function(hide_code=True)
def build_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = current_code if current_code else "0"
        return codes

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes


@app.cell(hide_code=True)
def _():
    def encode_text(text, codes):
        return "".join(codes[char] for char in text)


    def decode_text(encoded_text, tree):
        result = []
        node = tree

        for bit in encoded_text:
            if bit == "0":
                node = node.left
            else:
                node = node.right

            if node.char is not None:
                result.append(node.char)
                node = tree

        return "".join(result)

    return decode_text, encode_text


@app.function(hide_code=True)
def check_fano_condition(codes):
    code_values = list(codes.values())

    for i in range(len(code_values)):
        for j in range(len(code_values)):
            if i != j and code_values[j].startswith(code_values[i]):
                return False

    return True


@app.cell(hide_code=True)
def _(Counter, build_huffman_tree, decode_text, encode_text, text_input, time):
    text = text_input.value

    start = time.perf_counter()

    tree = build_huffman_tree(text)
    codes = build_codes(tree)
    encoded_text = encode_text(text, codes)
    decoded_text = decode_text(encoded_text, tree)

    elapsed = time.perf_counter() - start

    frequencies = Counter(text)
    fano_ok = check_fano_condition(codes)
    decode_ok = text == decoded_text
    return (
        codes,
        decode_ok,
        decoded_text,
        elapsed,
        encoded_text,
        fano_ok,
        frequencies,
        text,
    )


@app.cell(hide_code=True)
def _(encoded_text, frequencies, mo, text):
    mo.md(f"""
    ## Исходные данные

    Исходный текст:

    `{text}`

    Количество символов в тексте: **{len(text)}**

    Количество различных символов: **{len(frequencies)}**

    ## Закодированный текст

    Длина закодированного текста: **{len(encoded_text)} бит**

    {encoded_text}
    """)
    return


@app.cell(hide_code=True)
def _(frequencies, mo):
    frequency_table = [
        {
            "Символ": repr(char),
            "Частота": freq
        }
        for char, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    ]

    mo.ui.table(frequency_table)
    return


@app.cell(hide_code=True)
def _(codes, frequencies, mo):
    codes_table = [
        {
            "Символ": repr(char),
            "Частота": frequencies[char],
            "Код Хаффмана": code,
            "Длина кода": len(code),
        }
        for char, code in sorted(codes.items(), key=lambda x: frequencies[x[0]], reverse=True)
    ]

    mo.ui.table(codes_table)
    return


@app.cell(hide_code=True)
def _(decode_ok, decoded_text, fano_ok, mo):
    mo.md(f"""
    ## Восстановление текста

    Декодированный текст:

    `{decoded_text}`

    Совпадает с исходным текстом: **{decode_ok}**

    Условие Фано выполняется: **{fano_ok}**
    """)
    return


@app.cell(hide_code=True)
def _(elapsed, encoded_text, mo, text):
    original_bits = len(text) * 8
    compressed_bits = len(encoded_text)

    if original_bits == 0:
        compression_ratio = 0
    else:
        compression_ratio = compressed_bits / original_bits

    compression_table = [
        {
            "Показатель": "Исходный размер",
            "Значение": original_bits,
            "Единица": "бит",
        },
        {
            "Показатель": "Размер после кодирования",
            "Значение": compressed_bits,
            "Единица": "бит",
        },
        {
            "Показатель": "Коэффициент сжатия",
            "Значение": round(compression_ratio, 4),
            "Единица": "",
        },
        {
            "Показатель": "Время выполнения",
            "Значение": round(elapsed, 6),
            "Единица": "сек",
        },
    ]

    mo.ui.table(compression_table)
    return


@app.cell(hide_code=True)
def _(frequencies, plt):
    def plot_chars():
        chars = [repr(char) for char, freq in frequencies.items()]
        freqs = [freq for char, freq in frequencies.items()]
    
        fig, ax = plt.subplots()
    
        ax.bar(chars, freqs)
    
        ax.set_title("Частоты символов в тексте")
        ax.set_xlabel("Символ")
        ax.set_ylabel("Частота")
    
        plt.xticks(rotation=45)
    
        plt.show()

    plot_chars()
    return


@app.cell(hide_code=True)
def _(codes, plt):
    chars = [repr(char) for char in codes.keys()]
    lengths = [len(code) for code in codes.values()]

    fig, ax = plt.subplots()

    ax.bar(chars, lengths)

    ax.set_title("Длины кодов Хаффмана")
    ax.set_xlabel("Символ")
    ax.set_ylabel("Длина кода")

    plt.xticks(rotation=45)

    fig
    return


@app.cell(hide_code=True)
def _(decode_ok, fano_ok, mo):
    mo.md(f"""
    # Вывод

    В лабораторной работе был реализован алгоритм кодирования Хаффмана.

    Для каждого символа был построен двоичный код переменной длины.
    Чем чаще символ встречается в тексте, тем короче его код.

    Полученный словарь кодов удовлетворяет условию Фано: **{fano_ok}**.

    Декодирование выполнено успешно: **{decode_ok}**.

    Сложность построения дерева Хаффмана составляет `O(k log k)`,
    где `k` — количество различных символов.

    Кодирование и декодирование текста выполняются за `O(n)`,
    где `n` — длина текста.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
