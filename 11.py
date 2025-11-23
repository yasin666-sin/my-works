import os

# --- КОНФИГУРАЦИЯ ---
FIO = "Проскуряков Илья Александрович"
GROUP = "ПИ23-1" # Замените на вашу фактическую группу!

# Формирование базового имени файла
fio_parts = FIO.split()
surname = fio_parts[0]
initials = ""
if len(fio_parts) > 1:
    initials += fio_parts[1][0]
if len(fio_parts) > 2:
    initials += fio_parts[2][0]

FILENAME_BASE = f"{surname}_{initials}_{GROUP}"
INPUT_FILENAME = f"{FILENAME_BASE}_vvod.txt"
OUTPUT_FILENAME = f"{FILENAME_BASE}_vivod.txt"

# --- Вспомогательные функции для работы с матрицами ---

def read_matrix_from_file(filename):
    """
    Считывает матрицы из указанного файла.
    Возвращает словарь, где ключи - названия матриц (например, 'MATRIX_A'),
    а значения - словари с 'matrix' (список списков), 'rows', 'cols'.
    """
    matrices_data = {}
    current_matrix_name = None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line or line.startswith('#'): # Пропускаем пустые строки и комментарии
                    i += 1
                    continue

                if line.startswith("MATRIX_"):
                    current_matrix_name = line
                    matrices_data[current_matrix_name] = {'matrix': [], 'rows': 0, 'cols': 0}
                    i += 1
                    
                    # Читаем размеры
                    if i < len(lines):
                        dims_line = lines[i].strip()
                        try:
                            rows, cols = map(int, dims_line.split())
                            matrices_data[current_matrix_name]['rows'] = rows
                            matrices_data[current_matrix_name]['cols'] = cols
                            i += 1
                            
                            # Читаем данные матрицы
                            for r_idx in range(rows):
                                if i < len(lines):
                                    row_data_str = lines[i].strip()
                                    if not row_data_str: # Пропускаем пустые строки данных, если они есть
                                        i += 1
                                        continue
                                    row_data = list(map(int, row_data_str.split()))
                                    if len(row_data) != cols:
                                        raise ValueError(
                                            f"Ошибка чтения матрицы {current_matrix_name}: "
                                            f"Ожидалось {cols} столбцов, получено {len(row_data)} в строке данных {r_idx+1}."
                                        )
                                    matrices_data[current_matrix_name]['matrix'].append(row_data)
                                    i += 1
                                else:
                                    raise ValueError(f"Ошибка чтения матрицы {current_matrix_name}: Недостаточно строк данных.")
                            
                            if len(matrices_data[current_matrix_name]['matrix']) != rows:
                                raise ValueError(f"Ошибка чтения матрицы {current_matrix_name}: Ожидалось {rows} строк данных, получено {len(matrices_data[current_matrix_name]['matrix'])}.")

                        except ValueError as e:
                            print(f"Ошибка формата данных в файле {filename} для {current_matrix_name}: {e}")
                            return None
                        except IndexError:
                            print(f"Ошибка: Некорректный формат файла для матрицы {current_matrix_name} (отсутствуют размеры или данные).")
                            return None
                    else:
                        print(f"Ошибка: Некорректный формат файла для матрицы {current_matrix_name} (отсутствуют размеры).")
                        return None
                else:
                    i += 1 # Если не заголовок MATRIX_, просто пропускаем
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при чтении файла '{filename}': {e}")
        return None

    return matrices_data

def write_matrix_to_file(f_out, matrix, name, rows, cols):
    """
    Записывает матрицу в файл.
    """
    f_out.write(f"Матрица {name} ({rows}x{cols}):\n")
    for row in matrix:
        f_out.write(" ".join(map(str, row)) + "\n")
    f_out.write("\n")

def add_matrices(m1_data, m2_data):
    """
    Выполняет сложение двух матриц.
    Возвращает новую матрицу или None, если размеры несовместимы.
    """
    m1, rows1, cols1 = m1_data['matrix'], m1_data['rows'], m1_data['cols']
    m2, rows2, cols2 = m2_data['matrix'], m2_data['rows'], m2_data['cols']

    if rows1 != rows2 or cols1 != cols2:
        return None, f"Размеры матриц несовместимы для сложения ({rows1}x{cols1} и {rows2}x{cols2})."

    result = [[0 for _ in range(cols1)] for _ in range(rows1)]
    for i in range(rows1):
        for j in range(cols1):
            result[i][j] = m1[i][j] + m2[i][j]
    return {'matrix': result, 'rows': rows1, 'cols': cols1}, None

def multiply_matrices(m1_data, m2_data):
    """
    Выполняет умножение двух матриц.
    Возвращает новую матрицу или None, если размеры несовместимы.
    """
    m1, rows1, cols1 = m1_data['matrix'], m1_data['rows'], m1_data['cols']
    m2, rows2, cols2 = m2_data['matrix'], m2_data['rows'], m2_data['cols']

    if cols1 != rows2:
        return None, f"Размеры матриц несовместимы для умножения ({rows1}x{cols1} и {rows2}x{cols2})."

    result_rows = rows1
    result_cols = cols2
    result = [[0 for _ in range(result_cols)] for _ in range(result_rows)]

    for i in range(result_rows):
        for j in range(result_cols):
            for k in range(cols1): # Или rows2, они одинаковые
                result[i][j] += m1[i][k] * m2[k][j]
    return {'matrix': result, 'rows': result_rows, 'cols': result_cols}, None

def create_dummy_input_file(filename):
    """
    Создает файл с демонстрационными данными для ввода.
    """
    if os.path.exists(filename):
        print(f"Файл '{filename}' уже существует. Пропускаем создание демонстрационных данных.")
        return

    print(f"Создаем демонстрационный входной файл: '{filename}'")
    with open(filename, 'w', encoding='utf-8') as f_out:
        f_out.write("# Файл для ввода данных для практической работы №8\n")
        f_out.write("# ФИО: Проскуряков Илья Александрович\n")
        f_out.write("# Группа: ПИ23-1\n\n")

        f_out.write("MATRIX_A\n")
        f_out.write("2 3\n")
        f_out.write("1 2 3\n")
        f_out.write("4 5 6\n\n")

        f_out.write("MATRIX_B\n")
        f_out.write("3 2\n")
        f_out.write("7 8\n")
        f_out.write("9 10\n")
        f_out.write("11 12\n\n")

        f_out.write("MATRIX_C\n")
        f_out.write("2 3\n")
        f_out.write("10 20 30\n")
        f_out.write("40 50 60\n")
    print("Демонстрационный файл успешно создан.")


# --- Основная логика программы ---

def main():
    print(f"Запускаем программу для ФИО: {FIO}, Группа: {GROUP}")
    print(f"Входной файл: {INPUT_FILENAME}")
    print(f"Выходной файл: {OUTPUT_FILENAME}\n")

    # 1. Создать или проверить наличие входного файла с данными
    create_dummy_input_file(INPUT_FILENAME)
    
    # 2. Считать данные матриц из файла
    print("Чтение матриц из входного файла...")
    matrices_data = read_matrix_from_file(INPUT_FILENAME)

    if not matrices_data:
        print("Не удалось прочитать матрицы. Завершение работы.")
        return

    matrix_a = matrices_data.get('MATRIX_A')
    matrix_b = matrices_data.get('MATRIX_B')
    matrix_c = matrices_data.get('MATRIX_C')

    if not all([matrix_a, matrix_b, matrix_c]):
        print("Ошибка: Не все необходимые матрицы (MATRIX_A, MATRIX_B, MATRIX_C) были найдены во входном файле.")
        return

    print("Матрицы успешно прочитаны.")

    # 3. Выполнить операции и записать результаты в выходной файл
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f_out:
            f_out.write("Результаты выполнения заданий практической работы №8\n")
            f_out.write(f"ФИО: {FIO}\n")
            f_out.write(f"Группа: {GROUP}\n")
            f_out.write(f"Дата выполнения: {os.path.basename(OUTPUT_FILENAME).split('_')[0]} (Пример)\n\n") # Пример даты из имени файла

            f_out.write("--- Исходные матрицы ---\n")
            write_matrix_to_file(f_out, matrix_a['matrix'], "A", matrix_a['rows'], matrix_a['cols'])
            write_matrix_to_file(f_out, matrix_b['matrix'], "B", matrix_b['rows'], matrix_b['cols'])
            write_matrix_to_file(f_out, matrix_c['matrix'], "C", matrix_c['rows'], matrix_c['cols'])

            f_out.write("--- Операция: Сложение (A + C) ---\n")
            result_add, error_add = add_matrices(matrix_a, matrix_c)
            if result_add:
                write_matrix_to_file(f_out, result_add['matrix'], "A + C", result_add['rows'], result_add['cols'])
            else:
                f_out.write(f"Ошибка сложения: {error_add}\n\n")

            f_out.write("--- Операция: Умножение (A * B) ---\n")
            result_mul, error_mul = multiply_matrices(matrix_a, matrix_b)
            if result_mul:
                write_matrix_to_file(f_out, result_mul['matrix'], "A * B", result_mul['rows'], result_mul['cols'])
            else:
                f_out.write(f"Ошибка умножения: {error_mul}\n\n")

        print(f"\nРезультаты успешно записаны в файл: '{OUTPUT_FILENAME}'")

    except Exception as e:
        print(f"Произошла ошибка при записи результатов в файл '{OUTPUT_FILENAME}': {e}")

if __name__ == "__main__":
    main()
