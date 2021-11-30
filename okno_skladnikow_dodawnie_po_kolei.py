from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Przepis')
root.geometry("500x600")

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = 'lightblue'
saved_secondary_color = 'white'
saved_highlight_color = '#347083'


def query_database(which_card):
    if which_card == 1:

        # Clear the Treeview
        for record in recipes_tree.get_children():
            recipes_tree.delete(record)

        conn = sqlite3.connect('przepisy.db')
        c = conn.cursor()

        c.execute("SELECT nazwa, kategoria, ulubione FROM przepisy")

        records = c.fetchall()

        # Add our data to the screen
        global count_1
        count_1 = 0

        for record in records:
            if count_1 % 2 == 0:
                recipes_tree.insert(parent='', index='end', iid=count_1, text='',
                                    values=(record[0], record[1], record[2]),
                                    tags=('evenrow',))
            else:
                recipes_tree.insert(parent='', index='end', iid=count_1, text='',
                                    values=(record[0], record[1], record[2]),
                                    tags=('oddrow',))
            count_1 += 1

        conn.commit()

        conn.close()

    if which_card == 2:

        # Clear the Treeview
        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = sqlite3.connect('przepisy.db')
        c = conn.cursor()

        c.execute('''SELECT przepis, składniki.nazwa, ilość, rodzaje_jednostek.nazwa
                    FROM przepis_z_składnikami
                    INNER JOIN składniki
                    ON przepis_z_składnikami.składnik = składniki.ID
                    INNER JOIN rodzaje_jednostek
                    ON przepis_z_składnikami.jednostka = rodzaje_jednostek.ID''')

        records = c.fetchall()

        # Add our data to the screen
        global count_2
        count_2 = 0
        for record in records:
            if count_2 % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count_2, text='',
                               values=(count_2 + 1, record[1], record[2], record[3]),
                               tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count_2, text='',
                               values=(count_2 + 1, record[1], record[2], record[3]),
                               tags=('oddrow',))
            # increment counter
            count_2 += 1

        conn.commit()

        conn.close()


def task_1():
    print("1")


def task_2():
    print("1")


def task_3():
    print("1")


def task_4():
    print("1")


def add_menu():
    # Add Menu
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # Configure our menu
    option_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Options", menu=option_menu)
    # Drop down menu
    option_menu.add_command(label="Primary Color", command=task_1)
    option_menu.add_command(label="Secondary Color", command=task_2)
    option_menu.add_command(label="Highlight Color", command=task_3)
    option_menu.add_separator()
    option_menu.add_command(label="Reset Colors", command=task_4)
    option_menu.add_separator()
    option_menu.add_command(label="Exit", command=root.quit)


add_menu()

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Lista przepisów')
tabControl.add(tab2, text='Przepis')
tabControl.add(tab3, text='Lodówka')
tabControl.pack(expand=1, fill="both")

conn = sqlite3.connect('przepisy.db')

# Create a cursor instance
c = conn.cursor()

# Create Table
c.execute('''CREATE TABLE if not exists przepis_z_składnikami(
    przepis INT,   
    składnik INT, 
    ilość REAL, 
    jednostka INT)''')

# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

# Change Selected Color #347083
style.map('Treeview',
          background=[('selected', saved_highlight_color)])


# Update record
def update_record():
    # Grab the record number
    selected = recipes_tree.focus()
    # Update record
    recipes_tree.item(selected, text="", values=(
        id_entry.get(), name_entry.get(), cmb_category.current(), cmb_favorite.current(),))

    # Create a database or connect to one that exists
    conn = sqlite3.connect('przepisy.db')

    # Create a cursor instance
    c = conn.cursor()

    # TAB 1
    if tabControl.index(tabControl.select()) == 0:
        # Update the database

        c.execute("""UPDATE przepisy SET
                 nazwa  = :name,
                 kategoria = :category,
                 ulubione = :favorite
    
                 WHERE oid = :oid""",
                  {

                      'oid': id_entry.get(),
                      'name': name_entry.get(),
                      'category': cmb_category.get(),
                      'favorite': cmb_favorite.get(),

                  })

        # Clear entry boxes
        recipe_entry.delete(0, END)
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

    # TAB 2
    if tabControl.index(tabControl.select()) == 1:
        # Grab the record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(
            recipe_entry.get(), ingredient_entry.get(), quantity_entry.get(), cmb.current(),))

        # Update the database

        c.execute("""UPDATE przepis_z_składnikami SET
          składnik = :ingredient,
          ilość = :quantity,
          jednostka = :unit

          WHERE oid = :oid""",
                  {
                      'oid': recipe_entry.get(),
                      'ingredient': ingredient_entry.get(),
                      'quantity': quantity_entry.get(),
                      'unit': cmb.current(),

                  })

        # Clear entry boxes
        recipe_entry.delete(0, END)
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()


# Select Record
def select_record(e):
    # Tab 1
    if tabControl.index(tabControl.select()) == 0:
        # Clear entry boxes
        id_entry.delete(0, END)
        name_entry.delete(0, END)


        # Grab record Number
        selected = recipes_tree.focus()
        # Grab record values
        values = recipes_tree.item(selected, 'values')

        # outpus to entry boxes
        name_entry.insert(0, values[0])
        cmb_category.set(values[1])
        if values[2] == "1":
            cmb_favorite.set("tak")
        else:
            cmb_favorite.set("nie")

    # TAB 2
    if tabControl.index(tabControl.select()) == 1:
        # Clear entry boxes
        recipe_entry.delete(0, END)
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        # outpus to entry boxes
        recipe_entry.insert(0, values[0])
        ingredient_entry.insert(0, values[1])
        quantity_entry.insert(0, values[2])
        cmb.current(values[3])

    # TAB 3
    if tabControl.index(tabControl.select()) == 2:
        print("3")


# add new record to database
def add_record():
    conn = sqlite3.connect('przepisy.db')
    c = conn.cursor()

    # Add New Record
    if tabControl.index(tabControl.select()) == 0:
        c.execute("INSERT INTO przepisy VALUES (:ID, :nazwa, :kategoria, :ulubione)",
                  {
                      'ID': id_entry.get(),
                      'nazwa': name_entry.get(),
                      'kategoria': cmb_category.get(),
                      'ulubione': cmb_favorite.get(),

                  })
        # Clear entry boxes
        id_entry.delete(0, END)
        name_entry.delete(0, END)


        # Clear The Treeview Table
        recipes_tree.delete(*recipes_tree.get_children())

        conn.commit()
        conn.close()

        # Run to pull data from database on start
        query_database(1)

    if tabControl.index(tabControl.select()) == 1:
        c.execute("INSERT INTO przepis_z_składnikami VALUES (:id, :składnik, :ilość, :jednostka)",
                  {
                      'id': recipe_entry.get(),
                      'składnik': ingredient_entry.get(),
                      'ilość': quantity_entry.get(),
                      'jednostka': cmb.current(),
                  })

        # Clear entry boxes
        recipe_entry.delete(0, END)
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Clear The Treeview Table
        my_tree.delete(*my_tree.get_children())

        conn.commit()
        conn.close()

        # Run to pull data from database on start
        query_database(2)


# Remove one record
def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('przepisy.db')

    # Create a cursor instance
    c = conn.cursor()

    # Delete From Database
    c.execute("DELETE from przepis_z_składnikami WHERE oid=" + recipe_entry.get())

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

    # Clear The Entry Boxes
    clear_entries()

    # Add a little message box for fun
    messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")


def clear_entries():
    # Clear entry boxes
    recipe_entry.delete(0, END)
    ingredient_entry.delete(0, END)
    quantity_entry.delete(0, END)


class edit_buttons:

    def __init__(self, tree, tab):
        button_frame = LabelFrame(tab, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        add_button = Button(button_frame, text="Add Record", command=lambda: add_record())
        add_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
        remove_one_button.grid(row=0, column=3, padx=10, pady=10)

        # Bind the treeview
        tree.bind("<ButtonRelease-1>", select_record)


# <editor-fold desc="TAB 1">
# Recipes FRAME

recipes_frame = Frame(tab1)
recipes_frame.pack(pady=10, fill=Y)

# <editor-fold desc="Treeview">
# Create a Treeview Scrollbar
tree_scroll = Scrollbar(recipes_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
#
# Create The Treeview
recipes_tree = ttk.Treeview(recipes_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
recipes_tree.pack()
#
# Configure the Scrollbar
tree_scroll.config(command=recipes_tree.yview)

# Define Our Columns
recipes_tree['columns'] = ("Nazwa", "Kategoria", "Ulubione")

# Format Our Columns
recipes_tree.column("#0", width=0, stretch=NO)
recipes_tree.column("Nazwa", anchor=W, width=140)
recipes_tree.column("Kategoria", anchor=W, width=60)
recipes_tree.column("Ulubione", anchor=W, width=60)

recipes_tree.heading("#0", text="", anchor=W)
recipes_tree.heading("Nazwa", text="Nazwa", anchor=CENTER)
recipes_tree.heading("Kategoria", text="Kategoria", anchor=CENTER)
recipes_tree.heading("Ulubione", text="Ulubione", anchor=CENTER)

# Create Striped Row Tags
recipes_tree.tag_configure('oddrow', background=saved_secondary_color)
recipes_tree.tag_configure('evenrow', background=saved_primary_color)
# </editor-fold>

data_frame1 = LabelFrame(tab1, text="Record")
data_frame1.pack(fill="x", expand="yes", padx=20)

id_label = Label(data_frame1, text="ID")
id_label.grid(row=1, column=0, padx=10, pady=10)
id_entry = Entry(data_frame1)
id_entry.grid(row=1, column=1, padx=10, pady=10)

name_label = Label(data_frame1, text="Nazwa")
name_label.grid(row=1, column=2, padx=10, pady=10)
name_entry = Entry(data_frame1)
name_entry.grid(row=1, column=3, padx=10, pady=10)

conn = sqlite3.connect('przepisy.db')
c = conn.cursor()
c.execute('''SELECT nazwa_kategorii FROM kategorie''')
category_input_cmb = c.fetchall()
conn.close()

category_label = Label(data_frame1, text="Kategoria")
category_label.grid(row=2, column=0, padx=10, pady=10)
cmb_category = ttk.Combobox(data_frame1, value=category_input_cmb, width=15)
cmb_category.grid(row=2, column=1, padx=10, pady=10)

favorite_label = Label(data_frame1, text="Ulubione")
favorite_label.grid(row=2, column=2, padx=10, pady=10)
cmb_favorite = ttk.Combobox(data_frame1, width=15)
cmb_favorite['values'] = ('nie', 'tak')
cmb_favorite.grid(row=2, column=3, padx=10, pady=10)
cmb_favorite.current(0)

# </editor-fold>


# <editor-fold desc="TAB 2">
# Create a Treeview Frame
tree_frame = Frame(tab2)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
my_tree_scroll = Scrollbar(tree_frame)
my_tree_scroll.pack(side=RIGHT, fill=Y)
#
# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=my_tree_scroll.set, selectmode="extended")
my_tree.pack()
#
# Configure the Scrollbar
my_tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("ID", "Składnik", "Ilość", "Jednostka")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=140)
my_tree.column("Składnik", anchor=W, width=140)
my_tree.column("Ilość", anchor=CENTER, width=60)
my_tree.column("Jednostka", anchor=CENTER, width=60)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Składnik", text="Składnik", anchor=CENTER)
my_tree.heading("Ilość", text="Ilość", anchor=CENTER)
my_tree.heading("Jednostka", text="Jednostka", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(tab2, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

recipe_label = Label(data_frame, text="ID")
recipe_label.grid(row=1, column=0, padx=10, pady=10)
recipe_entry = Entry(data_frame)
recipe_entry.grid(row=1, column=1, padx=10, pady=10)

ingredient_label = Label(data_frame, text="Składnik")
ingredient_label.grid(row=1, column=2, padx=10, pady=10)
ingredient_entry = Entry(data_frame)
ingredient_entry.grid(row=1, column=3, padx=10, pady=10)

quantity_label = Label(data_frame, text="Ilość")
quantity_label.grid(row=2, column=0, padx=10, pady=10)
quantity_entry = Entry(data_frame)
quantity_entry.grid(row=2, column=1, padx=10, pady=10)

conn = sqlite3.connect('przepisy.db')
c = conn.cursor()
c.execute('''SELECT nazwa FROM rodzaje_jednostek''')
units_options = c.fetchall()
conn.close()

unit_label = Label(data_frame, text="Jednostka")
unit_label.grid(row=2, column=2, padx=10, pady=10)
cmb = ttk.Combobox(data_frame, value=units_options, width=15)
cmb.grid(row=2, column=3, padx=10, pady=10)
cmb.current(3)


# </editor-fold>

def add_buttons_tab1():
    button_frame_tab1 = LabelFrame(tab1, text="Commands")
    button_frame_tab1.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame_tab1, text="Update Record", command=lambda: update_record())
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame_tab1, text="Add Record", command=lambda: add_record())
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame_tab1, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    # Bind the treeview
    recipes_tree.bind("<ButtonRelease-1>", select_record)


def add_buttons_tab2():
    button_frame = LabelFrame(tab2, text="Commands")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Update Record", command=lambda: update_record())
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Add Record", command=lambda: add_record())
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>", select_record)


add_buttons_tab1()
add_buttons_tab2()

query_database(1)
query_database(2)

# query_database1(recipes_tree, 1)
# query_database1(my_tree, 2)


root.mainloop()
