import csv
import time

global matrix, target, m, n


def binary_search(index, left, right: int) -> int:
    # index - number of row in matrix, left - left bound, right - right bound
    mid = 0

    while left <= right:
        # вычисляем индекс серединного элемента
        mid = (right + left) // 2

        if matrix[index][mid] < target:
            left = mid + 1

        elif matrix[index][mid] > target:
            right = mid - 1

        else:
            # нашли target -> return
            return -1

    # не нашли, возвращаем наиболее близкий элемент слева к target
    return (left + right) // 2


def matrix_binary_search() -> bool:
    # наименьший элемент матрицы > target
    if matrix[0][0] > target:
        return False
    # i - row
    for i in range(m):
        if binary_search(i, 0, n - 1) == -1:
            # нашли target -> return
            return True

    return False


def matrix_ladder_search() -> bool:
    # наименьший элемент матрицы > target
    if matrix[0][0] > target:
        return False

    # i - row, j - column
    i, j = 0, n - 1
    # пока не вышли за пределы матрицы
    while j >= 0 and i < m:

        if matrix[i][j] == target:
            # нашли target -> return
            return True

        elif matrix[i][j] > target:
            # элемент > target, двигаемся влево
            j -= 1

        else:
            # элемент < target, двигаемся вниз
            i += 1

    return False


def matrix_exponential_search() -> bool:
    # наименьший элемент матрицы больше target
    if matrix[0][0] > target:
        return False

    # i - row, j - column
    i, j = 0, n - 1

    while i < m and j >= 0:
        # пока не вышли за пределы матрицы
        if matrix[i][j] == target:
            # нашли target -> return
            return True

        # элемент < target, двигаемся вниз
        if matrix[i][j] < target:
            i += 1

        # иначе двигаемся экспоненциально вправо
        elif matrix[i][j] > target:
            step = 1
            start_index = j

            # пока не найдем элемент меньше target или не выйдем за пределы матрицы
            while start_index >= 0 and matrix[i][start_index] > target:
                start_index -= step
                step *= 2

            if start_index < 0:
                start_index = 0

            # binary search в найденном интервале
            j = binary_search(i, start_index, j)

            # нашли target -> return
            if j == -1:
                return True

    return False


# среднее время работы binary search(100 испытаний)
def result_binary_search() -> int:
    average_value = 0

    for i in range(100):
        start = time.perf_counter_ns()
        result = matrix_binary_search()
        average_value += time.perf_counter_ns() - start

    return average_value // 100

# среднее время работы exponential search(100 испытаний)
def result_exponential_search() -> int:
    average_value = 0

    for i in range(100):
        start = time.perf_counter_ns()
        result = matrix_exponential_search()
        average_value += time.perf_counter_ns() - start

    return average_value // 100

# среднее время работы ladder search(100 испытаний)
def result_ladder_search() -> int:
    average_value = 0
    for i in range(100):
        start = time.perf_counter_ns()
        result = matrix_ladder_search()
        average_value += time.perf_counter_ns() - start

    return average_value // 100


def print_result_algorithms():
    global matrix, target, n, m
    # запись результатов в файл
    file = open('result.csv', 'w', encoding="UTF8", newline='')
    writer = csv.writer(file, delimiter='\t')

    bin_search = [["Binary search"], ['m', 'time(nanoseconds)']]
    exp_search_1 = [["exponential search_1"], ['m', 'time(nanoseconds)']]
    lad_search = [["ladder search"], ['m', 'time(nanoseconds)']]
    exp_search_2 = [["exponential search_2"], ['m', 'time(nanoseconds)']]
    n = 2 ** 13

    for d in range(1, 14):
        m = 2 ** d
        target = 2 * n + 1
        matrix = [[(n // m * i + j) * 2 for j in range(n)] for i in range(m)]
        bin_search.append([m, result_binary_search()])
        lad_search.append([m, result_ladder_search()])
        exp_search_1.append([m, result_exponential_search()])

        matrix = [[(n // m * (i + 1) * (j + 1)) * 2 for j in range(n)] for i in range(m)]
        target = 16 * n + 1
        exp_search_2.append([m, result_exponential_search()])

    writer.writerows(bin_search)
    writer.writerow(['\n'])
    writer.writerows(exp_search_1)
    writer.writerow(['\n'])
    writer.writerows(lad_search)
    writer.writerow(['\n'])
    writer.writerows(exp_search_2)

    file.close()


print_result_algorithms()
