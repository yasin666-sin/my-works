import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Проскуряков Илья Александрович")
        self.root.geometry("600x500")
        
        self.create_menu()

        self.tab_control = ttk.Notebook(root)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Калькулятор')
        self.tab_control.add(self.tab2, text='Чекбоксы')
        self.tab_control.add(self.tab3, text='Текст')

        self.tab_control.pack(expand=1, fill='both', padx=10, pady=10)

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить текст из файла", command=self.load_text_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def setup_tab1(self):

        title_label = ttk.Label(self.tab1, text="Простой калькулятор", 
                                font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        input_frame = ttk.Frame(self.tab1)
        input_frame.pack(pady=20)

        ttk.Label(input_frame, text="Первое число:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.num1_entry = ttk.Entry(input_frame, width=15)
        self.num1_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Операция:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.operation_var = tk.StringVar()
        self.operation_combo = ttk.Combobox(input_frame, textvariable=self.operation_var, 
                                           width=12, state='readonly')
        self.operation_combo['values'] = ('+', '-', '*', '/')
        self.operation_combo.current(0)
        self.operation_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Второе число:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.num2_entry = ttk.Entry(input_frame, width=15)
        self.num2_entry.grid(row=2, column=1, padx=5, pady=5)

        calc_button = ttk.Button(self.tab1, text="Вычислить", command=self.calculate)
        calc_button.pack(pady=10)

        self.result_label = ttk.Label(self.tab1, text="Результат: ", font=("Arial", 12))
        self.result_label.pack(pady=20)

        clear_button = ttk.Button(self.tab1, text="Очистить", command=self.clear_calculator)
        clear_button.pack(pady=5)
    
    def setup_tab2(self):

        title_label = ttk.Label(self.tab2, text="Выбор вариантов", 
                                font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        instruction_label = ttk.Label(self.tab2, text="Выберите один или несколько вариантов:")
        instruction_label.pack(pady=5)

        checkbox_frame = ttk.Frame(self.tab2)
        checkbox_frame.pack(pady=20)

        self.checkbox1_var = tk.BooleanVar()
        self.checkbox2_var = tk.BooleanVar()
        self.checkbox3_var = tk.BooleanVar()

        self.checkbox1 = ttk.Checkbutton(checkbox_frame, text="Первый вариант", 
                                        variable=self.checkbox1_var)
        self.checkbox2 = ttk.Checkbutton(checkbox_frame, text="Второй вариант", 
                                        variable=self.checkbox2_var)
        self.checkbox3 = ttk.Checkbutton(checkbox_frame, text="Третий вариант", 
                                        variable=self.checkbox3_var)

        self.checkbox1.pack(anchor='w', pady=5)
        self.checkbox2.pack(anchor='w', pady=5)
        self.checkbox3.pack(anchor='w', pady=5)

        select_button = ttk.Button(self.tab2, text="Показать выбор", command=self.show_selection)
        select_button.pack(pady=20)
    
    def setup_tab3(self):

        title_label = ttk.Label(self.tab3, text="Работа с текстом", 
                                font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        

        button_frame = ttk.Frame(self.tab3)
        button_frame.pack(pady=10, fill='x')

        load_button = ttk.Button(button_frame, text="Загрузить текст из файла", 
                                command=self.load_text_from_file)
        load_button.pack(side='left', padx=5)

        clear_button = ttk.Button(button_frame, text="Очистить текст", 
                                 command=self.clear_text)
        clear_button.pack(side='left', padx=5)

        save_button = ttk.Button(button_frame, text="Сохранить текст", 
                                command=self.save_text)
        save_button.pack(side='left', padx=5)

        self.text_area = scrolledtext.ScrolledText(self.tab3, wrap=tk.WORD, 
                                                  width=60, height=20)
        self.text_area.pack(pady=10, padx=10, fill='both', expand=True)

        self.stats_label = ttk.Label(self.tab3, text="Символов: 0 | Слов: 0 | Строк: 0")
        self.stats_label.pack(pady=5)

        self.text_area.bind('<KeyRelease>', self.update_stats)
    
    def calculate(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            operation = self.operation_var.get()
            
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
                    return
                result = num1 / num2
            else:
                messagebox.showerror("Ошибка", "Неверная операция!")
                return
            
            self.result_label.config(text=f"Результат: {result:.4f}")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def clear_calculator(self):
        self.num1_entry.delete(0, tk.END)
        self.num2_entry.delete(0, tk.END)
        self.operation_combo.current(0)
        self.result_label.config(text="Результат: ")
    
    def show_selection(self):
        selected = []
        
        if self.checkbox1_var.get():
            selected.append("первый вариант")
        if self.checkbox2_var.get():
            selected.append("второй вариант")
        if self.checkbox3_var.get():
            selected.append("третий вариант")
        
        if not selected:
            message = "1"
        else:
            message = f"Вы выбрали: {', '.join(selected)}"
        
        messagebox.showinfo("Ваш выбор", message)
    
    def load_text_from_file(self):
        file_path = filedialog.askopenfilename(
            title= 
            filetypes=[("10", "*.txt"), ("Все файлы", "*.*")]
        )
