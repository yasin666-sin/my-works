
class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Проскуряков Илья Александрович")
        self.root.geometry("800x600") # Начальный размер окна

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Создаем Notebook (вкладки)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10) # Добавляем отступы

        # --- Первая вкладка: Калькулятор ---
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Калькулятор")
        self.create_calculator_tab()

        # --- Вторая вкладка: Чекбоксы ---
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Чекбоксы")
        self.create_checkbox_tab()

        # --- Третья вкладка: Работа с текстом ---
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Текст")
        self.create_text_tab()

    def create_calculator_tab(self):
        # Используем grid для размещения элементов
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.columnconfigure(1, weight=1)
        self.tab1.columnconfigure(2, weight=1)
        self.tab1.columnconfigure(3, weight=1)

        tk.Label(self.tab1, text="Число 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.num1_entry = tk.Entry(self.tab1, width=15)
        self.num1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.tab1, text="Операция:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.operator_combo = ttk.Combobox(self.tab1, values=["+", "-", "*", "/"], width=10)
        self.operator_combo.set("+") # Устанавливаем оператор по умолчанию
        self.operator_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.tab1, text="Число 2:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.num2_entry = tk.Entry(self.tab1, width=15)
        self.num2_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(self.tab1, text="Вычислить", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Label(self.tab1, text="Результат:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.result_label = tk.Label(self.tab1, text="", font=("Arial", 12, "bold"))
        self.result_label.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    def calculate(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            operator = self.operator_combo.get()
            result = 0

            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 != 0:
                    result = num1 / num2
                else:
                    messagebox.showerror("Ошибка", "Деление на ноль!")
                    self.result_label.config(text="Ошибка")
                    return
            self.result_label.config(text=f"{result:.2f}") # Форматируем до двух знаков после запятой
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числа.")
            self.result_label.config(text="Ошибка")
        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", f"Произошла ошибка: {e}")
            self.result_label.config(text="Ошибка")

    def create_checkbox_tab(self):
        self.var1 = tk.BooleanVar()
        self.var2 = tk.BooleanVar()
        self.var3 = tk.BooleanVar()

        ttk.Checkbutton(self.tab2, text="Первый", variable=self.var1).pack(pady=5, anchor="w", padx=20)
        ttk.Checkbutton(self.tab2, text="Второй", variable=self.var2).pack(pady=5, anchor="w", padx=20)
        ttk.Checkbutton(self.tab2, text="Третий", variable=self.var3).pack(pady=5, anchor="w", padx=20)

        ttk.Button(self.tab2, text="Показать выбор", command=self.show_checkbox_selection).pack(pady=20)

    def show_checkbox_selection(self):
        selected_options = []
        if self.var1.get():
            selected_options.append("Первый")
        if self.var2.get():
            selected_options.append("Второй")
        if self.var3.get():
            selected_options.append("Третий")

        if selected_options:
            messagebox.showinfo("Ваш выбор", f"Вы выбрали: {', '.join(selected_options)}")
        else:
            messagebox.showinfo("Ваш выбор", "Вы ничего не выбрали.")

    def create_text_tab(self):
        self.text_widget = tk.Text(self.tab3, wrap="word", padx=10, pady=10)
        self.text_widget.pack(expand=True, fill="both")

        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(self.text_widget, command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=scrollbar.set)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Загрузить текст из файла", command=self.load_text_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

    def load_text_from_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_widget.delete(1.0, tk.END) # Удаляем весь текущий текст
            self.text_widget.insert(tk.END, content) # Вставляем новый текст
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл не найден: {filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
