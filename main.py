import ttkbootstrap as ttk
from tkinter import END, Listbox
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial

from data_retrive import read_enemies_data, get_digi_names
from widgets import AutocompleteEntry
from digimon import Digimon
from helpers import Fights


def add_to_table(entry, enemies_data):
    digi_line_check = False
    for idx in digi_line_index:
        if idx > 0:
            digi_line_check = True
            break
    if not digi_line_check:
        messagebox.showerror("Input Error", "Empty Digi-Line")
        return
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
    tree_id = tree.insert("", 'end', values=(val, exp, bits))
    entry.delete(0, END)
    update_total_bits()
    fights.add_fight(tree_id, int(exp))
    for digimon in digimons:
        if digimon.id in digi_line_index:
            digimon.win_fight(tree_id)
        digimon.calculate_exp(fights)
    refresh_digi_line()


def validate_and_add_custom(name_var, bits_var):
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
    item_id = tree.insert("", 'end', values=(name, 0, bits_value))
    name_var.set("")
    bits_var.set("")
    if not update_total_bits():
        tree.delete(item_id)
        messagebox.showerror("Input Error", "Not enough Bits!")


# Button to remove selected row
def remove_selected(tree):
    selected = tree.selection()
    for item in selected:
        tree.delete(item)
        update_total_bits()
        fights.remove_fights(item)
        for digimon in digimons:
            digimon.remove_fight(item)
    for digimon in digimons:
        digimon.calculate_exp(fights)
    refresh_digi_line()


def duplicate_selected(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("No Selection", "Please select one or more rows to duplicate.")
        return
    for item in selected:
        values = list(tree.item(item, 'values'))
        tree_id = tree.insert("", 'end', values=values)
        update_total_bits()
        fights.add_fight(tree_id, int(values[1]))
        for digimon in digimons:
            if digimon.id in digi_line_index:
                digimon.win_fight(tree_id)
            digimon.calculate_exp(fights)
        refresh_digi_line()


def on_delete_key(event, tree):
    remove_selected(tree)


def add_to_digi_line(digimon_listbox, digimons, digi_line_slots, digi_line_images):
    selected = digimon_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection error", "Please select a Digimon first.")
        return

    selected_index = selected[0]
    digi_id_name = digimon_listbox.get(0, END)[selected_index]
    digi_id = int(digi_id_name.split('. ')[0])
    for digimon_obj in digimons:
        if digimon_obj.id == digi_id:
            break

    for label in digi_line_slots:
        if label.cget("text").startswith(f"Player_name: {digimon_obj.id}. {digimon_obj.player_name}"):
            messagebox.showinfo("Already added", f"{digimon_obj.player_name} is already in Digi-Line!")
            return

    for i, label in enumerate(digi_line_slots):
        if not label.cget("text"):
            info_text = (
                f"Player_name: {digimon_obj.id}. {digimon_obj.player_name}\n"
                f"Name: {digimon_obj.digimon_name}\n"
                f"Lvl: {digimon_obj.lvl}\n"
                f"Next: {digimon_obj.exp_needed()}"
            )
            label.config(text=info_text)
            image = ImageTk.PhotoImage(Image.open(f"data/images/{digimon_obj.digimon_name}.jpg"))
            digi_line_images[i].config(image=image)
            digi_line_images[i].image = image

            remove_buttons[i].configure(state="normal")
            digimon_listbox.itemconfig(selected_index, bg="lightgreen")
            digi_line_index[i] = digimon_obj.id
            return

    messagebox.showwarning("Digi-Line Full", "Digi-Line is full! Remove one to add new.")



def remove_digimon_from_container(digimon_listbox):
    selected = digimon_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection error", "Please select a Digimon to remove.")
        return

    selected_index = selected[0]

    # Отримуємо фон елементу
    bg_color = digimon_listbox.itemcget(selected_index, "bg")

    if bg_color == "lightgreen":
        messagebox.showinfo("Cannot remove", "This Digimon is part of the Digi-Line and cannot be removed.")
        return

    # Видаляємо Digimon зі списку
    digimon_listbox.delete(selected_index)
    digimon_listbox.selection_clear(0, END)


def open_add_digimon_window(window, digimon_listbox, digimons):
    add_win = ttk.Toplevel(window)
    add_win.title("Add New Digimon")
    add_win.geometry("300x300")
    add_win.grab_set()  # Блокує головне вікно поки відкрите це

    # Entry: Player name
    ttk.Label(add_win, text="Player Name:").pack(pady=(10, 0))
    player_name_var = ttk.StringVar()
    player_name_entry = ttk.Entry(add_win, textvariable=player_name_var)
    player_name_entry.pack()

    # Entry: Digimon name
    ttk.Label(add_win, text="Digimon Name:").pack(pady=(10, 0))
    digimon_name_var = ttk.StringVar()
    digimon_name_entry = AutocompleteEntry(add_win, textvariable=digimon_name_var,
                                           root_window=add_win, suggestions=get_digi_names())
    digimon_name_entry.pack()

    # Entry: Level
    ttk.Label(add_win, text="Level:").pack(pady=(10, 0))
    level_var = ttk.StringVar()
    level_entry = ttk.Entry(add_win, textvariable=level_var)
    level_entry.pack()

    # Entry: Level
    ttk.Label(add_win, text="Exp(optional):").pack(pady=(10, 0))
    exp_var = ttk.StringVar()
    exp_entry = ttk.Entry(add_win, textvariable=exp_var)
    exp_entry.pack()

    # Внутрішня функція для додавання Digimon
    def confirm_add():
        name = digimon_name_var.get().strip()
        player = player_name_var.get().strip()
        lvl = level_var.get().strip() if level_var.get() else None
        exp = exp_var.get().strip() if exp_var.get() else None

        if not name or not player or not lvl:
            messagebox.showerror("Validation Error", "Names and lvl must be filled.")
            return

        try:
            lvl_int = int(lvl)
        except ValueError:
            messagebox.showerror("Validation Error", "Level must be an integer.")
            return

        try:
            exp_int = int(exp)
        except ValueError:
            messagebox.showerror("Validation Error", "Experience must be an integer or empty.")
            return
        except TypeError:
            exp_int = 0

        # Формуємо рядок і додаємо в Listbox
        new_digimon = Digimon(player, name, lvl=lvl_int if lvl_int else None, exp=exp_int)
        digimons.append(new_digimon)
        full_digi = f"{new_digimon.id}. {player}"
        digimon_listbox.insert("end", full_digi)
        add_win.destroy()

    # Кнопки: Add + Cancel
    btn_frame = ttk.Frame(add_win)
    btn_frame.pack(pady=20)

    add_btn = ttk.Button(btn_frame, text="Add Digimon", style="primary", command=confirm_add)
    add_btn.pack(side="left", padx=10)

    cancel_btn = ttk.Button(btn_frame, text="Cancel", style="secondary", command=add_win.destroy)
    cancel_btn.pack(side="left", padx=10)


# Кнопка Remove для слоту
def make_remove_func(index, digi_line_slots, remove_buttons, digi_line_images):
    def remove_slot():
        # Знімаємо підсвітку з digimon_listbox, якщо він там є
        slot_text = digi_line_slots[index].cget("text")
        if slot_text:
            first_line = slot_text.split('\n')[0]
            if first_line.startswith("Player_name: "):
                player_name = first_line[len("Player_name: "):]
                # Знаходимо індекс у digimon_listbox
                for idx in range(digimon_listbox.size()):
                    if digimon_listbox.get(idx) == player_name:
                        digimon_listbox.itemconfig(idx, bg="white")
                        break
        digi_line_slots[index].config(text="")
        digi_line_images[index].config(image="")
        remove_buttons[index].configure(state="disabled")

        digi_id = int(player_name.split('. ')[0])
        digi_line_index[index] = 0

    return remove_slot


def refresh_digi_line():
    for i, label in enumerate(digi_line_slots):
        if label.cget("text"):
            exists = False
            for digimon_obj in digimons:
                if digimon_obj.id == digi_line_index[i]:
                    exists = True
                    break
            if not exists:
                return
            info_text = (
                f"Player_name: {digimon_obj.id}. {digimon_obj.player_name}\n"
                f"Name: {digimon_obj.digimon_name}\n"
                f"Lvl: {digimon_obj.lvl}\n"
                f"Next: {digimon_obj.exp_needed()}"
            )
            label.config(text=info_text)
    return




if __name__ == "__main__":
    window = ttk.Window(themename="flatly")
    window.geometry("1024x768")
    window.title("Digimon World 2 Planner")

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

    fights = Fights()

    add_to_table_wrap = partial(add_to_table, entry, enemies_data)
    add_btn = ttk.Button(container, text="Add Fight", command=add_to_table_wrap)
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

    validate_and_add_custom_wrap = partial(validate_and_add_custom, name_var, bits_var)
    custom_btn = ttk.Button(manual_add_frame, text="Add Custom", command=validate_and_add_custom_wrap)
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

    on_delete_key_wrap = partial(on_delete_key, tree)
    # Прив’язуємо обробник до Treeview
    tree.bind("<Delete>", on_delete_key_wrap)

    bottom_btns = ttk.Frame(table_frame)
    bottom_btns.pack(side="bottom", pady=10)

    remove_selected_wrap = partial(remove_selected,tree)
    remove_btn = ttk.Button(bottom_btns, text="Remove", style="danger", command=remove_selected_wrap)
    remove_btn.pack(side="left", padx=(0, 10), ipadx=10)

    duplicate_selected_wrap = partial(duplicate_selected, tree)
    copy_btn = ttk.Button(bottom_btns, text="Copy Selected", style="secondary", command=duplicate_selected_wrap)
    copy_btn.pack(side="left", ipadx=10)

    digimon_info = ttk.Frame(window, width=700, borderwidth=10, relief="groove")
    digimon_info.pack(pady=15, padx=15, side='left', fill='both')

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
    digimons = [Digimon('Agumon', 'Agumon'),
                Digimon('Patamon', 'Patamon'),
                Digimon('DemiDevimon', 'DemiDevimon')]
    for digi in digimons:
        digimon_listbox.insert("end", f'{digi.id}. {digi.player_name}')

    digimon_buttons_container = ttk.Frame(digimon_list_container, height=120)
    digimon_buttons_container.pack(side="left", fill="y", padx=(0, 10), pady=10)
    buttons_width = 20

    # Список для віджетів Digi-Line (3 Label-и для 3 слотів)
    digi_line_slots = []
    digi_line_images = []

    add_to_digi_line_wrap = partial(add_to_digi_line, digimon_listbox, digimons, digi_line_slots,
                                    digi_line_images)
    add_digi_btn = ttk.Button(digimon_buttons_container, text="Add to Digi-Line", style="primary",
                              command=add_to_digi_line_wrap, width=buttons_width)
    add_digi_btn.pack(side="top", pady=2, padx=10)

    remove_digimon_from_container_wrap = partial(remove_digimon_from_container, digimon_listbox)
    add_rm_btn = ttk.Button(digimon_buttons_container, text="Remove Digimon", style="danger",
                              command=remove_digimon_from_container_wrap, width=buttons_width)
    add_rm_btn.pack(side="top", pady=2, padx=10)

    open_add_digimon_window_wrap = partial(open_add_digimon_window, window, digimon_listbox, digimons)
    add_new_digimon_btn = ttk.Button(digimon_buttons_container, text="Add Digimon", style="success",
                                     command=lambda: open_add_digimon_window_wrap(), width=buttons_width)
    add_new_digimon_btn.pack(side="top", pady=2, padx=10)

    # Правий контейнер - digimon_info вже створений і має fill='both'

    # Контейнер для Digi-Line (90% висоти)
    digi_line_container = ttk.Frame(digimon_info)
    digi_line_container.pack(side="top", fill="both", expand=True, pady=(10, 5))

    # Замінимо цикл створення слотів Digi-Line так:
    remove_buttons = []
    digi_line_index = [0, 0, 0]

    for i in range(3):
        frame = ttk.Frame(digi_line_container, borderwidth=1, relief="solid")
        frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        label_title = ttk.Label(frame, text=f"Digi-Line {i + 1}", anchor="center", font=("Segoe UI", 12, "bold"))
        label_title.pack(side="top", fill="x")

        digi_image = ttk.Label(frame)
        digi_image.pack(side='left', fill="both")

        digi_label = ttk.Label(frame, text="", anchor="w", font=("Segoe UI", 11), foreground="green")
        digi_label.pack(expand=True, fill="both", side='left')

        make_remove_func_wrap = partial(make_remove_func, i, digi_line_slots, remove_buttons, digi_line_images)
        remove_btn = ttk.Button(frame, text="Remove", state="disabled", command=make_remove_func_wrap())
        remove_btn.pack(side="left", pady=5, padx=5)

        digi_line_images.append(digi_image)
        digi_line_slots.append(digi_label)
        remove_buttons.append(remove_btn)

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

        if total >= 0:
            total_bits_var.set(f"Total Bits: {total}")
            return True
        else:
            return False




    window.mainloop()
