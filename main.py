import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from DB_connect import connect

class MainApp:
    def __init__(self):
        self.App = tk.Tk()
        self.App.geometry("1000x500")
        self.App.title("Работа с заказами")

        self.MainFrame = tk.Frame(self.App, bg="white")
        self.MainFrame.pack(fill="both", expand=True)

        self.TopFrame = tk.Frame(self.MainFrame, bg="white")
        self.TopFrame.pack(fill="x", expand=False, side="top")

        self.Lbl1 = tk.Label(self.TopFrame, text="Выберите заказчика", bg="white", font=("Arial", 10, "bold"))
        self.Lbl1.grid(row=0, column=0, padx=10, pady=10)

        self.Lbl2 = tk.Label(self.TopFrame, text="Введите строку поиска", bg="white", font=("Arial", 10, "bold"))
        self.Lbl2.grid(row=1, column=0, padx=10, pady=10)

        self.Combo = ttk.Combobox(self.TopFrame, width=13, height=60, font=("Arial", 12))
        self.Combo.grid(row=0, column=1, padx=10, pady=10)

        self.FindEntry = tk.Entry(self.TopFrame, width=10, font=("Arial", 12), bd=0,
                                  highlightbackground="gray",
                                  highlightcolor="blue",
                                  highlightthickness=2)
        self.FindEntry.grid(row=1, column=1, padx=10, pady=10)

        self.FiltrBtn = tk.Button(self.TopFrame, width=14, height=2, text="Фильтровать", font=("Arial", 9),
                                  command=self.filtration)
        self.FiltrBtn.grid(row=0, column=2, padx=10, pady=10)

        self.ShowAllBtn = tk.Button(self.TopFrame, width=14, height=2, text="Показать все", font=("Arial", 9),
                                    command=self.get_table_data)
        self.ShowAllBtn.grid(row=0, column=3, padx=10, pady=10)

        self.FindBtn = tk.Button(self.TopFrame, width=14, height=2, text="Найти", font=("Arial", 9),
                                 command=self.search_data)
        self.FindBtn.grid(row=1, column=2, padx=10, pady=10)

        self.Lbl3 = tk.Label(self.TopFrame, text="Выберите поле для сортировки", bg="white", font=("Arial", 10, "bold"))
        self.Lbl3.grid(row=0, column=4, padx=5, pady=5)

        self.ComboSort = ttk.Combobox(self.TopFrame, width=13, height=60, font=("Arial", 12))
        self.ComboSort.grid(row=1, column=4, padx=10, pady=10)

        self.ComboSort["values"] = ("-", "Заказчик", "Дата заказа", "Сумма заказа")
        self.ComboSort.current(0)

        self.sort_direction = tk.StringVar(value="asc")

        self.RadioSort1 = tk.Radiobutton(self.TopFrame, text="По возрастанию", bg="white", font=("Arial", 10, "bold"),
                                         value="asc",
                                         variable=self.sort_direction, command=self.sort_table_data)
        self.RadioSort1.grid(row=0, column=5, padx=5)

        self.RadioSort2 = tk.Radiobutton(self.TopFrame, text="По убыванию", bg="white", font=("Arial", 10, "bold"),
                                         value="desc",
                                         variable=self.sort_direction, command=self.sort_table_data)
        self.RadioSort2.grid(row=1, column=5, padx=5)

        self.ComboSort.bind("<<ComboboxSelected>>", self.sort_table_data)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.BottomFrame = tk.Frame(self.MainFrame, bg="white")
        self.BottomFrame.pack(fill="x", expand=False, side="bottom")

        self.CostumerTable = ttk.Treeview(self.BottomFrame, columns=("col1", "col2", "col3", "col4", "col5"),
                                          show="headings")

        self.CostumerTable.heading("col1", text="Заказчик", anchor="center")
        self.CostumerTable.heading("col2", text="Город", anchor="center")
        self.CostumerTable.heading("col3", text="Телефон", anchor="center")
        self.CostumerTable.heading("col4", text="Дата заказа", anchor="center")
        self.CostumerTable.heading("col5", text="Сумма заказа", anchor="center")

        self.CostumerTable.column("col1", width=200, anchor="center")
        self.CostumerTable.column("col2", width=150, anchor="center")
        self.CostumerTable.column("col3", width=150, anchor="center")
        self.CostumerTable.column("col4", width=120, anchor="center")
        self.CostumerTable.column("col5", width=120, anchor="center")

        self.CostumerTable.grid(row=0, column=0, padx=10, pady=10)

        self.countLbl = tk.Label(self.BottomFrame, text="", bg="white", font=("Arial", 10, "bold"))
        self.countLbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.sumLbl = tk.Label(self.BottomFrame, text="Общая сумма: ", bg="white", font=("Arial", 10, "bold"))
        self.sumLbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def get_table_data(self):
        for row_id in self.CostumerTable.get_children():
            self.CostumerTable.delete(row_id)
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("select * from orders_report_view")
        result = cursor.fetchall()
        for row in result:
            self.CostumerTable.insert('', 'end', values=tuple(row))
        cursor.close()
        conn.close()
        self.get_stats_data()

    def get_stats_data(self):
        total_amount = 0
        count_order = 0

        is_searching = bool(self.FindEntry.get().strip())

        for row_id in self.CostumerTable.get_children():
            item = self.CostumerTable.item(row_id)

            if is_searching and 'highlight' not in item['tags']:
                continue

            total_amount += float(item['values'][4])
            count_order += 1

        self.countLbl['text'] = f"Всего заказов: {count_order}"
        self.sumLbl['text'] = f"Общая сумма: {total_amount}"

    def get_combo_data(self):
        conn = connect()
        cursor = conn.cursor()
        customers = []
        cursor.execute("select distinct customer_name from orders_report_view")
        rows = cursor.fetchall()
        for row in rows:
            customers.append(row[0])
        self.Combo['values'] = customers
        self.Combo.current(0)
        cursor.close()
        conn.close()

    def sort_table_data(self, event=None):
        mapping = {"Заказчик": 0, "Дата заказа": 3, "Сумма заказа": 4}
        if self.ComboSort.get() not in mapping:
            return

        col_idx = mapping[self.ComboSort.get()]

        data = [(self.CostumerTable.item(idx, "values"), idx) for idx in self.CostumerTable.get_children()]

        data.sort(key=lambda x: float(x[0][col_idx]) if col_idx == 4 else x[0][col_idx],
                  reverse=(self.sort_direction.get() == "desc"))

        for i, (_, idx) in enumerate(data):
            self.CostumerTable.move(idx, '', i)

    def search_data(self):
        conn = connect()
        cursor = conn.cursor()
        user_input = self.FindEntry.get().strip().lower()

        if not user_input:
            self.get_table_data()
            return

        self.CostumerTable.tag_configure('highlight', background='#FFFFCC', foreground='black')

        for row_id in self.CostumerTable.get_children():
            self.CostumerTable.delete(row_id)

        cursor.execute("SELECT * FROM orders_report_view")
        rows = cursor.fetchall()

        for row in rows:
            row_text_str = " ".join(str(item).lower() for item in row if item is not None)

            if user_input in row_text_str:
                self.CostumerTable.insert('', 'end', values=tuple(row), tags=('highlight',))
            else:
                self.CostumerTable.insert('', 'end', values=tuple(row))
        self.get_stats_data()
        cursor.close()
        conn.close()

    def get_bd_status(self):
        conn = connect()
        if conn:
            tk.messagebox.showinfo("Успешное подключение", "База данных была успешно подключена!")
        else:
            tk.messagebox.showwarning("Неудачное подключение", "Не удалось подключить базу данных")

    def filtration(self):
        conn = connect()
        cursor = conn.cursor()
        filtration_parametr = self.Combo.get()
        for row_id in self.CostumerTable.get_children():
            self.CostumerTable.delete(row_id)
        sql = """select * from orders_report_view where customer_name = %s"""
        cursor.execute(sql, (filtration_parametr,))
        rows = cursor.fetchall()
        for row in rows:
            self.CostumerTable.insert('', 'end', values=tuple(row))
        cursor.close()
        conn.close()
        self.get_stats_data()

    def run(self):
        self.get_bd_status()
        self.get_table_data()
        self.get_combo_data()
        self.App.mainloop()

if __name__ == '__main__':
    app = MainApp()
    app.run()