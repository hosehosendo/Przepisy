from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('Przepis')
root.geometry("650x600")

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = 'lightblue'
saved_secondary_color = 'white'
saved_highlight_color = '#347083'




def create_tables():

    conn = sqlite3.connect('przepisy.db')
    c = conn.cursor()

    # stworzenie tabeli przepisow
    c.execute(
        '''CREATE TABLE if not exists przepisy(ID INTEGER  PRIMARY KEY AUTOINCREMENT, nazwa TEXT, kategoria TEXT, ulubione BIT, opis TEXT)''')

    # stworzenie tabeli składnikow
    c.execute(
        '''CREATE TABLE if not exists składniki(ID INT, nazwa TEXT, kcal REAL, białka REAL, tłuszcze REAL, węglowodany REAL, rodzaj INT, na stanie NULL)''')

    # stworzenie tabeli rodzajow jednostek
    c.execute('''CREATE TABLE if not exists rodzaje_jednostek(ID INT, nazwa TEXT, skrót TEXT,	rodzaj TEXT)''')

    # stworzenie tabeli przepisow ze skladnikami i ich iloscia. jednostką i rodzajem jednostki many-to-many relation
    c.execute(
        '''CREATE TABLE if not exists przepis_z_składnikami(przepis INT,składnik INT, ilość REAL, jednostka INT)''')

    # stworzenie tabeli z kategoriami przepisów
    c.execute('''CREATE TABLE if not exists kategorie(ID integer PRIMARY KEY, nazwa_kategorii TEXT)''')


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
                    ON przepis_z_składnikami.jednostka = rodzaje_jednostek.ID
                    WHERE przepis =(?)''', (active_recipe_id,))

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


def info():
    response = messagebox.showinfo(" Info", "Cześć stworzyłem tą aplikację, żeby w łatwy sposób "
                                            "można było znaleźć przepis po zawartości produktów, "
                                            "które aktualnie posiadasz. W pierwsze zakładce są przepisy,"
                                            "w drugiej składniki i opis przepisu, a w trzeciej produkty, które posiadasz."
                                            " kontakt : hubertlosofficial@gmail.com")


def add_menu():
    # Add Menu
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # Configure our menu
    option_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Options", menu=option_menu)
    # Drop down menu
    option_menu.add_command(label="Info", command=info)
    option_menu.add_separator()
    option_menu.add_command(label="Wyjście", command=root.quit)


def open_recipe():
    # open tab 2
    tabControl.select(1)

    # Grab record Number
    selected = recipes_tree.focus()
    # Grab record values
    values = recipes_tree.item(selected, 'values')

    conn = sqlite3.connect('przepisy.db')
    c = conn.cursor()

    c.execute("SELECT ID FROM przepisy WHERE nazwa=(?)", ((values[0]),))

    records = c.fetchall()

    global active_recipe_id
    active_recipe_id = records[0][0]
    print(records[0][0])
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    c.execute('''SELECT przepis, składniki.nazwa, ilość, rodzaje_jednostek.nazwa
            FROM przepis_z_składnikami 
            INNER JOIN składniki 
            ON przepis_z_składnikami.składnik = składniki.ID
            INNER JOIN rodzaje_jednostek 
            ON przepis_z_składnikami.jednostka = rodzaje_jednostek.ID
            WHERE przepis =(?)''', (active_recipe_id,))

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

    c.execute("SELECT opis FROM przepisy WHERE ID=(?)", (active_recipe_id,))

    conn.commit()

    conn.close()


# Update record
def update_record():
    # Grab the record number
    selected = recipes_tree.focus()
    # Update record
    recipes_tree.item(selected, text="", values=(
        name_entry.get(), cmb_category.current(), cmb_favorite.current(),))

    # Create a database or connect to one that exists
    conn = sqlite3.connect('przepisy.db')

    # Create a cursor instance
    c = conn.cursor()

    # TAB 1
    if tabControl.index(tabControl.select()) == 0:
        # Update the database
        # Grab the record number
        selected = recipes_tree.focus()
        # Update record
        recipes_tree.item(selected, text="", values=(
            name_entry.get(), cmb_category.get(), cmb_favorite.get(),))

        c.execute("""UPDATE przepisy SET
                 nazwa  = (?),
                 kategoria = (?),
                 ulubione = (?)

                 WHERE nazwa = (?)""", (name_entry.get(), cmb_category.get(), cmb_favorite.get(), name_entry.get()))

        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

    # TAB 2
    if tabControl.index(tabControl.select()) == 1:
        # Grab the record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(
            ingredient_entry.get(), quantity_entry.get(), cmb.current(),))

        # Update the database

        global select_ingredient

        c.execute("SELECT ID FROM składniki WHERE nazwa = (?)", (ingredient_entry.get(),))

        result_ingredient = c.fetchall()


        c.execute("""UPDATE przepis_z_składnikami SET
          składnik = :ingredient,
          ilość = :quantity,
          jednostka = :unit

          WHERE ROWID  = :oid""",
                  {
                      'ingredient': result_ingredient[0][0],
                      'quantity': quantity_entry.get(),
                        'unit': (cmb.current()+1),
                        'oid': select_ingredient,
                  })

        # Clear entry boxes
        # c.execute("INSERT INTO przepisy (opis) VALUES (?)", (description_entry.get(), ))

        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

    query_database(2)

# Select Record
def select_record(e):

    # Tab 1
    if tabControl.index(tabControl.select()) == 0:
        # Clear entry boxes
        name_entry.delete(0, END)

        # Grab record Number
        selected = recipes_tree.focus()
        # Grab record values
        values = recipes_tree.item(selected, 'values')

        # outpus to entry boxes
        name_entry.insert(0, values[0])
        cmb_category.set(values[1])
        cmb_favorite.set(values[2])

    # TAB 2
    if tabControl.index(tabControl.select()) == 1:
        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        # outpus to entry boxes
        ingredient_entry.insert(0, values[1])
        quantity_entry.insert(0, values[2])
        cmb.set(values[3])

        conn = sqlite3.connect('przepisy.db')
        c = conn.cursor()


        c.execute('''SELECT przepis_z_składnikami.rowid FROM przepis_z_składnikami 
                  INNER JOIN składniki 
                  ON przepis_z_składnikami.składnik = składniki.ID
                  WHERE składniki.nazwa = (?) AND ilość = (?) ''', (values[1], values[2],))


        result = c.fetchall()

        global select_ingredient
        select_ingredient = result[0][0]


        conn.commit()
        conn.close()

    # TAB 3
    if tabControl.index(tabControl.select()) == 2:
        print("3")


# add new record to database
def add_record():
    conn = sqlite3.connect('przepisy.db')
    c = conn.cursor()
    typ_id = int()
    # Add New Record
    if tabControl.index(tabControl.select()) == 0:
        c.execute("INSERT INTO przepisy (nazwa, kategoria, ulubione) VALUES (?,?,?)",
                  (name_entry.get(), cmb_category.get(), cmb_favorite.get()))
        # Clear entry boxes
        name_entry.delete(0, END)

        # Clear The Treeview Table
        recipes_tree.delete(*recipes_tree.get_children())

        conn.commit()
        conn.close()

        # Run to pull data from database on start
        query_database(1)

    if tabControl.index(tabControl.select()) == 1:

        c.execute("SELECT ID FROM składniki WHERE nazwa = (?)", (ingredient_entry.get(),))

        result = c.fetchall()

        c.execute("INSERT INTO przepis_z_składnikami VALUES (:przepis, :składnik, :ilość, :jednostka)",
                  {
                      'przepis': active_recipe_id,
                      'składnik': result[0][0],
                      'ilość': quantity_entry.get(),
                      'jednostka': (cmb.current()+1),
                  })


        # c.execute("INSERT INTO przepisy (opis) VALUES (?)", (description_entry.get()))

        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Clear The Treeview Table
        my_tree.delete(*my_tree.get_children())

        conn.commit()
        conn.close()

        # Run to pull data from database on start
        query_database(2)


def remove_all():
    # Add a little message box for fun
    response = messagebox.askyesno("Uwaga", "Zostaną usunięte wszystkie przepisy, jesteś pewny?!")

    # Add logic for message box

    if response == 1:
        # Create a database or connect to one that exists
        conn = sqlite3.connect('przepisy.db')

        # Create a cursor instance
        c = conn.cursor()

        if tabControl.index(tabControl.select()) == 0:

            # Clear the Treeview
            for record in recipes_tree.get_children():
                recipes_tree.delete(record)

            # Delete Everything From The Table
            c.execute("DROP TABLE przepisy")

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            create_tables()

        if tabControl.index(tabControl.select()) == 1:

            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            # Delete Everything From The Table
            c.execute("DROP TABLE przepis_z_składnikami")

            # Create a database or connect to one that exists
            conn = sqlite3.connect('przepisy.db')

            # Create a cursor instance
            c = conn.cursor()

            # Create Table
            c.execute(
                '''CREATE TABLE if not exists przepis_z_składnikami(przepis INT,składnik INT, ilość REAL, jednostka INT)''')

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            create_tables()

        # Clear entry boxes if filled
        clear_entries()


# Remove one record
def remove_one():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('przepisy.db')

    # Create a cursor instance
    c = conn.cursor()

    if tabControl.index(tabControl.select()) == 0:
        x = recipes_tree.selection()[0]
        recipes_tree.delete(x)
        c.execute("DELETE from przepisy WHERE nazwa=?", (name_entry.get()))

    if tabControl.index(tabControl.select()) == 1:
        x = my_tree.selection()[0]
        my_tree.delete(x)
        c.execute("DELETE from przepis_z_składnikami WHERE nazwa=?", (name_entry.get()))

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
    ingredient_entry.delete(0, END)
    quantity_entry.delete(0, END)


def add_buttons_tab1():
    button_frame_tab1 = LabelFrame(tab1, text="Commands")
    button_frame_tab1.pack(fill="x", expand="yes", padx=20)

    open_recipe_button = Button(button_frame_tab1, text="Otwórz przepis", command=lambda: open_recipe())
    open_recipe_button.grid(row=0, column=0, padx=10, pady=10)

    update_button = Button(button_frame_tab1, text="Update Record", command=lambda: update_record())
    update_button.grid(row=0, column=1, padx=10, pady=10)

    add_button = Button(button_frame_tab1, text="Add Record", command=lambda: add_record())
    add_button.grid(row=0, column=2, padx=10, pady=10)

    remove_all_button = Button(button_frame_tab1, text="Remove All Records", command=remove_all)
    remove_all_button.grid(row=1, column=0, padx=10, pady=10)

    remove_one_button = Button(button_frame_tab1, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=1, column=1, padx=10, pady=10)

    # Bind the treeview
    recipes_tree.bind("<ButtonRelease-1>", select_record)
    # recipes_tree.bind("<Double-1>", open_recipe)


def add_buttons_tab2():
    button_frame = LabelFrame(tab2, text="Commands")
    button_frame.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame, text="Update Record", command=lambda: update_record())
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame, text="Add Record", command=lambda: add_record())
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
    remove_all_button.grid(row=0, column=2, padx=10, pady=10)
    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>", select_record)
    # my_tree.bind("<Double-1>", open_recipe)


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

active_recipe_id = 0
select_ingredient = 0

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

def double_open(event):
    open_recipe()

recipes_tree.bind('<Double 1>', double_open)
# </editor-fold>

data_frame1 = LabelFrame(tab1, text="Record")
data_frame1.pack(fill="x", expand="yes", padx=20)

# id_label = Label(data_frame1, text="ID")
# id_label.grid(row=1, column=0, padx=10, pady=10)
# id_entry = Entry(data_frame1)
# id_entry.grid(row=1, column=1, padx=10, pady=10)

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
category_label.grid(row=1, column=4, padx=10, pady=10)
cmb_category = ttk.Combobox(data_frame1, value=category_input_cmb, width=15)
cmb_category.grid(row=1, column=5, padx=10, pady=10)
cmb_category.current(1)

# def open_cmb(event):
#     w = event.widget
#     w.event_generate('<Down>', when='head')
#
# cmb_category.bind("<Button-1>", open_cmb)


favorite_label = Label(data_frame1, text="Ulubione")
favorite_label.grid(row=2, column=2, padx=10, pady=10)
cmb_favorite = ttk.Combobox(data_frame1, width=15)
cmb_favorite['values'] = ('nie', 'tak')
cmb_favorite.grid(row=2, column=3, padx=10, pady=10)
cmb_favorite.current(0)

def combo_events(evt):
    w = evt.widget
    w.event_generate('<Down>')

cmb_favorite.bind('<Button-1>', combo_events)

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
my_tree.column("ID", anchor=W, width=40)
my_tree.column("Składnik", anchor=W, width=200)
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

description_frame = LabelFrame(tab2, text="Opis")
description_frame.pack(fill="x", expand="yes", padx=20)

description_entry = Entry(description_frame)
description_entry.grid(row=1, column=0, padx=10, pady=10, ipady=60, ipadx=200)

# Add Record Entry Boxes
data_frame = LabelFrame(tab2, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

ingredient_label = Label(data_frame, text="Składnik")
ingredient_label.grid(row=1, column=0, padx=5, pady=5)
ingredient_entry = Entry(data_frame)
ingredient_entry.grid(row=1, column=1, padx=5, pady=5)

quantity_label = Label(data_frame, text="Ilość")
quantity_label.grid(row=1, column=2, padx=5, pady=5)
quantity_entry = Entry(data_frame)
quantity_entry.grid(row=1, column=3, padx=5, pady=5)

conn = sqlite3.connect('przepisy.db')
c = conn.cursor()
c.execute('''SELECT nazwa FROM rodzaje_jednostek''')
units_options = c.fetchall()
conn.close()

unit_label = Label(data_frame, text="Jednostka")
unit_label.grid(row=1, column=4, padx=5, pady=5)
cmb = ttk.Combobox(data_frame, value=units_options, width=15)
cmb.grid(row=1, column=5, padx=5, pady=5)
cmb.current(3)

# </editor-fold>


add_buttons_tab1()
add_buttons_tab2()

query_database(1)
query_database(2)

root.mainloop()