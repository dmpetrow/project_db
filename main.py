import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Настройки подключения к базе данных
DB_CONFIG = {
    'dbname': 'constellations_db',
    'user': 'postgres',
    'password': 'qwerty21',
    'host': 'localhost',
    'port': '5432'
}

# Функция подключения к базе данных
def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
        return None

# Вкладка для созвездий
class ConstellationsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_input)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Латинское название:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_latin_name = tk.Entry(frame_input)
        self.entry_latin_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Площадь (в градусах):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_area = tk.Entry(frame_input)
        self.entry_area.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Основные звезды:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_main_stars = tk.Entry(frame_input)
        self.entry_main_stars.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_constellation).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_constellation).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Название", "Латинское название", "Основные звезды", "Площадь")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()

    def add_constellation(self):
        name = self.entry_name.get()
        latin_name = self.entry_latin_name.get()
        area = self.entry_area.get()
        main_stars = self.entry_main_stars.get()

        if not name or not latin_name or not area or not main_stars:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return

        try:
            area = float(area)
            main_stars = int(main_stars)
        except ValueError:
            messagebox.showerror("Ошибка", "Площадь и количество основных звезд должны быть числами.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO constellations (name, latin_name, area_square_degrees, main_stars_count)
                            VALUES (%s, %s, %s, %s)""",
                        (name, latin_name, area, main_stars)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Созвездие успешно добавлено!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить созвездие: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM constellations")
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()

    def delete_constellation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите запись для удаления.")
            return

        constellation_id = self.tree.item(selected_item[0])['values'][0]

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM constellations WHERE constellation_id = %s", (constellation_id,))
                    conn.commit()
                    messagebox.showinfo("Успех", "Созвездие успешно удалено!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить созвездие: {e}")
            finally:
                conn.close()

# Вкладка для звезд
class StarsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_input)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="ID созвездия:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_constellation_id = tk.Entry(frame_input)
        self.entry_constellation_id.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Прямое восхождение:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_ra = tk.Entry(frame_input)
        self.entry_ra.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Склонение:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_declination = tk.Entry(frame_input)
        self.entry_declination.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Видимая звёздная величина:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_magnitude = tk.Entry(frame_input)
        self.entry_magnitude.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Расстояние (свет. годы):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_distance = tk.Entry(frame_input)
        self.entry_distance.grid(row=5, column=1, padx=5, pady=5)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_star).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_star).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Название", "ID созвездия", "Прямое восхождение", "Склонение", "Величина", "Расстояние")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()

    def add_star(self):
        name = self.entry_name.get()
        constellation_id = self.entry_constellation_id.get()
        ra = self.entry_ra.get()
        declination = self.entry_declination.get()
        magnitude = self.entry_magnitude.get()
        distance = self.entry_distance.get()

        if not name or not ra or not declination or not distance:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните обязательные поля.")
            return

        try:
            ra = float(ra)
            declination = float(declination)
            distance = float(distance)
            magnitude = float(magnitude) if magnitude else None
        except ValueError:
            messagebox.showerror("Ошибка", "Некоторые числовые поля содержат неверные данные.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO stars (name, constellation_id, right_ascension, declination, magnitude, distance_light_years)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                        (name, constellation_id if constellation_id else None, ra, declination, magnitude, distance)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Звезда успешно добавлена!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить звезду: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM stars")
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()

    def delete_star(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите запись для удаления.")
            return

        star_id = self.tree.item(selected_item[0])['values'][0]

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM stars WHERE star_id = %s", (star_id,))
                    conn.commit()
                    messagebox.showinfo("Успех", "Звезда успешно удалена!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить звезду: {e}")
            finally:
                conn.close()

# Вкладка для объектов
class ObjectTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_input)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="ID созвездия:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_constellation_id = tk.Entry(frame_input)
        self.entry_constellation_id.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Описание:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_description = tk.Entry(frame_input)
        self.entry_description.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_object).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_object).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Название", "ID созвездия", "Описание")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()

    def add_object(self):
        name = self.entry_name.get()
        constellation_id = self.entry_constellation_id.get()
        description = self.entry_description.get()
       
        if not name or not description:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните обязательные поля.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO observation_objects (name, constellation_id, description)
                            VALUES (%s, %s, %s )""",
                        (name, constellation_id if constellation_id else None, description)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Объект успешно добавлена!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить объект: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM observation_objects")
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()

    def delete_object(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите запись для удаления.")
            return

        object_id = self.tree.item(selected_item[0])['values'][0]

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM  observation_objects WHERE object_id = %s", (object_id,))
                    conn.commit()
                    messagebox.showinfo("Успех", "Объект успешно удалена!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить объект: {e}")
            finally:
                conn.close()                

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("База данных созвездий")
        self.geometry("900x600")

        # Создаем виджет Notebook для вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка для созвездий
        self.constellations_tab = ConstellationsTab(self.notebook)
        self.notebook.add(self.constellations_tab.frame, text="Созвездия")

        # Вкладка для звезд
        self.stars_tab = StarsTab(self.notebook)
        self.notebook.add(self.stars_tab.frame, text="Звезды")

        # Вкладка для объектов
        self.object_tab = ObjectTab(self.notebook)
        self.notebook.add(self.object_tab.frame, text="Объекты")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
