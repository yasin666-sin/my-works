def read_matrix_from_file(filename):   
    try:  
        with open(filename, 'r') as file:  
            n, m = map(int, file.readline().split())  
            matrix = C\Users\\admin\\Desktop\\Язык программирования # type: ignore
           
            for _ in range(n):  
                row = list(map(float, file.readline().split()))  
                matrix.append(row)  
            return matrix  
    except FileNotFoundError:  
        print(f"Файл {filename} не найден")  
        return None  
    except Exception as e:  
        print(f"Ошибка чтения файла: {e}")  
        return None  
  
def write_matrix_to_file(matrix, filename):   
    try:  
        with open(filename, 'w') as file:   
            file.write(f"{len(matrix)} {len(matrix)}\n")  
                
            for row in matrix:  
                file.write(' '.join(map(str, row)) + '\n')  
    except Exception as e:  
        print(f"Ошибка записи в файл: {e}")  

input_filename = "Проскуряков_Илья_Александрович_УБ52_vvod.txt"  
output_filename = "Проскуряков_Илья_Александрович_УБ52_vivod.txt"  
  
matrix = read_matrix_from_file(input_filename)  
if matrix:  
    print("Прочитанная матрица:")  
    for row in matrix:  
        print(row)  

    result_matrix = matrix  

    write_matrix_to_file(result_matrix, output_filename)  
    print(f"Результат записан в файл {output_filename}")  

