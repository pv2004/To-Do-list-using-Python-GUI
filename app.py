import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame # type: ignore
import datetime as dt
from PIL import Image, ImageTk

def add_item():
    global entries, items_pane

    if len(input_box.get()) < 1:
        input_box.configure(bootstyle="danger")
    else:
        date = dt.datetime.now()
        entries.update({date: {"status": 0, "value": input_box.get()}})
        update_list_view(items_pane, entries)
        input_box.delete(0, END)

def add_item_via_enter(event):
    add_item()

def reset_input_box(event):
    input_box.configure(bootstyle="default")

def delete_item(key):
    global entries, items_pane, completed_pane

    print(entries)
    entries.pop(key)
    update_list_view(items_pane, entries)
    update_completed_view(completed_pane, entries)

def mark_as_done(key):
    global entries, items_pane, completed_pane

    print(entries)

    obj = entries[key]
    entries.update({key: {"status": 1, "value": obj["value"]}})
    update_completed_view(completed_pane, entries)
    update_list_view(items_pane, entries)

def undo_mark(key):
    global entries, items_pane, completed_pane

    print(entries)

    obj = entries[key]
    entries.update({key: {"status": 0, "value": obj["value"]}})
    update_completed_view(completed_pane, entries)
    update_list_view(items_pane, entries)

def update_completed_view(view, list):
    for widget in view.winfo_children():
        widget.destroy()

    count = 1
    if len(list) > 0:
        for key, content in list.items():
            if content["status"] == 0:
                continue

            date = dt.datetime.date(key)
            time = dt.datetime.time(key)
            year = int(date.strftime("%Y"))
            month = int(date.strftime("%m"))
            day = int(date.strftime("%d"))
            hour = int(time.strftime("%I"))
            minute = int(time.strftime("%M"))
            second = int(time.strftime("%S"))
            ampm = time.strftime("%p")
            date_str = f"{year}-{month}-{day} {hour}:{minute}:{second} {ampm}"

            item_frame = tk.Frame(view, border=2)
            item_frame.pack(fill=X, expand=YES, ipadx=10, ipady=10)

            details_frame = tk.Frame(item_frame)
            details_frame.pack(side=LEFT, expand=True, fill=BOTH)

            item_value = ttk.Label(details_frame, text=content["value"], font=('sans-serif', 16), justify=LEFT)
            item_value.pack(side=TOP, fill=BOTH, padx=10, pady=(10, 0))

            item_date = ttk.Label(details_frame, text=date_str, font=('sans-serif', 8), justify=LEFT)
            item_date.pack(side=BOTTOM, fill=BOTH, padx=10, pady=(20, 10))

            item_delete = ttk.Button(item_frame, text="Delete Item", bootstyle="danger", cursor="hand2", command=lambda:delete_item(key))
            item_delete.pack(side=RIGHT, padx=20)
            item_unmark = ttk.Button(item_frame, text="Mark as Pending", bootstyle="warning", cursor="hand2", command=lambda:undo_mark(key))
            item_unmark.pack(side=RIGHT, padx=(10, 4))

            if(count % 2 == 0):
                item_frame.configure(bg="#fff")
                details_frame.configure(bg="#fff")
                item_value.configure(background="#fff")
                item_date.configure(background="#fff")
            else:
                item_frame.configure(bg="#F8FCFA")
                details_frame.configure(bg="#F8FCFA")
                item_value.configure(background="#F8FCFA")
                item_date.configure(background="#F8FCFA")

            count = count + 1

def update_list_view(view, list):
    for widget in view.winfo_children():
        widget.destroy()

    count = 1
    if len(list) > 0:
        for key, content in list.items():
            if content["status"] == 1:
                continue

            date = dt.datetime.date(key)
            time = dt.datetime.time(key)
            year = int(date.strftime("%Y"))
            month = int(date.strftime("%m"))
            day = int(date.strftime("%d"))
            hour = int(time.strftime("%I"))
            minute = int(time.strftime("%M"))
            second = int(time.strftime("%S"))
            ampm = time.strftime("%p")
            date_str = f"{year}-{month}-{day} {hour}:{minute}:{second} {ampm}"

            item_frame = tk.Frame(view, border=2)
            item_frame.pack(fill=X, expand=YES, ipadx=10, ipady=10)

            details_frame = tk.Frame(item_frame)
            details_frame.pack(side=LEFT, expand=True, fill=BOTH)

            item_value = ttk.Label(details_frame, text=content["value"], font=('sans-serif', 16), justify=LEFT)
            item_value.pack(side=TOP, fill=BOTH, padx=10, pady=(10, 0))

            item_date = ttk.Label(details_frame, text=date_str, font=('sans-serif', 8), justify=LEFT)
            item_date.pack(side=BOTTOM, fill=BOTH, padx=10, pady=(20, 10))

            item_delete = ttk.Button(item_frame, text="Delete Item", bootstyle="danger", cursor="hand2", command=lambda:delete_item(key))
            item_delete.pack(side=RIGHT, padx=20)
            item_mark = ttk.Button(item_frame, text="Mark as Done", bootstyle="success", cursor="hand2", command=lambda:mark_as_done(key))
            item_mark.pack(side=RIGHT, padx=(10, 4))

            if(count % 2 == 0):
                item_frame.configure(bg="#fff")
                details_frame.configure(bg="#fff")
                item_value.configure(background="#fff")
                item_date.configure(background="#fff")
            else:
                item_frame.configure(bg="#F8FCFA")
                details_frame.configure(bg="#F8FCFA")
                item_value.configure(background="#F8FCFA")
                item_date.configure(background="#F8FCFA")

            count = count + 1

def switch_to_itemlist():
    global completed_pane, items_pane, items_btn, completed_btn
    items_btn.config(bootstyle="dark")
    completed_btn.config(bootstyle="light")
    completed_pane.pack_forget()
    items_pane.pack(fill=BOTH, expand=False)

def switch_to_completedlist():
    global completed_pane, items_pane, items_btn, completed_btn
    items_btn.config(bootstyle="light")
    completed_btn.config(bootstyle="dark")
    items_pane.pack_forget()
    completed_pane.pack(fill=BOTH, expand=False)

root = ttk.Window( title="To-Do List")

# Use PIL library to transform PNG into ICO for Tkinter Window Icon
ico = Image.open("to-do-list.png")
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

entries = {}

# Input Area
frame1 = tk.Frame(root)
frame1.pack(side=TOP, padx=20, pady=(10, 20), ipadx=20)

input_label = ttk.LabelFrame(frame1, text="Insert New Item")
input_label.pack(padx=20, ipadx=20)

input_box = ttk.Entry(input_label, width=150)
input_box.bind("<Key>", reset_input_box)
input_box.bind("<Return>", add_item_via_enter)
input_box.pack(side=LEFT, padx=(20, 0), pady=10)

input_btn = ttk.Button(input_label, text="Add Item", bootstyle="primary", cursor="hand2", command=add_item)
input_btn.pack(side=RIGHT, padx=(0, 20), pady=10)

switch_btn_frame = tk.Frame(root)
switch_btn_frame.pack(side=TOP, fill=X)

items_btn = ttk.Button(switch_btn_frame, text="Pending Items", cursor="hand2", command=switch_to_itemlist, bootstyle="dark")
items_btn.pack(side=LEFT, padx=(10, 0), expand=False)
completed_btn = ttk.Button(switch_btn_frame, text="Completed Items", cursor="hand2", command=switch_to_completedlist, bootstyle="light")
completed_btn.pack(side=LEFT, padx=(10, 0), expand=False)

view_frame = tk.Frame(root, width=150, height=600, bd=2)
view_frame.pack(padx=20, pady=20, fill=BOTH, expand=False)

# To-Do List Area
items_pane = ScrolledFrame(view_frame, autohide=True, height=600)
# items_pane = ttk.Frame(root, height=600)
items_pane.pack(fill=BOTH, expand=False)

update_list_view(items_pane, entries)

completed_pane = ScrolledFrame(view_frame, autohide=True, height=600)
# completed_pane = ttk.Frame(root, height=600)

update_completed_view(completed_pane, entries)

root.mainloop()




