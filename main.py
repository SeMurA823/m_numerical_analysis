# Константы

E = 0.0001
X0 = 0.
Y0 = 1.
B = 1
START_N = 4

# Настройки для записи таблицы
FILENAME = 'log.csv'
SPLIT_SYMBOL = ';'


def write_to_csv(f, x, y_h, y_h_2, max_d, max_t):
    f.write(f"{x}{SPLIT_SYMBOL}{y_h}{SPLIT_SYMBOL}{y_h_2}{SPLIT_SYMBOL}{max_d}{SPLIT_SYMBOL}{max_t}\n")


# Функция f(x,y)
def f(x, y):
    return y - (2 * x) / y


# Xi = X0 +ih
def get_x(i, h):
    return X0 + i * h


# Точное решение
def get_y_t(x):
    return (2 * x + 1) ** 0.5


def get_h(n):
    return (B - X0) / n


# Получение Y(k+1)
def get_y_k_1(x_k, y_k, h):
    k1 = f(x_k, y_k)
    k2 = f(x_k + h / 2, y_k + h * k1 / 2)
    k3 = f(x_k + h / 2, y_k + h * k2 / 2)
    k4 = f(x_k + h, y_k + h * k3)
    y = h * (k1 + 2 * k2 + 2 * k3 + k4) / 6 + y_k
    return y


def get_arr_y_k(n, h):
    y_arr = [Y0]
    for i in range(1, n + 1):
        x_k = get_x(i - 1, h)
        y_k = y_arr[len(y_arr) - 1]
        y_k_1 = get_y_k_1(x_k, y_k, h)
        y_arr.append(y_k_1)
    return y_arr


def main():
    print(f"----------------PARAMS---------------------")
    print(f"SPLIT SYMBOL : '{SPLIT_SYMBOL}'")

    print(f"E : {E}")
    count = 0
    # Уменьшаю интервал в 2 раза, увеличивая количество точек в 2 раза
    n = START_N
    file_table = open(FILENAME, 'w')
    print(f"FILE : {file_table.name}")
    file_table.write(
        f"X{SPLIT_SYMBOL}Y(h){SPLIT_SYMBOL}Y(h/2){SPLIT_SYMBOL}|Y(h) - Y(h/2)|{SPLIT_SYMBOL}|Y(h/2) - Yточ|\n")
    # max|Yn-Yn/2|
    max_d = 0
    # max|Yn/2 - Yточн|
    max_t = 0
    print(f"-------------------------------------------\n")
    print(f"------------START CALCULATE----------------")
    y_arr_old = get_arr_y_k(n, get_h(n))
    print(y_arr_old)
    while True:
        count += 1
        n *= 2
        # Шаг
        h = get_h(n)
        # новый набор значений Y
        y_arr = get_arr_y_k(n, h)
        print(y_arr)
        max_d_local = 0
        for i in range(len(y_arr)):
            x_k = get_x(i, h)
            y_k = y_arr[i]
            # Разность с точным решением
            t = abs(y_k - get_y_t(x_k))
            if t > max_t:
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

        if max_d_local > max_d:
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
