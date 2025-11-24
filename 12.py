mport tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import os
import threading
import datetime

# --- КОНФИГУРАЦИЯ ---
FIO = "Проскуряков Илья Александрович"
GROUP = "ПИ23-1"  # Замените на вашу фактическую группу!
# Последняя цифра зачетки для определения варианта.
# Например, если зачетка заканчивается на 5, ставим 5.
ZACHETKA_LAST_DIGIT = 3 # <<<<< ВВЕДИТЕ СЮДА ПОСЛЕДНЮЮ ЦИФРУ ВАШЕЙ ЗАЧЕТКИ!

# GitHub Personal Access Token (PAT)
# ОЧЕНЬ ВАЖНО: Замените 'YOUR_GITHUB_TOKEN_HERE' на ваш реальный токен!
# Инструкции по получению токена выше.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN_HERE") 
# Рекомендуется использовать переменную окружения: GITHUB_TOKEN=ghp_... python your_script.py
# Если токена нет или он некорректен, запросы могут быть ограничены.

# Формирование базового имени файла
fio_parts = FIO.split()
surname = fio_parts[0]
initials = "".join([part[0] for part in fio_parts[1:] if part])
FILENAME_BASE = f"{surname}_{initials}_{GROUP}"
OUTPUT_FILENAME_VARIANT = f"{FILENAME_BASE}_variant_owner_info.json"

# Список популярных репозиториев (owner, repo_name)
# Используется для определения "варианта" и как примеры
POPULAR_REPOS = [
    ("tensorflow", "tensorflow"),
    ("facebook", "react-native"),
    ("kubernetes", "kubernetes"),
    ("twbs", "bootstrap"),
    ("microsoft", "vscode"),
    ("vuejs", "vue"),
    ("angular", "angular"),
    ("pallets", "flask"),
    ("golang", "go"),
    ("d3", "d3")
]

# --- Функции для работы с GitHub API ---

def get_github_headers(token):
    """Возвращает заголовок для авторизации GitHub API."""
    if token and token != "YOUR_GITHUB_TOKEN_HERE":
        return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    return {"Accept": "application/vnd.github.v3+json"}

def get_repo_owner_info(owner, repo_name, token):
    """
    Получает информацию о владельце репозитория GitHub.
    Возвращает словарь с запрошенными полями или None в случае ошибки.
    """
    headers = get_github_headers(token)
    
    try:
        # 1. Запрос информации о репозитории для получения URL владельца
        repo_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status() # Вызывает исключение для ошибок HTTP (4xx или 5xx)
        repo_data = repo_response.json()

        if 'owner' not in repo_data or 'url' not in repo_data['owner']:
            return None, "Не удалось найти информацию о владельце в данных репозитория."

        owner_api_url = repo_data['owner']['url'] # Это URL для API пользователя

        # 2. Запрос детальной информации о владельце (пользователе/организации)
        owner_response = requests.get(owner_api_url, headers=headers)
        owner_response.raise_for_status()
        owner_data = owner_response.json()

        # Фильтрация и форматирование данных согласно заданию
        filtered_info = {
            'company': owner_data.get('company'),
            'created_at': owner_data.get('created_at'),
            'email': owner_data.get('email'),
            'id': owner_data.get('id'),
            'name': owner_data.get('name') if owner_data.get('name') else owner_data.get('login'), # 'name' может быть None, используем 'login'
            'url': owner_data.get('url')
        }
        return filtered_info, None

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code
        if status_code == 404:
            return None, f"Репозиторий '{owner}/{repo_name}' не найден. Проверьте правильность написания."
        elif status_code == 403 and 'X-RateLimit-Remaining' in http_err.response.headers and http_err.response.headers['X-RateLimit-Remaining'] == '0':
            return None, "Превышен лимит запросов к GitHub API. Пожалуйста, используйте Personal Access Token."
        return None, f"Ошибка HTTP при запросе GitHub API: {status_code} - {http_err.response.text}"
    except requests.exceptions.ConnectionError:
        return None, "Ошибка соединения: проверьте ваше интернет-подключение."
    except requests.exceptions.Timeout:
        return None, "Время ожидания запроса истекло."
    except requests.exceptions.RequestException as req_err:
        return None, f"Произошла непредвиденная ошибка запроса: {req_err}"
    except json.JSONDecodeError:
        return None, "Ошибка парсинга JSON ответа от GitHub API."
    except Exception as e:
        return None, f"Произошла непредвиденная ошибка: {e}"

# --- Функция для сохранения информации о варианте ---

def save_variant_info_to_file(fio, group, zachetka_last_digit):
    """
    Сохраняет информацию о владельце репозитория для заданного варианта в JSON-файл.
    """
    variant_index = zachetka_last_digit % len(POPULAR_REPOS)
    owner, repo_name = POPULAR_REPOS[variant_index]

    print(f"Определен репозиторий для варианта (последняя цифра зачетки {zachetka_last_digit}): {owner}/{repo_name}")
    
    owner_info, error = get_repo_owner_info(owner, repo_name, GITHUB_TOKEN)

    if owner_info:
        try:
            with open(OUTPUT_FILENAME_VARIANT, 'w', encoding='utf-8') as f:
                json.dump(owner_info, f, indent=2, ensure_ascii=False)
            print(f"Информация о владельце репозитория '{owner}/{repo_name}' сохранена в '{OUTPUT_FILENAME_VARIANT}'")
        except IOError as e:
            print(f"Ошибка при записи в файл '{OUTPUT_FILENAME_VARIANT}': {e}")
    else:
        print(f"Не удалось получить информацию о владельце репозитория '{owner}/{repo_name}' для файла: {error}")

# --- Графический интерфейс ---

class GitHubOwnerInfoApp:
    def __init__(self, master):
        self.master = master
        master.title(f"GitHub Owner Info App - {FIO} ({GROUP})")
        master.geometry("700x550") # Устанавливаем размер окна по умолчанию

        # Инструкция и поле ввода
        self.label = tk.Label(master, text="Введите имя репозитория (формат: владелец/репозиторий), например, 'tensorflow/tensorflow':", wraplength=680)
        self.label.pack(pady=10)

        self.repo_entry = tk.Entry(master, width=60)
        self.repo_entry.pack(pady=5)
        self.repo_entry.bind("<Return>", lambda event: self.start_search()) # Поиск по Enter

        self.search_button = tk.Button(master, text="Получить информацию о владельце", command=self.start_search)
        self.search_button.pack(pady=10)

        # Поле для вывода результата
        self.result_label = tk.Label(master, text="Результат:")
        self.result_label.pack()

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20, state='disabled', font=('Consolas', 10))
        self.result_text.pack(pady=10)

        # Строка состояния
        self.status_label = tk.Label(master, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Примеры репозиториев
        self.examples_label = tk.Label(master, text="Примеры: tensorflow/tensorflow, facebook/react-native, kubernetes/kubernetes")
        self.examples_label.pack(pady=5)

    def start_search(self):
        """Запускает поиск в отдельном потоке, чтобы не блокировать GUI."""
        repo_full_name = self.repo_entry.get().strip()
        if not repo_full_name:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите имя репозитория в формате 'владелец/репозиторий'.")
            return
        
        self.status_label.config(text="Загрузка данных...")
        self.set_result_text("Запрос к GitHub API...")
        self.search_button.config(state='disabled') # Отключаем кнопку на время запроса

        # Запускаем API-запрос в отдельном потоке
        threading.Thread(target=self._perform_search, args=(repo_full_name,)).start()

    def _perform_search(self, repo_full_name):
        """Выполняет фактический API-запрос и обновляет GUI."""
        try:
            parts = repo_full_name.split('/')
            if len(parts) != 2:
                raise ValueError("Некорректный формат. Используйте 'владелец/репозиторий'.")
            owner, repo_name = parts[0], parts[1]

            owner_info, error = get_repo_owner_info(owner, repo_name, GITHUB_TOKEN)

            if owner_info:
                # Обновляем GUI в основном потоке Tkinter
                self.master.after(0, self.update_gui_results, owner_info)
            else:
                self.master.after(0, self.update_gui_error, error)

        except ValueError as e:
            self.master.after(0, self.update_gui_error, str(e))
        except Exception as e:
            self.master.after(0, self.update_gui_error, f"Произошла непредвиденная ошибка: {e}")
        finally:
            self.master.after(0, lambda: self.search_button.config(state='normal')) # Включаем кнопку обратно

    def set_result_text(self, text):
        """Устанавливает текст в поле результата."""
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state='disabled')

    def update_gui_results(self, owner_info):
        """Обновляет GUI с успешным результатом."""
        self.set_result_text(json.dumps(owner_info, indent=2, ensure_ascii=False))
        self.status_label.config(text="Готово. Данные получены.")

    def update_gui_error(self, message):
        """Обновляет GUI с сообщением об ошибке."""
        self.set_result_text(f"Ошибка:\n{message}")
        self.status_label.config(text=f"Ошибка: {message}", fg="red")
        messagebox.showerror("Ошибка", message)


# --- Точка входа в программу ---
if __name__ == "__main__":
    # Сохраняем информацию о владельце репозитория для вашего варианта
    print("--- Подготовка файла для варианта ---")
    if GITHUB_TOKEN == "YOUR_GITHUB_TOKEN_HERE":
        print("ВНИМАНИЕ: GitHub Personal Access Token не установлен. Запросы могут быть ограничены. "
              "Пожалуйста, замените 'YOUR_GITHUB_TOKEN_HERE' на ваш токен.")
    save_variant_info_to_file(FIO, GROUP, ZACHETKA_LAST_DIGIT)
    print("--- Запуск графического интерфейса ---")
    
    # Создание и запуск графического окна
    root = tk.Tk()
    app = GitHubOwnerInfoApp(root)
    root.mainloop()
