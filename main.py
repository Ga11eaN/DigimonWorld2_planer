import ttkbootstrap as ttk
from widgets import AutocompleteEntry
from tkinter import END, Listbox
from data_retrive import read_enemies_data
from tkinter import messagebox


if __name__ == "__main__":
    window = ttk.Window(themename="flatly")
    window.geometry("1024x768")
    window.title("Autocomplete Entry з таблицею")

    enemies_data = read_enemies_data()
    items = [enemy['Encounter'] for enemy in enemies_data]

    left_entry_width = 482
    container_left = ttk.Frame(window, width=left_entry_width, height=738, borderwidth=10, relief="groove")
    container_left.pack_propagate(False)
    container_left.pack(pady=10, padx=10, side='left')

    # Контейнер для Entry + кнопки
    container = ttk.Frame(container_left, height=50, borderwidth=10, relief="groove")
    container.pack(pady=10, padx=10, side='top', fill='both')

    entry = AutocompleteEntry(container, container_left, items, width=left_entry_width)
    entry.pack(side="left", fill="x", expand=True)

    def add_to_table():
        val = entry.get().strip()
        if val not in items:
            return
        exp = None
        bits = None
        for enemy in enemies_data:
            if enemy['Encounter'] == val:
                exp = enemy['Exp']
                bits = enemy['Bits']
                break
        if not exp or not bits:
            return
        tree.insert("", 'end', values=(val, exp, bits))
        entry.delete(0, END)
        update_total_bits()

    add_btn = ttk.Button(container, text="Add Fight", command=add_to_table)
    add_btn.pack(side="left", padx=(10, 0))

    # --- Додаємо вгорі, нижче container (після entry + Add Fight кнопки) ---
    manual_add_frame = ttk.Frame(container_left, height=50, borderwidth=10, relief="groove")
    manual_add_frame.pack(pady=5, padx=10, fill='both')

    # Name Entry
    ttk.Label(manual_add_frame, text="Name:").pack(side="left")
    name_var = ttk.StringVar()
    name_entry = ttk.Entry(manual_add_frame, textvariable=name_var, width=15)
    name_entry.pack(side="left", padx=(5, 10))

    # Bits Change Entry
    ttk.Label(manual_add_frame, text="Bits Change:").pack(side="left")
    bits_var = ttk.StringVar()
    bits_entry = ttk.Entry(manual_add_frame, textvariable=bits_var, width=10)
    bits_entry.pack(side="left", padx=(5, 10))


    # --- Кнопка "Add Custom" ---
    def validate_and_add_custom():
        name = name_var.get().strip()
        bits_str = bits_var.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Name cannot be empty.")
            return

        try:
            bits_value = int(bits_str)
        except ValueError:
            messagebox.showerror("Input Error", "Bits Change must be an integer.")
            return

        # Add to table
        tree.insert("", 'end', values=(name, 0, bits_value))
        name_var.set("")
        bits_var.set("")
        update_total_bits()


    custom_btn = ttk.Button(manual_add_frame, text="Add Custom", command=validate_and_add_custom)
    custom_btn.pack(side="left", padx=(10, 0))

    # Frame for table + remove button (horizontal layout)
    table_frame = ttk.Frame(container_left, borderwidth=10, relief="groove", height=650, width=left_entry_width)
    table_frame.pack(padx=10, pady=10, expand=True, fill='both')

    # Фрейм для Treeview + Scrollbar
    tree_scroll_frame = ttk.Frame(table_frame)
    tree_scroll_frame.pack(side="top", fill="both", expand=True)

    # Table on the left side
    columns = ("Enemies", "Exp", "Bits")
    tree = ttk.Treeview(tree_scroll_frame, columns=columns, show="headings", height=10)
    tree.pack(side="left", fill='both', expand=True)

    # Scrollbar for table
    scrollbar = ttk.Scrollbar(tree_scroll_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    # Set column widths
    tree.column("Enemies", width=310, anchor="w")
    tree.column("Exp", width=35, anchor="center")
    tree.column("Bits", width=35, anchor="center")

    for col in columns:
        tree.heading(col, text=col)

    # Button to remove selected row
    def remove_selected():
        selected = tree.selection()
        for item in selected:
            tree.delete(item)
            update_total_bits()


    def duplicate_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select one or more rows to duplicate.")
            return
        for item in selected:
            values = list(tree.item(item, 'values'))
            tree.insert("", 'end', values=values)

    def on_delete_key(event):
        remove_selected()

    # Прив’язуємо обробник до Treeview
    tree.bind("<Delete>", on_delete_key)

    bottom_btns = ttk.Frame(table_frame)
    bottom_btns.pack(side="bottom", pady=10)

    remove_btn = ttk.Button(bottom_btns, text="Remove", style="danger", command=remove_selected)
    remove_btn.pack(side="left", padx=(0, 10), ipadx=10)

    copy_btn = ttk.Button(bottom_btns, text="Copy Selected", style="secondary", command=duplicate_selected)
    copy_btn.pack(side="left", ipadx=10)

    digimon_info = ttk.Frame(window, width=700, borderwidth=10, relief="groove")
    digimon_info.pack(pady=15, padx=15, side='left', fill='both')

    # ---- В середині твого коду, після створення digimon_info ----

    # Створюємо список Digimon List (Listbox)
    # Контейнер для digimon_listbox + scrollbar
    digimon_list_container = ttk.Frame(digimon_info, width=512, height=120)
    digimon_list_container.pack_propagate(False)
    digimon_list_container.pack(side="top", fill="y", padx=(0, 10), pady=10)

    # Listbox у контейнері з фіксованою шириною
    digimon_listbox = Listbox(digimon_list_container, height=15)
    digimon_listbox.pack(side="left", fill="both", expand=True)

    # Вертикальний скролбар для Listbox
    scrollbar = ttk.Scrollbar(digimon_list_container, orient="vertical", command=digimon_listbox.yview)
    scrollbar.pack(side="left", fill="y")

    # Підключаємо скролбар до listbox
    digimon_listbox.config(yscrollcommand=scrollbar.set)

    # Додаємо прикладові імена Digimon
    digimons = ["Agumon", "Gabumon", "Patamon", "Gomamon", "Tentomon", "Palmon"]
    for digi in digimons:
        digimon_listbox.insert("end", digi)

    # Кнопка Add to Digi-Line
    def add_to_digi_line():
        selected = digimon_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection error", "Please select a Digimon first.")
            return
        selected_index = selected[0]
        selected_digi = digimon_listbox.get(selected_index)

        # Якщо вже підсвічено, можна попередити чи ні, тут просто повторно не додаємо підсвічування
        if selected_index in highlighted_indices:
            messagebox.showinfo("Already added", f"{selected_digi} is already in Digi-Line!")
            return

        # Підсвічуємо фон рядка зеленим
        digimon_listbox.itemconfig(selected_index, bg="lightgreen")

        # Запам'ятовуємо індекс, щоб не знімати підсвічування далі
        highlighted_indices.add(selected_index)

        messagebox.showinfo("Added", f"{selected_digi} added to Digi-Line!")


    diigmon_buttons_container = ttk.Frame(digimon_list_container, height=120)
    diigmon_buttons_container.pack(side="left", fill="y", padx=(0, 10), pady=10)

    # Множина для збереження індексів підсвічених Digimon
    highlighted_indices = set()
    add_digi_btn = ttk.Button(diigmon_buttons_container, text="Add to Digi-Line", style="primary",
                              command=add_to_digi_line)
    add_digi_btn.pack(side="top", pady=10, padx=10)

    def remove_digimon_from_container():
        pass

    add_rm_btn = ttk.Button(diigmon_buttons_container, text="Remove Digimon", style="danger",
                              command=remove_digimon_from_container)
    add_rm_btn.pack(side="top", pady=10, padx=10)

    # Правий контейнер - digimon_info вже створений і має fill='both'

    # Контейнер для Digi-Line (90% висоти)
    digi_line_container = ttk.Frame(digimon_info)
    digi_line_container.pack(side="top", fill="both", expand=True, pady=(10, 5))

    # Висоту розділяємо на 3 рівні частини (по вертикалі) з підписами
    for i in range(3):
        frame = ttk.Frame(digi_line_container, borderwidth=1, relief="solid")
        frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        label = ttk.Label(frame, text=f"Digi-Line {i + 1}", anchor="center", font=("Segoe UI", 12, "bold"))
        label.pack(side="top", fill="x")

        # Можеш додати сюди свої віджети чи Listbox, наприклад:
        # digi_listbox = Listbox(frame)
        # digi_listbox.pack(fill="both", expand=True)

    # Контейнер для Total Bits (10% висоти)
    total_bits_container = ttk.Frame(digimon_info, borderwidth=2, relief="ridge")
    total_bits_container.pack(side="bottom", fill="x", padx=5, pady=5)

    total_bits_var = ttk.StringVar(value="Total Bits: 0")
    total_bits_label = ttk.Label(total_bits_container, textvariable=total_bits_var, font=("Segoe UI", 12, "bold"))
    total_bits_label.pack(pady=10, padx=10)


    # Функція для оновлення Total Bits (рахуємо суму з лівої таблиці tree)
    def update_total_bits():
        total = 0
        for child in tree.get_children():
            bits_value = tree.item(child, 'values')[2]
            try:
                total += int(bits_value)
            except ValueError:
                pass
        total_bits_var.set(f"Total Bits: {total}")


    window.mainloop()
