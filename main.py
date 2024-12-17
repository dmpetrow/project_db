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

class ConstellationsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_constellation).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_constellation).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.edit_record).pack(side=tk.LEFT, padx=5)

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
        # Создаем окно для добавления новой записи
        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить созвездие")

        # Поля для ввода данных
        tk.Label(add_window, text="Название:").grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Латинское название:").grid(row=1, column=0)
        latin_name_entry = tk.Entry(add_window)
        latin_name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Площадь (в градусах):").grid(row=2, column=0)
        area_entry = tk.Entry(add_window)
        area_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Основные звезды:").grid(row=3, column=0)
        main_stars_entry = tk.Entry(add_window)
        main_stars_entry.grid(row=3, column=1)

        # Кнопка для сохранения новой записи
        tk.Button(add_window, text="Сохранить", command=lambda: self.save_new_constellation(
            name_entry.get(), latin_name_entry.get(), area_entry.get(), main_stars_entry.get(), add_window
        )).grid(row=4, column=0, columnspan=2)

    def save_new_constellation(self, name, latin_name, area, main_stars, window):
        # Сохраняем новое созвездие в базу данных
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
                    window.destroy()  # Закрыть окно добавления
                    self.refresh_table()  # Обновить таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить созвездие: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        # Очистка текущих данных в таблице
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT constellation_id, name, latin_name, main_stars_count, area_square_degrees
                        FROM constellations
                        ORDER BY constellation_id ASC  -- Сортировка по ID созвездия
                    """)
                    rows = cursor.fetchall()
                    for row in rows:
                        # Вставка каждой строки в таблицу
                        self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()


    def delete_constellation(self):
        # Удаление выбранной записи
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

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для обновления!")
            return

        # Получаем данные выбранной записи
        record = self.tree.item(selected_item, "values")

        # Открываем окно редактирования с переданными значениями
        self.open_edit_window(record)

    def open_edit_window(self, record):
        edit_window = tk.Toplevel(self.parent)  # Use self.parent as the parent
        edit_window.title("Изменить запись")

        # Параметры записи
        tk.Label(edit_window, text="Название:").grid(row=0, column=0)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, record[1])
        name_entry.grid(row=0, column=1)

        tk.Label(edit_window, text="Латинское название:").grid(row=1, column=0)
        latin_name_entry = tk.Entry(edit_window)
        latin_name_entry.insert(0, record[2])
        latin_name_entry.grid(row=1, column=1)

        tk.Label(edit_window, text="Площадь (в градусах):").grid(row=2, column=0)
        area_entry = tk.Entry(edit_window)
        area_entry.insert(0, record[4])
        area_entry.grid(row=2, column=1)

        tk.Label(edit_window, text="Основные звезды:").grid(row=3, column=0)
        main_stars_entry = tk.Entry(edit_window)
        main_stars_entry.insert(0, record[3])
        main_stars_entry.grid(row=3, column=1)

        # Кнопка сохранить изменения
        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_changes(
            record[0], name_entry.get(), latin_name_entry.get(), area_entry.get(), main_stars_entry.get(), edit_window
        )).grid(row=4, column=0, columnspan=2)

    def save_changes(self, constellation_id, name, latin_name, area, main_stars, window):
        # Сохраняем изменения в базу данных
        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE constellations
                        SET name = %s, latin_name = %s, area_square_degrees = %s, main_stars_count = %s
                        WHERE constellation_id = %s
                    """, (name, latin_name, area, main_stars, constellation_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Запись успешно обновлена!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить запись: {e}")
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

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_star).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_star).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.edit_record).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Название звезды", "Созвездие", "Прямое восхождение", "Склонение", "Величина", "Расстояние (св. лет)")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()

    def add_star(self):
        # Создаем окно для добавления новой записи
        add_window = tk.Toplevel(self.parent)  # Используем self.parent, чтобы окно было дочерним для главного
        add_window.title("Добавить звезду")

        # Поля для ввода данных
        tk.Label(add_window, text="Название звезды:").grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Прямое восхождение:").grid(row=1, column=0)
        ra_entry = tk.Entry(add_window)
        ra_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Склонение:").grid(row=2, column=0)
        decl_entry = tk.Entry(add_window)
        decl_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Расстояние (св. лет):").grid(row=3, column=0)
        distance_entry = tk.Entry(add_window)
        distance_entry.grid(row=3, column=1)

        tk.Label(add_window, text="ID созвездия:").grid(row=4, column=0)
        constellation_id_entry = tk.Entry(add_window)
        constellation_id_entry.grid(row=4, column=1)

        tk.Label(add_window, text="Видимая звёздная величина:").grid(row=5, column=0)
        magnitude_entry = tk.Entry(add_window)
        magnitude_entry.grid(row=5, column=1)

        # Кнопка для сохранения новой записи
        tk.Button(add_window, text="Сохранить", command=lambda: self.save_new_star(
            name_entry.get(), ra_entry.get(), decl_entry.get(), distance_entry.get(), 
            constellation_id_entry.get(), magnitude_entry.get(), add_window
        )).grid(row=6, column=0, columnspan=2)

    def save_new_star(self, name, ra, decl, distance, constellation_id, magnitude, window):
        # Сохраняем новую звезду в базу данных
        if not name or not ra or not decl or not distance:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните обязательные поля.")
            return

        try:
            ra = float(ra)
            decl = float(decl)
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
                        (name, constellation_id if constellation_id else None, ra, decl, magnitude, distance)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Звезда успешно добавлена!")
                    window.destroy()  # Закрыть окно добавления
                    self.refresh_table()  # Обновить таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить звезду: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        # Очистка текущих данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT s.star_id, s.name, c.name AS constellation_name, 
                            s.right_ascension, s.declination, s.magnitude, 
                            s.distance_light_years
                        FROM stars s
                        LEFT JOIN constellations c ON s.constellation_id = c.constellation_id
                        ORDER BY s.star_id ASC  -- Сортировка по ID звезды
                    """)
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

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для обновления!")
            return

        # Получаем данные выбранной записи
        record = self.tree.item(selected_item, "values")

        # Открываем окно редактирования с переданными значениями
        self.open_edit_window(record)

    def open_edit_window(self, record):
        edit_window = tk.Toplevel(self.parent)  # Use self.parent as the parent
        edit_window.title("Изменить запись")

        # Параметры записи
        tk.Label(edit_window, text="Название звезды:").grid(row=0, column=0)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, record[1])
        name_entry.grid(row=0, column=1)

        tk.Label(edit_window, text="Прямое восхождение:").grid(row=1, column=0)
        ra_entry = tk.Entry(edit_window)
        ra_entry.insert(0, record[3])
        ra_entry.grid(row=1, column=1)

        tk.Label(edit_window, text="Склонение:").grid(row=2, column=0)
        decl_entry = tk.Entry(edit_window)
        decl_entry.insert(0, record[4])
        decl_entry.grid(row=2, column=1)

        tk.Label(edit_window, text="Расстояние (св. лет):").grid(row=3, column=0)
        distance_entry = tk.Entry(edit_window)
        distance_entry.insert(0, record[6])
        distance_entry.grid(row=3, column=1)

        # Кнопка сохранить изменения
        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_changes(
            record[0], name_entry.get(), ra_entry.get(), decl_entry.get(), distance_entry.get(), edit_window
        )).grid(row=4, column=0, columnspan=2)
  

    def save_changes(self, star_id, name, ra, decl, distance, window):
        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE stars
                        SET name = %s, right_ascension = %s, declination = %s, distance_light_years = %s
                        WHERE star_id = %s
                    """, (name, ra, decl, distance, star_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Запись успешно обновлена!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить запись: {e}")
            finally:
                conn.close()           
                
                
class ObjectTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.entry_name = None
        self.entry_constellation_id = None
        self.entry_description = None
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_object).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_object).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.edit_record).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Название объекта", "Созвездие", "Описание")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()


    def add_object(self):
        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить новый объект")

        # Поля для ввода данных
        tk.Label(add_window, text="Название объекта:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="ID созвездия:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        constellation_id_entry = tk.Entry(add_window)
        constellation_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Описание:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        description_entry = tk.Entry(add_window)
        description_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка для сохранения новой записи
        tk.Button(add_window, text="Сохранить", command=lambda: self.save_new_object(
            name_entry.get(), constellation_id_entry.get(), description_entry.get(), add_window
        )).grid(row=3, column=0, columnspan=2, pady=10)

    def save_new_object(self, name, constellation_id, description, window):
        if not name or not description:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните обязательные поля.")
            return

        # Проверка на числовое значение ID созвездия
        if constellation_id and not constellation_id.isdigit():
            messagebox.showerror("Ошибка", "ID созвездия должен быть числом.")
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
                    messagebox.showinfo("Успех", "Объект успешно добавлен!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить объект: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        # Очистка текущих данных в таблице
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT o.object_id, o.name, c.name AS constellation_name, o.description
                        FROM observation_objects o
                        LEFT JOIN constellations c ON o.constellation_id = c.constellation_id
                        ORDER BY o.object_id ASC  -- Сортировка по ID
                    """)
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
                    messagebox.showinfo("Успех", "Объект успешно удален!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить объект: {e}")
            finally:
                conn.close()

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для обновления!")
            return

        # Получаем данные выбранной записи
        record = self.tree.item(selected_item, "values")

        # Открываем окно редактирования с переданными значениями
        self.open_edit_window(record)

    def open_edit_window(self, record):
        edit_window = tk.Toplevel(self.parent)  # Use self.parent as the parent
        edit_window.title("Изменить объект")

        # Поле для редактирования названия объекта
        tk.Label(edit_window, text="Название объекта:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, record[1])  # Вставляем текущее название объекта
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Поле для редактирования описания объекта
        tk.Label(edit_window, text="Описание:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        description_entry = tk.Entry(edit_window)
        description_entry.insert(0, record[3])  # Вставляем текущее описание объекта
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        # Кнопка для сохранения изменений
        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_changes(
            record[0],  # object_id
            name_entry.get(),
            record[2],  # constellations_id (ID созвездия, не редактируемый)
            description_entry.get(),
            edit_window
        )).grid(row=3, column=0, columnspan=2, pady=10)


    def save_changes(self, object_id, name, description, window):
        if not name or not description:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните обязательные поля.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE observation_objects
                        SET name = %s, description = %s
                        WHERE object_id = %s
                    """, (name, description, object_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Запись успешно обновлена!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить запись: {e}")
            finally:
                conn.close()
               

class HistoricalFactsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_fact).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_fact).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.edit_fact).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Созвездие", "Текст факта")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()

    def add_fact(self):
        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить новый исторический факт")

        # Поля для ввода данных
        tk.Label(add_window, text="Созвездие (ID):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        constellation_id_entry = tk.Entry(add_window)
        constellation_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Текст факта:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        fact_text_entry = tk.Entry(add_window)
        fact_text_entry.grid(row=1, column=1, padx=5, pady=5)

        # Кнопка для сохранения новой записи
        tk.Button(add_window, text="Сохранить", command=lambda: self.save_new_fact(
            constellation_id_entry.get(), fact_text_entry.get(), add_window
        )).grid(row=2, column=0, columnspan=2, pady=10)

    def save_new_fact(self, constellation_id, fact_text, window):
        if not constellation_id or not fact_text:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return

        # Проверка на числовое значение ID созвездия
        if not constellation_id.isdigit():
            messagebox.showerror("Ошибка", "ID созвездия должен быть числом.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO historical_facts (constellation_id, fact_text)
                            VALUES (%s, %s)""",
                        (constellation_id, fact_text)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Исторический факт успешно добавлен!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить исторический факт: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        # Очистка текущих данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT h.fact_id, c.name AS constellation_name, h.fact_text
                        FROM historical_facts h
                        LEFT JOIN constellations c ON h.constellation_id = c.constellation_id
                        ORDER BY h.fact_id ASC
                    """)
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()

    def delete_fact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите запись для удаления.")
            return

        fact_id = self.tree.item(selected_item[0])['values'][0]

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM historical_facts WHERE fact_id = %s", (fact_id,))
                    conn.commit()
                    messagebox.showinfo("Успех", "Исторический факт успешно удален!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить исторический факт: {e}")
            finally:
                conn.close()

    def edit_fact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для редактирования.")
            return

        fact_id = self.tree.item(selected_item[0])['values'][0]
        fact_text = self.tree.item(selected_item[0])['values'][2]
        constellation_name = self.tree.item(selected_item[0])['values'][1]

        # Открытие окна редактирования
        self.open_edit_fact_window(fact_id, constellation_name, fact_text)

    def open_edit_fact_window(self, fact_id, constellation_name, fact_text):
        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Редактировать исторический факт")

        # Показываем только ID созвездия (не редактируем)
        tk.Label(edit_window, text="Созвездие:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        constellation_label = tk.Label(edit_window, text=constellation_name)
        constellation_label.grid(row=0, column=1, padx=5, pady=5)

        # Поле для редактирования текста факта
        tk.Label(edit_window, text="Текст факта:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        fact_text_entry = tk.Entry(edit_window)
        fact_text_entry.insert(0, fact_text)
        fact_text_entry.grid(row=1, column=1, padx=5, pady=5)

        # Кнопка для сохранения изменений
        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_fact_changes(
            fact_id, fact_text_entry.get(), edit_window
        )).grid(row=2, column=0, columnspan=2, pady=10)

    def save_fact_changes(self, fact_id, fact_text, window):
        if not fact_text:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните текст факта.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE historical_facts
                        SET fact_text = %s
                        WHERE fact_id = %s
                    """, (fact_text, fact_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Исторический факт успешно обновлен!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить факт: {e}")
            finally:
                conn.close()


class ObservationSeasonsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)
        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_season).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_season).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.edit_record).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID", "Название сезона", "Начальный месяц", "Конечный месяц")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()

    def add_season(self):
        # Создаем окно для добавления нового сезона
        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить сезон")

        # Поля для ввода данных
        tk.Label(add_window, text="Название сезона:").grid(row=0, column=0)
        season_name_entry = tk.Entry(add_window)
        season_name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Начальный месяц (1-12):").grid(row=1, column=0)
        start_month_entry = tk.Entry(add_window)
        start_month_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Конечный месяц (1-12):").grid(row=2, column=0)
        end_month_entry = tk.Entry(add_window)
        end_month_entry.grid(row=2, column=1)

        # Кнопка для сохранения нового сезона
        tk.Button(add_window, text="Сохранить", command=lambda: self.save_new_season(
            season_name_entry.get(), start_month_entry.get(), end_month_entry.get(), add_window
        )).grid(row=3, column=0, columnspan=2)

    def save_new_season(self, name, start_month, end_month, window):
        # Сохраняем новый сезон в базу данных
        if not name or not start_month.isdigit() or not end_month.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")
            return

        try:
            start_month = int(start_month)
            end_month = int(end_month)
        except ValueError:
            messagebox.showerror("Ошибка", "Месяцы должны быть числами.")
            return

        # Проверка диапазонов месяцев
        if not (1 <= start_month <= 12) or not (1 <= end_month <= 12):
            messagebox.showwarning("Ошибка", "Месяцы должны быть в диапазоне от 1 до 12.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO observation_seasons (season_name, start_month, end_month)
                        VALUES (%s, %s, %s)""",
                        (name, start_month, end_month)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Сезон успешно добавлен!")
                    window.destroy()  # Закрыть окно добавления
                    self.refresh_table()  # Обновить таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить сезон: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        # Очистка текущих данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM observation_seasons")
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()
    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для обновления!")
            return

        # Получаем данные выбранной записи
        record = self.tree.item(selected_item, "values")

        # Открываем окно редактирования с переданными значениями
        self.open_edit_window(record)

    def open_edit_window(self, record):
        edit_window = tk.Toplevel(self.parent)  # Use self.parent as the parent
        edit_window.title("Изменить сезон")

        # Поля для редактирования записи
        tk.Label(edit_window, text="Название сезона:").grid(row=0, column=0)
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, record[1])
        name_entry.grid(row=0, column=1)

        tk.Label(edit_window, text="Начальный месяц:").grid(row=1, column=0)
        start_month_entry = tk.Entry(edit_window)
        start_month_entry.insert(0, record[2])
        start_month_entry.grid(row=1, column=1)

        tk.Label(edit_window, text="Конечный месяц:").grid(row=2, column=0)
        end_month_entry = tk.Entry(edit_window)
        end_month_entry.insert(0, record[3])
        end_month_entry.grid(row=2, column=1)

        # Кнопка для сохранения изменений
        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_changes(
            record[0], name_entry.get(), start_month_entry.get(), end_month_entry.get(), edit_window
        )).grid(row=3, column=0, columnspan=2)

    def save_changes(self, season_id, season_name, start_month, end_month, window):
        # Проверка на корректность данных
        if not season_name or not start_month.isdigit() or not end_month.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")
            return

        start_month = int(start_month)
        end_month = int(end_month)

        if not (1 <= start_month <= 12) or not (1 <= end_month <= 12):
            messagebox.showwarning("Ошибка", "Месяцы должны быть в диапазоне от 1 до 12.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE observation_seasons
                        SET season_name = %s, start_month = %s, end_month = %s
                        WHERE season_id = %s
                    """, (season_name, start_month, end_month, season_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Сезон успешно обновлен!")
                    window.destroy()  # Закрыть окно редактирования
                    self.refresh_table()  # Обновить таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить сезон: {e}")
            finally:
                conn.close()            

    def delete_season(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите запись для удаления.")
            return

        season_id = self.tree.item(selected_item[0])['values'][0]

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Удаляем записи из таблицы constellation_seasons, которые ссылаются на этот сезон
                    cursor.execute("DELETE FROM constellation_seasons WHERE season_id = %s", (season_id,))

                    # Удаляем сам сезон из таблицы observation_seasons
                    cursor.execute("DELETE FROM observation_seasons WHERE season_id = %s", (season_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", "Сезон успешно удален!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить сезон: {e}")
            finally:
                conn.close()

class ConstellationSeasonsTab:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных
        frame_input = tk.Frame(self.frame)
        frame_input.pack(pady=10, padx=10, fill=tk.X)

        # Кнопки действий
        frame_buttons = tk.Frame(self.frame)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Добавить", command=self.add_constellation_season).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Удалить", command=self.delete_constellation_season).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="Обновить", command=self.edit_record).pack(side=tk.LEFT, padx=5)

        # Таблица данных
        frame_table = tk.Frame(self.frame)
        frame_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.columns = ("ID созвездия", "Название созвездия", "ID сезона", "Название сезона", "Месяц начала", "Месяц конца")
        self.tree = ttk.Treeview(frame_table, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка данных при запуске
        self.refresh_table()


    def add_constellation_season(self):
        # Создаем окно для добавления новой записи
        add_window = tk.Toplevel(self.parent)  # Используем self.parent, чтобы окно было дочерним для главного
        add_window.title("Добавить связь созвездие-сезон")

        # Поля для ввода данных
        tk.Label(add_window, text="ID созвездия:").grid(row=0, column=0)
        constellation_id_entry = tk.Entry(add_window)
        constellation_id_entry.grid(row=0, column=1)

        tk.Label(add_window, text="ID сезона:").grid(row=1, column=0)
        season_id_entry = tk.Entry(add_window)
        season_id_entry.grid(row=1, column=1)

        # Кнопка для сохранения новой записи
        tk.Button(add_window, text="Сохранить", command=lambda: self.save_new_constellation_season(
            constellation_id_entry.get(), season_id_entry.get(), add_window
        )).grid(row=2, column=0, columnspan=2)

    def save_new_constellation_season(self, constellation_id, season_id, window):
        # Сохраняем новую запись о связи между созвездием и сезоном в базу данных
        if not constellation_id.isdigit() or not season_id.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, введите корректные ID (целые числа).")
            return

        try:
            constellation_id = int(constellation_id)
            season_id = int(season_id)
        except ValueError:
            messagebox.showerror("Ошибка", "Некоторые поля содержат неверные данные.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO constellation_seasons (constellation_id, season_id)
                        VALUES (%s, %s)""",
                        (constellation_id, season_id)
                    )
                    conn.commit()
                    messagebox.showinfo("Успех", "Запись о связи созвездие-сезон успешно добавлена!")
                    window.destroy()  # Закрыть окно добавления
                    self.refresh_table()  # Обновить таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить запись: {e}")
            finally:
                conn.close()

    def refresh_table(self):
        # Очистка текущих данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT cs.constellation_id, co.name AS constellation_name,
                            cs.season_id, os.season_name, os.start_month, os.end_month
                        FROM constellation_seasons cs
                        JOIN constellations co ON cs.constellation_id = co.constellation_id
                        JOIN observation_seasons os ON cs.season_id = os.season_id
                        ORDER BY cs.constellation_id ASC            
                    """)
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            finally:
                conn.close()


    def delete_constellation_season(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите запись для удаления.")
            return

        constellation_id = self.tree.item(selected_item[0])['values'][0]
        season_id = self.tree.item(selected_item[0])['values'][1]

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Удаляем связь между созвездием и сезоном
                    cursor.execute("DELETE FROM constellation_seasons WHERE constellation_id = %s AND season_id = %s", 
                                   (constellation_id, season_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Связь между созвездием и сезоном успешно удалена!")
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить связь: {e}")
            finally:
                conn.close()

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для обновления!")
            return

        # Получаем данные выбранной записи
        record = self.tree.item(selected_item, "values")

        # Открываем окно редактирования с переданными значениями
        self.open_edit_window(record)

    def open_edit_window(self, record):
        edit_window = tk.Toplevel(self.parent)  # Используем self.parent как родительское окно
        edit_window.title("Изменить связь созвездие-сезон")

        # Параметры записи
        tk.Label(edit_window, text="ID созвездия:").grid(row=0, column=0)
        constellation_id_entry = tk.Entry(edit_window)
        constellation_id_entry.insert(0, record[0])
        constellation_id_entry.grid(row=0, column=1)

        tk.Label(edit_window, text="ID сезона:").grid(row=1, column=0)
        season_id_entry = tk.Entry(edit_window)
        season_id_entry.insert(0, record[2])
        season_id_entry.grid(row=1, column=1)

        # Кнопка для сохранения изменений
        tk.Button(edit_window, text="Сохранить", command=lambda: self.save_changes(
            record[0], record[1], constellation_id_entry.get(), season_id_entry.get(), edit_window
        )).grid(row=2, column=0, columnspan=2)

    def save_changes(self, old_constellation_id, old_season_id, new_constellation_id, new_season_id, window):
        # Обновляем данные о связи созвездие-сезон
        if not new_constellation_id.isdigit() or not new_season_id.isdigit():
            messagebox.showwarning("Ошибка", "Пожалуйста, введите корректные ID (целые числа).")
            return

        try:
            new_constellation_id = int(new_constellation_id)
            new_season_id = int(new_season_id)
        except ValueError:
            messagebox.showerror("Ошибка", "Некоторые поля содержат неверные данные.")
            return

        conn = connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE constellation_seasons
                        SET constellation_id = %s, season_id = %s
                        WHERE constellation_id = %s AND season_id = %s
                    """, (new_constellation_id, new_season_id, old_constellation_id, old_season_id))
                    conn.commit()
                    messagebox.showinfo("Успех", "Связь успешно обновлена!")
                    window.destroy()
                    self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить запись: {e}")
            finally:
                conn.close()

# Обновление главного приложения
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("База данных созвездий")
        self.geometry("900x600")

        # Создаем виджет Notebook для вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Добавление всех вкладок
        self.constellations_tab = ConstellationsTab(self.notebook)
        self.notebook.add(self.constellations_tab.frame, text="Созвездия")

        self.stars_tab = StarsTab(self.notebook)
        self.notebook.add(self.stars_tab.frame, text="Звезды")

        self.object_tab = ObjectTab(self.notebook)
        self.notebook.add(self.object_tab.frame, text="Объекты")

        self.historical_facts_tab = HistoricalFactsTab(self.notebook)
        self.notebook.add(self.historical_facts_tab.frame, text="Исторические факты")

        self.observation_seasons_tab = ObservationSeasonsTab(self.notebook)
        self.notebook.add(self.observation_seasons_tab.frame, text="Сезоны наблюдения")

        self.constellation_seasons_tab = ConstellationSeasonsTab(self.notebook)
        self.notebook.add(self.constellation_seasons_tab.frame, text="Сезон - Созвездие")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
