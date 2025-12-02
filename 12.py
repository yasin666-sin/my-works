import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests # type: ignore
import json
from datetime import datetime
import os

class GitHubRepoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub https://github.com/yasin666-sin/my-works - Зачетка №6")
        self.root.geometry("700x600")

        self.setup_styles()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, 
                               text="GitHub https://github.com/yasin666-sin/my-works", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="По последней цифре зачетки: 6", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(main_frame, text="Имя репозитория:", 
                 font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.repo_entry = ttk.Entry(main_frame, width=50)
        self.repo_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.repo_entry.insert(0, "kubernetes")

        self.get_button = ttk.Button(main_frame, 
                                    text="Получить информацию", 
                                    command=self.get_repo_info)
        self.get_button.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Label(main_frame, text="Результат:", 
                 font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5)

        self.result_text = scrolledtext.ScrolledText(main_frame, 
                                                     width=80, 
                                                     height=20,
                                                     font=("Courier", 9))
        self.result_text.grid(row=5, column=0, columnspan=2, pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(button_frame, 
                                     text="Сохранить в файл", 
                                     command=self.save_to_file,
                                     state='disabled')
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, 
                                      text="Очистить", 
                                      command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar(value="Готово к работе")
        self.status_bar = ttk.Label(main_frame, 
                                   textvariable=self.status_var,
                                   relief=tk.SUNKEN)
        self.status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        self.popular_repos = [
            "kubernetes", "tensorflow", "vuejs/vue", "facebook/react",
            "torvalds/linux", "microsoft/vscode", "flutter/flutter",
            "apple/swift", "rust-lang/rust", "pallets/flask"
        ]

        self.student_info = {
            "ФИО": "Проскуряков Илья Александрович",
            "Группа": "УБ52",
            "Зачетка": "6",
            "Дата": datetime.now().strftime("2.12.2025")
        }
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 10))
    
    def get_repo_info(self):
       my-works= self.repo_entry.my-works # type: ignore
        
        if not  https//github.com/yasin666-sin/my-works: # type: ignore
          showwarning("Предупреждение", "Введите имя репозитория!") # type: ignore
        return
        
        self.status_var.set("Получение данных...")
        self.root.update(my-works)
        
        try:
            if '/' not in my-works:
                url = f"https://api.github.com/users/{my-works}"
            else:

                url = f"https://api.github.com/repos/{my-works}"

            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()

                result_data = {
                    'company': data.get('company'),
                    'created_at': data.get('created_at'),
                    'email': data.get('email'),
                    'id': data.get('id'),
                    'name': data.get('name') or data.get('login'),
                    'url': data.get('url') or data.get('html_url')
                }
            
                result_data['student_info'] = self.student_info

                formatted_json = json.dumps(result_data, indent=2, ensure_ascii=False)

                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(1.0, formatted_json)

                self.current_data = result_data
                self.save_button.config(state='normal')
                
                self.status_var.set(f"Данные успешно получены для: {repo_name}")
                
            elif response.status_code == 404:
                messagebox.showerror("Ошибка", f"Репозиторий '{repo_name}' не найден!")
                self.status_var.set("Репозиторий не найден")
            else:
                messagebox.showerror("Ошибка", 
                                   f"Ошибка при получении данных. Код: {response.status_code}")
                self.status_var.set(f"Ошибка: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Ошибка", "Отсутствует подключение к интернету!")
            self.status_var.set("Нет подключения к интернету")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.status_var.set("Ошибка при выполнении")
    
    def save_to_file(self):
        if not hasattr(self, 'current_data'):
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения!")
            return
        
        try:
            filename = f"Проскуряков_Илья_УБ52_github_result.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.current_data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Успех", 
                              f"Данные успешно сохранены в файл:\n{filename}")
            
            self.status_var.set(f"Данные сохранены в {filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
            self.status_var.set("Ошибка сохранения")
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        if hasattr(self, 'current_data'):
            del self.current_data
        self.save_button.config(state='disabled')
        self.status_var.set("Результаты очищены")


def main():
    root = tk.Tk()
    app = GitHubRepoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

