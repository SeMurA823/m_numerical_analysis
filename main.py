import logging

#

# filename - имя файла с логами, если нужен, то нужно ввести название файла (Информацией о выполнении),
# туда перенаправляются все выводы с логера: logger.info, logger.debug и т.д.
# level - выбор того, что будет выводиться:
# DEBUG - выводит всё,
# INFO - выводит только выводы логера: logger.info
logging.basicConfig(level=logging.INFO, filename="logs.log", datefmt='%H:%M:%S')

logger = logging.getLogger("main.py")

# Константы
E = 0.0001
X0 = 0.
Y0 = 1.
B = 1
START_N = 4

# настройки для записи таблицы
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
        y_arr.append(get_y_k_1(x_k, y_k, h))
    return y_arr


def main():
    logger.info(f"----------------PARAMS---------------------")
    logger.info(f"SPLIT SYMBOL : '{SPLIT_SYMBOL}'")

    logger.info(f"E : {E}")
    count = 0
    # Уменьшаю интервал в 2 раза, увеличивая количество точек в 2 раза
    n = START_N
    f = open(FILENAME, 'w')
    logger.info(f"FILE : {f.name}")
    f.write(f"X{SPLIT_SYMBOL}Y(h){SPLIT_SYMBOL}Y(h/2){SPLIT_SYMBOL}|Y(h) - Y(h/2)|{SPLIT_SYMBOL}|Y(h/2) - Yточ|\n")
    # max|Yn-Yn/2|
    max_d_global = 0
    # max|Yn/2 - Yточн|
    max_t = 0
    logger.info(f"-------------------------------------------\n")
    logger.info(f"------------START CALCULATE----------------")
    y_arr = get_arr_y_k(n, get_h(n))
    logger.info(y_arr)
    while True:
        count += 1
        n *= 2
        h = get_h(n)
        y_arr_new = get_arr_y_k(n, h)
        logger.info(y_arr_new)
        max_d_local = 0
        for i in range(len(y_arr_new)):
            x_k = get_x(i, h)
            y_k = y_arr_new[i]
            t = abs(y_k - get_y_t(x_k))
            if t > max_t:
                max_t = t
            if i % 2 == 0:
                y_k_previous = y_arr[i // 2]
                d = abs(y_k - y_k_previous)
                if d > max_d_local:
                    max_d_local = d
                write_to_csv(f, x_k, y_k_previous, y_k, d, t)
            else:
                write_to_csv(f, x_k, "", y_k, "", t)

        if max_d_local > max_d_global:
            max_d_global = max_d_local
        if max_d_local < E:
            break
        y_arr = y_arr_new
        f.write("\n\n")
    # Навёл красоты на вывод)
    logger.info(f"--------------END CALCULATE-----------------\n")
    logger.info(f"----------------RESULTS---------------------")
    logger.info(f"Кол-во уменьшений шага: {count}")
    logger.info(f"max|Y(n) - Y(n/2)| : {max_d_global}")
    logger.info(f"max|Y(n/2) - Yточн| : {max_t}")
    logger.info(f"Таблицы : {FILENAME}")
    logger.info(f"--------------------------------------------\n")


main()
