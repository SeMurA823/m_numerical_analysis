E = 0.0001
a = 0.
b = 1.
k1 = 1
k2 = 0
a1 = 1
l1 = 1
l2 = 0
b1 = 10

START_N = 4
FILENAME = 'table.csv'
SPLIT_SYMBOL = ';'
from math import sin, cos, radians


def rangeWithEnd(start, stop, step=1):
    if (step > 0):
        stop = stop + 1
    else:
        stop = stop - 1
    return range(start, stop, step)


# Xi = X0 +ih
def get_x(i, h):
    return a + i * h


def write_to_csv(f, x, y_h, y_h_2, max_d, max_t):
    f.write(f"{x}{SPLIT_SYMBOL}{y_h}{SPLIT_SYMBOL}{y_h_2}{SPLIT_SYMBOL}{max_d}{SPLIT_SYMBOL}{max_t}\n")


def p(t):  # коэф при первой производной
    return sin(t) / cos(t)


def g(t):  # коэф при нулевой производной
    return (cos(t)) ** 2


def f(t):  # правая часть
    return 0


def get_y_t(t):  # точное решение
    c = (10 - cos(sin(1))) / sin(sin(1))
    return cos(sin(t)) + c * sin(sin(t))


def get_h(n):
    return (b - a) / n


def get_arr_y_k(n, h):
    t = [get_x(i, h) for i in rangeWithEnd(0, n)]
    aa, bb, cc, ff = [], [], [], []
    for i in rangeWithEnd(0, n):
        aa.append(1 - p(t[i]) * h / 2)
        bb.append(1 + p(t[i]) * h / 2)
        cc.append(2 - g(t[i]) * h**2)
        ff.append(h ** 2 * f(t[i]))
    al = [0 for _ in rangeWithEnd(0, n)]
    bet, u = [0 for _ in rangeWithEnd(0, n)], [0 for _ in rangeWithEnd(0, n)]
    al[1] = k2 / (k2 - k1 * h)
    bet[1] = -(a1 * h) / (k2 - k1 * h)
    for i in rangeWithEnd(1, n - 1):
        al[i + 1] = (bb[i] / (cc[i] - al[i] * aa[i]))
        bet[i + 1] = ((aa[i] * bet[i] - ff[i]) / (cc[i] - al[i] * aa[i]))
    u[n] = ((l2 * bet[n] + b1 * h) / (l2 + h * l1 - l2 * al[n]))
    for i in rangeWithEnd(n - 1, 0, -1):
        u[i] = al[i + 1] * u[i + 1] + bet[i + 1]
    return u


def main():
    print(f"----------------PARAMS---------------------")
    print(f"SPLIT SYMBOL : '{SPLIT_SYMBOL}'")

    print(f"E : {E}")
    count = 0
    n = START_N
    file_table = open(FILENAME, 'w')

    file_table.write(
        f"X{SPLIT_SYMBOL}Y(h){SPLIT_SYMBOL}Y(h/2){SPLIT_SYMBOL}|Y(h) - Y(h/2)|{SPLIT_SYMBOL}|Y(h/2) - Yточ|\n")
    # max|Yh-Yh/2|
    max_d = 0
    # max|Yh/2 - Yточн|
    max_t = 0

    print(f"-------------------------------------------\n")
    print(f"------------START CALCULATE----------------")

    y_arr_old = get_arr_y_k(n, get_h(n))
    while True:
        max_t = 0
        count += 1
        n *= 2
        # Шаг
        h = get_h(n)
        # новый набор значений Y
        y_arr = get_arr_y_k(n, h)
        max_d_local = 0
        for i in range(len(y_arr)):
            x_k = get_x(i, h)
            y_k = y_arr[i]
            # Разность с точным решением
            t = abs(y_k - get_y_t(x_k))
            if (max_t < t):
                max_t = t
            # Дополнительное поведение для чисел, с одинаковым шагом из предыдущего
            if i % 2 == 0:
                # Берем старый Y для того же X
                y_k_previous = y_arr_old[i // 2]
                # Разность между новым и старым
                d = abs(y_k - y_k_previous)
                if d > max_d_local:
                    max_d_local = d
                # Записываем в таблицу
                write_to_csv(file_table, x_k, y_k_previous, y_k, d, t)
            # Для всех остальных
            else:
                # Записываем в таблицу
                write_to_csv(file_table, x_k, "", y_k, "", t)
        max_d = max_d_local
        if max_d_local < E:
            break
        y_arr_old = y_arr
        file_table.write("\n\n")
    # Навёл красоты на вывод)
    print(f"--------------END CALCULATE-----------------\n")
    print(f"----------------RESULTS---------------------")
    print(f"Кол-во уменьшений шага: {count}")
    print(f"max|Y(n) - Y(n/2)| : {max_d}")
    print(f"max|Y(n/2) - Yточн| : {max_t}")
    print(f"Таблицы : {FILENAME}")
    print(f"--------------------------------------------\n")

main()
