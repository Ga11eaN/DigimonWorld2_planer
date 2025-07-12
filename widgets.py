import tkinter as tk
import ttkbootstrap as ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, master, root_window, suggestions, *args, **kwargs):
        kwargs["width"] = int(round(kwargs["width"]/10))
        super().__init__(master, *args, **kwargs)
        self.root_window = root_window
        self.suggestions = suggestions
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace_add("write", self.on_change)

        self.listbox = None

        self.bind("<Down>", self.move_focus_to_listbox)

    def on_change(self, *_):
        typed = self.var.get().lower()
        if typed == "":
            self.hide_listbox()
            return

        matches = [item for item in self.suggestions if typed in item.lower()]
        if matches:
            self.show_listbox(matches)
        else:
            self.hide_listbox()

    def show_listbox(self, matches):
        if self.listbox:
            self.listbox.destroy()

        root = self.root_window

        self.listbox = tk.Listbox(root,
                                  bg="#FFFFFF", fg="#000000",
                                  highlightbackground="#007BFF", highlightthickness=1,
                                  selectbackground="#0D6EFD", selectforeground="#FFFFFF",
                                  relief="flat", borderwidth=0, font=("Segoe UI", 10))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        x = self.winfo_rootx() - root.winfo_rootx()
        y = self.winfo_rooty() - root.winfo_rooty() + self.winfo_height()
        width_px = self.winfo_width()

        self.listbox.place(x=x, y=y, width=width_px)

        for match in matches:
            self.listbox.insert(tk.END, match)

    def hide_listbox(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

    def on_select(self, event):
        if self.listbox:
            selection = self.listbox.get(self.listbox.curselection())
            self.var.set(selection)
            self.hide_listbox()
            self.icursor(tk.END)

    def move_focus_to_listbox(self, event):
        if self.listbox:
            self.listbox.focus()
            self.listbox.selection_set(0)
