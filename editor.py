from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

root = Tk()
root.title("Text Editor in Python!")
root.geometry("1000x600")
root.resizable(True, True)

global open_status_name
open_status_name = False

global selected
selected = False

toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, pady=5)

my_frame = Frame(root)
my_frame.pack(pady=5)

ver_scroll = Scrollbar(my_frame)
ver_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

my_text = Text(my_frame, width=80, height=20, font=("Helvetica", 16), selectbackground="lightgrey",
               selectforeground="black", undo=True,
               yscrollcommand=ver_scroll.set, xscrollcommand=hor_scroll.set, wrap="none")
my_text.pack()

ver_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

my_menu = Menu(root)
root.config(menu=my_menu)

status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)


def new_file(e):
    my_text.delete("1.0", END)
    root.title("Untitled")
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False


def open_file(e):
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="E:/", title="Open File",
                                           filetypes=(
                                               ("Text Files",
                                                "*.txt"), ("HTML Files", "*.html"),
                                               ("Python Files",
                                                "*.py"), ("All Files", "*.*")
                                           ))

    if text_file:
        global open_status_name
        open_status_name = text_file

    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("E:/", "")
    root.title(f'{name}')

    text_file = open(text_file, 'r')
    lines = text_file.read()
    my_text.insert(END, lines)
    text_file.close()


def save_as_file(e):
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="E:/", title="Save File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"),
        ("Python Files", "*.py"), ("All Files", "*.*")
    ))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("E:/", "")
        root.title(f'{name}')

    text_file = open(text_file, 'w')
    text_file.write(my_text.get(1.0, END))

    text_file.close()


def save_file(e):
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

        status_bar.config(text=f'Saved: {open_status_name}        ')

    else:
        save_as_file(e)


file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="(Ctrl+n)")
file_menu.add_command(label="Open", command=open_file, accelerator="(Ctrl+o)")
file_menu.add_command(label="Save", command=save_file, accelerator="(Ctrl+s)")
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.bind('<Control-Key-n>', new_file)
root.bind('<Control-Key-o>', open_file)
root.bind('<Control-Key-s>', save_file)


def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


def select_all(e):
    my_text.tag_add('sel', '1.0', 'end')


edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(
    False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(
    False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste", command=lambda: paste_text(
    False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(
    label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(
    label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=lambda: select_all(
    True), accelerator="(Ctrl+a)")

root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

root.bind('Control-A', select_all)
root.bind('Control-a', select_all)


def bold():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    my_text.tag_configure("bold", font=bold_font)
    current_tags = my_text.tag_names("sel.first")

    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")

    else:
        my_text.tag_add("bold", "sel.first", "sel.last")


def italic():
    italic_font = font.Font(my_text, my_text.cget("font"))
    italic_font.configure(slant="italic")

    my_text.tag_configure("italic", font=italic_font)
    current_tags = my_text.tag_names("sel.first")

    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")

    else:
        my_text.tag_add("italic", "sel.first", "sel.last")


bold_icon = ImageTk.PhotoImage(Image.open(
    "icons/bold.png").resize((15, 15), Image.LANCZOS))
bold_button = Button(toolbar_frame, borderwidth=0.,
                     image=bold_icon, command=bold)
bold_button.grid(row=0, column=3, sticky=W, padx=8, pady=2)

italic_icon = ImageTk.PhotoImage(Image.open(
    "icons/italics.png").resize((15, 15), Image.LANCZOS))
italic_button = Button(toolbar_frame, borderwidth=0.,
                       image=italic_icon, command=italic)
italic_button.grid(row=0, column=4, sticky=W, padx=8, pady=2)

root.mainloop()
