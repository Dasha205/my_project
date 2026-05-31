import tkinter as tk
from tkinter import ttk

class OrderApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Работа с заказами")
        self.root.geometry("950x550")
        self.root.resizable(False, False)

        self.customer_var = tk.StringVar(value="Все")
        self.sort_field = tk.StringVar(value="")
        self.sort_order = tk.StringVar(value="ASC")
        self.search_var = tk.StringVar()
        self.current_items = []

        self.create_widgets()
        self.load_customers()
        self.load_data()

    def create_widgets(self):
        control_frame = ttk.LabelFrame(self.root, text="Управление", padding=10)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Строка 1: Выбор заказчика
        row1 = ttk.Frame(control_frame)
        row1.pack(fill="x", pady=5)
        
        ttk.Label(row1, text="Выберите заказчика:", font=("Arial", 10)).pack(side="left", padx=5)
        self.cb_customer = ttk.Combobox(row1, textvariable=self.customer_var, width=25, state="readonly")
        self.cb_customer.pack(side="left", padx=5)
        
        ttk.Button(row1, text="Фильтровать", command=self.filter_data, width=12).pack(side="left", padx=5)
        ttk.Button(row1, text="Показать все", command=self.show_all, width=12).pack(side="left", padx=5)

        # Строка 2: Поиск
        row2 = ttk.Frame(control_frame)
        row2.pack(fill="x", pady=5)
        
        ttk.Label(row2, text="Введите строку поиска:", font=("Arial", 10)).pack(side="left", padx=5)
        self.search_entry = ttk.Entry(row2, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(row2, text="Найти", command=self.search_data, width=10).pack(side="left", padx=5)

        # Строка 3: Сортировка
        row3 = ttk.Frame(control_frame)
        row3.pack(fill="x", pady=10)
        
        ttk.Label(row3, text="Выберите поле для сортировки:", font=("Arial", 10)).pack(side="left", padx=5)
        
        sort_frame = ttk.Frame(row3)
        sort_frame.pack(side="left", padx=10)
        
        self.rb_customer = ttk.Radiobutton(sort_frame, text="Заказчик", variable=self.sort_field, 
                                           value="customer", command=self.load_data)
        self.rb_customer.pack(side="left", padx=5)
        
        self.rb_date = ttk.Radiobutton(sort_frame, text="Дата заказа", variable=self.sort_field, 
                                       value="date", command=self.load_data)
        self.rb_date.pack(side="left", padx=5)
        
        self.rb_sum = ttk.Radiobutton(sort_frame, text="Сумма заказа", variable=self.sort_field, 
                                      value="sum", command=self.load_data)
        self.rb_sum.pack(side="left", padx=5)
        
        order_frame = ttk.Frame(row3)
        order_frame.pack(side="left", padx=20)
        
        ttk.Radiobutton(order_frame, text="По возрастанию", variable=self.sort_order, 
                       value="ASC", command=self.load_data).pack(side="left", padx=5)
        ttk.Radiobutton(order_frame, text="По убыванию", variable=self.sort_order, 
                       value="DESC", command=self.load_data).pack(side="left", padx=5)

        # Таблица
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("customer", "city", "phone", "date", "sum")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("customer", text="Заказчик")
        self.tree.heading("city", text="Город")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("date", text="Дата заказа")
        self.tree.heading("sum", text="Сумма заказа")
        
        self.tree.column("customer", width=180)
        self.tree.column("city", width=120)
        self.tree.column("phone", width=130)
        self.tree.column("date", width=110)
        self.tree.column("sum", width=120)
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Итоги
        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x", padx=10, pady=10)
        
        self.lbl_count = ttk.Label(bottom, text="Всего заказов: 0", font=("Arial", 10, "bold"))
        self.lbl_count.pack(side="left", padx=10)
        
        self.lbl_sum = ttk.Label(bottom, text="Общая сумма: 0.00", font=("Arial", 10, "bold"))
        self.lbl_sum.pack(side="left", padx=10)

    def load_customers(self):
        customers = self.db.get_customers()
        self.cb_customer['values'] = ["Все"] + customers

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        orders = self.db.get_orders(self.customer_var.get(), self.sort_field.get(), self.sort_order.get())
        
        total = 0
        self.current_items = []
        
        for order in orders:
            date_str = str(order[3])
            if "-" in date_str:
                parts = date_str.split("-")
                date_str = f"{parts[2]}.{parts[1]}.{parts[0]}"
            
            item = self.tree.insert("", "end", values=(
                order[0], order[1], order[2], date_str, f"{order[4]:.2f}"
            ))
            self.current_items.append(item)
            total += order[4]
        
        self.lbl_count.config(text=f"Всего заказов: {len(orders)}")
        self.lbl_sum.config(text=f"Общая сумма: {total:,.2f}")

    def filter_data(self):
        self.load_data()

    def show_all(self):
        self.customer_var.set("Все")
        self.search_var.set("")
        self.load_data()

    def search_data(self):
        for item in self.current_items:
            self.tree.tag_configure(f"bg_{item}", background="")
            self.tree.item(item, tags=())
        
        if not self.search_var.get():
            return
        
        search_text = self.search_var.get().lower()
        found = 0
        
        for item in self.current_items:
            values = self.tree.item(item)['values']
            for val in values:
                if search_text in str(val).lower():
                    self.tree.tag_configure(f"bg_{item}", background="yellow")
                    self.tree.item(item, tags=(f"bg_{item}",))
                    found += 1
                    break
