from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
import sqlite3
from configparser import ConfigParser
# import lodowka


root = Tk()
root.title('Przepisy')
root.geometry("650x600")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# Read our config file and get colors
saved_primary_color = 'lightblue'
saved_secondary_color = 'white'
saved_highlight_color = '#333333'


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
    c.execute('''CREATE TABLE if not exists rodzaje_jednostek(ID INT, nazwa TEXT, skrót TEXT,  rodzaj TEXT)''')

    # stworzenie tabeli przepisow ze skladnikami i ich iloscia. jednostką i rodzajem jednostki many-to-many relation
    c.execute(
        '''CREATE TABLE if not exists przepis_z_składnikami(przepis INT,składnik INT, ilość REAL, jednostka INT)''')

    # stworzenie tabeli z kategoriami przepisów
    c.execute('''CREATE TABLE if not exists kategorie(ID integer PRIMARY KEY, nazwa_kategorii TEXT)''')

    # stworzenie tabeli z kategoriami przepisów
    c.execute('''CREATE TABLE if not exists lodówka(ID integer PRIMARY KEY, produkt INT)''')


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

    if which_card == 3:

        # Clear the Treeview
        for record in fridge_tree.get_children():
            fridge_tree.delete(record)

        conn = sqlite3.connect('przepisy.db')
        c = conn.cursor()

        c.execute('''SELECT produkt
                    FROM lodówka''')

        records = c.fetchall()

        # Add our data to the screen
        global count_3
        count_3 = 0
        for record in records:
            if count_3 % 2 == 0:
                fridge_tree.insert(parent='', index='end', iid=count_3, text='',
                                   values=(count_3 + 1, record[0]),
                                   tags=('evenrow',))
            else:
                fridge_tree.insert(parent='', index='end', iid=count_3, text='',
                                   values=(count_3 + 1, record[0]),
                                   tags=('oddrow',))
            # increment counter
            count_3 += 1

        conn.commit()

        conn.close()


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

    result = c.fetchall()
    print(result[0][0])

    description_entry.config(state='normal')
    description_entry.delete(0, "end")
    description_entry.insert(0, result[0][0])
    description_entry.config(state='disabled')

    conn.commit()

    conn.close()


# Update record
def update_record():
    # Grab the record number
    selected = recipes_tree.focus()
    # Update record
    recipes_tree.item(selected, text="", values=(
        name.entry.get(), category_cmb.combobox.current(), favorite_cmb.combobox.current(),))

    conn = sqlite3.connect('przepisy.db')
    c = conn.cursor()

    # TAB 1
    if tabControl.index(tabControl.select()) == 0:
        # Update the database
        # Grab the record number
        selected = recipes_tree.focus()
        # Update record
        recipes_tree.item(selected, text="", values=(
            name.entry.get(), category_cmb.combobox.get(), favorite_cmb.combobox.get(),))

        c.execute("""UPDATE przepisy SET
                 nazwa  = (?),
                 kategoria = (?),
                 ulubione = (?)

                 WHERE nazwa = (?)""",
                  (name.entry.get(), category_cmb.combobox.get(), favorite_cmb.combobox.get(), name.entry.get()))

        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity.entry.delete(0, END)

    # TAB 2
    if tabControl.index(tabControl.select()) == 1:
        # Grab the record number
        selected = my_tree.focus()
        # Update record
        my_tree.item(selected, text="", values=(
            ingredient_entry.get(), quantity.entry.get(), unit.combobox.current(),))

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
                      'quantity': quantity.entry.get(),
                      'unit': (unit.combobox.current() + 1),
                      'oid': select_ingredient,
                  })

        c.execute("UPDATE przepisy SET opis = (?) WHERE ID = (?)", (description_entry.get(), active_recipe_id,))

        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity.entry.delete(0, END)

    conn.commit()
    conn.close()

    query_database(2)


# Select Record
def select_record(e):
    # Tab 1
    if tabControl.index(tabControl.select()) == 0:
        # Clear entry boxes
        name.entry.delete(0, END)

        # Grab record Number
        selected = recipes_tree.focus()
        # Grab record values
        values = recipes_tree.item(selected, 'values')

        # outpus to entry boxes
        name.entry.insert(0, values[0])
        category_cmb.combobox.set(values[1])
        favorite_cmb.combobox.set(values[2])

    # TAB 2
    if tabControl.index(tabControl.select()) == 1:
        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity.entry.delete(0, END)

        # Grab record Number
        selected = my_tree.focus()
        # Grab record values
        values = my_tree.item(selected, 'values')

        # outpus to entry boxes
        ingredient_entry.insert(0, values[1])
        quantity.entry.insert(0, values[2])
        unit.combobox.set(values[3])

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
        # Grab record Number
        selected = fridge_tree.focus()
        # Grab record values
        values = fridge_tree.item(selected, 'values')

        print(values)

        # outputs to entry boxes
        product_entry.set(values[1])


# add new record to database
def add_record():
    conn = sqlite3.connect('przepisy.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()

    # Add New Record
    if tabControl.index(tabControl.select()) == 0:

        # checking if a name is already given

        c.execute("SELECT nazwa FROM przepisy")

        result = c.fetchall()

        if name.entry.get() in result:
            response = messagebox.showinfo(" Info",
                                           "Ta nazwa jest już zajęta.")

        else:
            c.execute("INSERT INTO przepisy (nazwa, kategoria, ulubione) VALUES (?,?,?)",
                      (name.entry.get(), category_cmb.combobox.get(), favorite_cmb.combobox.get()))
            # Clear entry boxes
            name.entry.delete(0, END)

            # Clear The Treeview Table
            recipes_tree.delete(*recipes_tree.get_children())

            conn.commit()
            conn.close()

            # Run to pull data from database on start
            query_database(1)

    if tabControl.index(tabControl.select()) == 1:

        c.execute("SELECT ID FROM składniki WHERE nazwa = (?)", (ingredient_entry.get(),))

        result = c.fetchall()

        if len(result) == 1:

            c.execute("INSERT INTO przepis_z_składnikami VALUES (:przepis, :składnik, :ilość, :jednostka)",
                      {
                          'przepis': active_recipe_id,
                          'składnik': result[0],
                          'ilość': quantity.entry.get(),
                          'jednostka': (unit.combobox.current() + 1),
                      })
        else:

            # response = messagebox.showinfo(" Info", "Brak takiego składnika, dodawanie nowych składników jest przygotowywane ;)")
            response = messagebox.askyesno("Brak składnika", "Czy chcesz dodać ten składnik do bazy?")
            if response == 1:
                add_new_ingradient()

        # Clear entry boxes
        ingredient_entry.delete(0, END)
        quantity.entry.delete(0, END)

        # Clear The Treeview Table
        my_tree.delete(*my_tree.get_children())

        conn.commit()
        conn.close()

        # Run to pull data from database on start
        query_database(2)

    if tabControl.index(tabControl.select()) == 2:

        c.execute("SELECT ID FROM składniki WHERE nazwa = (?)", (product_entry.get(),))

        result = c.fetchall()

        if len(result) == 1:

            c.execute("SELECT ID FROM lodówka WHERE produkt = (?)", (result[0],))

            result2 = c.fetchall()
            if len(result2) == 0:

                c.execute("INSERT INTO lodówka (produkt) VALUES (?)", (result,))

            else:
                response = messagebox.showinfo(" Info",
                                               "Ten produkt jest już w twojej lodówce")

        else:

            response = messagebox.showinfo(" Info",
                                           "Brak takiego składnika, dodawanie nowych składników jest przygotowywane ;)")
            # response = messagebox.askyesno("Brak składnika", "Czy chcesz dodać ten składnik do bazy?")
            # if response == 1:
            #     add_new_ingradient()

        # Clear entry boxes
        product_entry.delete(0, END)

        # Clear The Treeview Table
        fridge_tree.delete(*fridge_tree.get_children())

        conn.commit()
        conn.close()

        # Run to pull data from database on start
        query_database(3)


def info():
    response = messagebox.showinfo(" Info", "Cześć stworzyłem tą aplikację, żeby w łatwy sposób "
                                            "można było znaleźć przepis po zawartości produktów, "
                                            "które aktualnie posiadasz. W pierwsze zakładce są przepisy,"
                                            "w drugiej składniki i opis przepisu, a w trzeciej produkty, które posiadasz."
                                            " kontakt : hubertlosofficial@gmail.com")


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


def remove_one():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('przepisy.db')

    # Create a cursor instance
    c = conn.cursor()

    if tabControl.index(tabControl.select()) == 0:
        x = recipes_tree.selection()[0]
        recipes_tree.delete(x)
        c.execute("DELETE from przepisy WHERE nazwa=?", (name.entry.get(),))

    if tabControl.index(tabControl.select()) == 1:
        x = my_tree.selection()[0]
        my_tree.delete(x)
        c.execute("DELETE from przepis_z_składnikami WHERE nazwa=?", (name.entry.get(),))

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

    # Clear The Entry Boxes
    clear_entries()

    # Add a little message box for fun
    messagebox.showinfo("Info!", "Usunięto!")


def clear_entries():
    # Clear entry boxes
    ingredient_entry.delete(0, END)
    quantity.entry.delete(0, END)


def double_open(event):
    open_recipe()


def combo_events(evt):
    w = evt.widget
    w.event_generate('<Down>')


def edit_description():
    if edit_description_button.cget('text') == "Edytuj Opis":
        description_entry.config(state='normal')
        edit_description_button.config(text="OK")
        return
    if edit_description_button.cget('text') == "OK":
        description_entry.config(state='disabled')
        edit_description_button.config(text="Edytuj Opis")

        global select_ingredient

        conn = sqlite3.connect('przepisy.db')
        c = conn.cursor()

        c.execute("UPDATE przepisy SET opis = (?) WHERE ID = (?)", (description_entry.get(), active_recipe_id,))

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        return


def add_buttons_tab1():
    button_frame_tab1 = LabelFrame(tab1, text="Commands")
    button_frame_tab1.pack(fill="x", expand="yes", padx=20)

    width_buttons = 12

    open_recipe_button = Button(button_frame_tab1, text="Otwórz przepis", command=lambda: open_recipe())
    open_recipe_button.grid(row=0, column=0, padx=10, pady=10)
    open_recipe_button.config(width=width_buttons)

    update_button = Button(button_frame_tab1, text="Zaktualizuj", command=lambda: update_record())
    update_button.grid(row=0, column=1, padx=10, pady=10)
    update_button.config(width=width_buttons)

    add_button = Button(button_frame_tab1, text="Dodaj", command=lambda: add_record())
    add_button.grid(row=0, column=2, padx=10, pady=10)
    add_button.config(width=width_buttons)

    remove_all_button = Button(button_frame_tab1, text="Usuń wszystko", command=remove_all)
    remove_all_button.grid(row=0, column=3, padx=10, pady=10)
    remove_all_button.config(width=width_buttons)

    remove_one_button = Button(button_frame_tab1, text="Usuń zaznaczony", command=remove_one)
    remove_one_button.grid(row=0, column=4, padx=10, pady=10)
    remove_one_button.config(width=width_buttons)

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


def add_buttons_tab3():
    add_button3 = Button(data_frame3, text="Dodaj", command=lambda: add_record())
    add_button3.grid(row=1, column=2, padx=10, pady=10)
    add_button3.config(width=15)

    remove_one_button3 = Button(data_frame3, text="Usuń", command=remove_one)
    remove_one_button3.grid(row=1, column=3, padx=10, pady=10)
    remove_one_button3.config(width=15)

    remove_all_button3 = Button(data_frame3, text="Usuń wszystkie", command=remove_all)
    remove_all_button3.grid(row=1, column=4, padx=10, pady=10)
    remove_all_button3.config(width=15)

    button_frame = LabelFrame(tab3, text="Commands")
    button_frame.pack(fill="x", expand="yes", padx=20)

    # find_recipes_button = Button(button_frame, text="Znajdź przepis", command=add_record())
    # find_recipes_button.grid(row=0, column=0, padx=10, pady=10)
    # find_recipes_button.config(width=50)

    # Bind the treeview
    fridge_tree.bind("<ButtonRelease-1>", select_record)


# funkcja do dokończenia
def add_new_ingradient():
    def add_ingradient():
        if ingradient_name.entry.index("end") == 0 or kcal.entry.index("end") == 0 \
                or proteins.entry.index("end") == 0 or fats.entry.index("end") == 0 \
                or carbohydrates.entry.index("end") == 0:
            response = messagebox.showinfo(" Info", "Musisz uzupełnić wszystkie pola!")

        else:
            try:
                kcal_int = int(kcal.entry.get())
                proteins_int = int(proteins.entry.get())
                fats_int = int(fats.entry.get())
                carbohydrates_int = int(carbohydrates.entry.get())

                c.execute("INSERT INTO składniki (kcal, białka, tłuszcze, węglowodany, rodzaj, na stanie) VALUES (?,?,?,?,?,?)",
                          (ingradient_name.entry.get(), kcal_int, proteins_int, fats_int, carbohydrates_int,
                           type_meal.optionmenu.get(), in_stock.optionmenu.get() ))

            except:
                print("Kalorie, białka, tłuszczę i węglowodany muszą być liczbami całkowitymi")

    conn = sqlite3.connect('przepisy.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()

    c.execute("SELECT DISTINCT rodzaj FROM składniki;")

    type_meal_list = c.fetchall()

    # box z dodanie elementów
    root_ingradient = Tk()
    root_ingradient.title('Przepis')
    root_ingradient_width = 400
    root_ingradient_height = 400

    x = (screen_width / 2) - (root_ingradient_width / 2)
    y = (screen_height / 2) - (root_ingradient_height / 2)

    root_ingradient.geometry('%dx%d+%d+%d' % (root_ingradient_width, root_ingradient_height, x, y))


    add_ingradient_frame = LabelFrame(root_ingradient, text="Dodaj składnik")
    add_ingradient_frame.pack(fill="x", expand="yes", padx=20)

    ingradient_name = Entry_with_label(add_ingradient_frame, set_column=1, set_row=1, name="Nazwa")
    kcal = Entry_with_label(add_ingradient_frame, set_column=1, set_row=2, name="Kalorie")
    proteins = Entry_with_label(add_ingradient_frame, set_column=1, set_row=3, name="Białka")
    fats = Entry_with_label(add_ingradient_frame, set_column=1, set_row=4, name="Tłuszcze")
    carbohydrates = Entry_with_label(add_ingradient_frame, set_column=1, set_row=5, name="Węglowadany")
    # combobox
    type_meal = OptionMenu_with_Label(add_ingradient_frame, set_column=1, set_row=6, name="Typ",
                                      include_value=type_meal_list)
    in_stock = OptionMenu_with_Label(add_ingradient_frame, set_column=1, set_row=7, name="Na stanie?",
                                     include_value=["tak", "nie"])

    add_ingradient_button = Button(add_ingradient_frame, text="Dodaj składnik", command=lambda: add_ingradient())
    add_ingradient_button.grid(row=8, column=1, padx=10, pady=10)
    add_ingradient_button.config(width=12)

    #     dodanie elementów do bazy składników
    #     dodanie składika do przepisu

    root_ingradient.mainloop()


class Entry_with_label():

    def __init__(self, frame, set_row, set_column, name):
        self.label = Label(frame, text=name)
        self.label.grid(row=set_row, column=set_column, padx=10, pady=10)
        self.entry = Entry(frame)
        self.entry.grid(row=set_row, column=set_column + 1, padx=10, pady=10)


class Combobox_with_Label():

    def __init__(self, frame, set_row, set_column, current, name, include_value):
        category_label = Label(frame, text=name)
        category_label.grid(row=set_row, column=set_column, padx=10, pady=10)
        self.combobox = ttk.Combobox(frame, value=include_value, width=15)
        self.combobox.grid(row=set_row, column=set_column + 1, padx=10, pady=10)
        self.combobox.current(current)


class OptionMenu_with_Label():

    def __init__(self, frame, set_row, set_column, name, include_value, set_width=20):
        label = Label(frame, text=name)
        label.grid(row=set_row, column=set_column, padx=10, pady=10)
        variable = StringVar(frame)
        variable.set("Wybierz")
        self.optionmenu = ttk.OptionMenu(frame, variable, *include_value)
        self.optionmenu.grid(row=set_row, column=set_column + 1, padx=10, pady=10)
        self.optionmenu.config(width=set_width)


# global variable

active_recipe_id = 0
select_ingredient = 0

add_menu()

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Lista przepisów')
tabControl.add(tab2, text='Przepis')
tabControl.add(tab3, text='Lodówka')
tabControl.pack(expand=1, fill="both")

create_tables()

# Create tree
style = ttk.Style()
style.theme_use('default')

style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=20,
                fieldbackground="#D3D3D3")

style.map('Treeview',
          background=[('selected', saved_highlight_color)])

# <editor-fold desc="TAB 1 - RECIPES">

# Recipes FRAME
recipes_frame = Frame(tab1)
recipes_frame.pack(pady=10, fill=Y)

# <editor-fold desc="Treeview">
# Create a Treeview Scrollbar
tree_scroll = Scrollbar(recipes_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

recipes_tree = ttk.Treeview(recipes_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
recipes_tree.pack()

tree_scroll.config(command=recipes_tree.yview)
recipes_tree['columns'] = ("Nazwa", "Kategoria", "Ulubione")

# Format Columns

recipes_tree.column("#0", width=0, stretch=NO)
recipes_tree.column("Nazwa", anchor=W, width=400)
recipes_tree.column("Kategoria", anchor=W, width=100)
recipes_tree.column("Ulubione", anchor=W, width=100)

recipes_tree.heading("#0", text="", anchor=W)
recipes_tree.heading("Nazwa", text="Nazwa", anchor=CENTER)
recipes_tree.heading("Kategoria", text="Kategoria", anchor=CENTER)
recipes_tree.heading("Ulubione", text="Ulubione", anchor=CENTER)

# Create Striped Row Tags
recipes_tree.tag_configure('oddrow', background=saved_secondary_color)
recipes_tree.tag_configure('evenrow', background=saved_primary_color)

recipes_tree.bind('<Double 1>', double_open)
# </editor-fold>

conn = sqlite3.connect('przepisy.db')
c = conn.cursor()
c.execute('''SELECT nazwa_kategorii FROM kategorie''')
category_input_cmb = c.fetchall()
conn.close()

data_frame1 = LabelFrame(tab1, text="Record")
data_frame1.pack(fill="x", expand="yes", padx=20)

name = Entry_with_label(data_frame1, set_row=1, set_column=2, name="Nazwa")

category_cmb = Combobox_with_Label(data_frame1, set_row=1, set_column=4, current=1, name="Kategoria",
                                   include_value=category_input_cmb)

favorite_cmb = Combobox_with_Label(data_frame1, set_row=2, set_column=2, current=0, name="Ulubione",
                                   include_value=['nie', 'tak'])
favorite_cmb.combobox.bind('<Button-1>', combo_events)

add_buttons_tab1()
# </editor-fold>


# <editor-fold desc="TAB 2 - INGREDIENTS">
# Create a Treeview Frame
tree_frame = Frame(tab2)
tree_frame.pack(pady=10)

my_tree_scroll = Scrollbar(tree_frame)
my_tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=my_tree_scroll.set, selectmode="extended")
my_tree.pack()

my_tree_scroll.config(command=my_tree.yview)
my_tree['columns'] = ("ID", "Składnik", "Ilość", "Jednostka")

# Format  Columns
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
description_entry.grid(row=1, column=0, padx=10, pady=10, ipady=60, ipadx=180)
description_entry.config(state='disabled')

edit_description_button = Button(description_frame, text="Edytuj Opis", command=lambda: edit_description())
edit_description_button.grid(row=1, column=1, padx=10, pady=10)
edit_description_button.config(height=2, width=10)

# Add Record Entry Boxes
data_frame = LabelFrame(tab2, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

conn = sqlite3.connect('przepisy.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

c.execute("SELECT nazwa FROM składniki")
list_of_ingredients = c.fetchall()

conn.commit()
conn.close()

ingredient_label = Label(data_frame, text="Składnik")
ingredient_label.grid(row=1, column=0, padx=5, pady=5)
ingredient_entry = AutocompleteCombobox(data_frame, completevalues=list_of_ingredients)
ingredient_entry.grid(row=1, column=1, padx=5, pady=5)

quantity = Entry_with_label(data_frame, set_row=1, set_column=2, name="Ilość")

conn = sqlite3.connect('przepisy.db')
c = conn.cursor()
c.execute('''SELECT nazwa FROM rodzaje_jednostek''')
units_options = c.fetchall()
conn.close()

unit = Combobox_with_Label(data_frame, set_row=1, set_column=4, current=3, name="Jednostka",
                           include_value=units_options)

add_buttons_tab2()
# </editor-fold>


# <editor-fold desc="TAB 3 - FRIDGE">

# Fridge FRAME
fridge_frame = Frame(tab3)
fridge_frame.pack(pady=10, fill=Y)

# <editor-fold desc="Treeview">
# Create a Treeview Scrollbar
tree_scroll3 = Scrollbar(fridge_frame)
tree_scroll3.pack(side=RIGHT, fill=Y)

fridge_tree = ttk.Treeview(fridge_frame, yscrollcommand=tree_scroll3.set, selectmode="extended")
fridge_tree.pack()

tree_scroll3.config(command=fridge_tree.yview)
fridge_tree['columns'] = ("ID", "Składnik")

# Format Columns

fridge_tree.column("#0", width=0, stretch=NO)
fridge_tree.column("ID", anchor=W, width=100)
fridge_tree.column("Składnik", anchor=W, width=500)

fridge_tree.heading("#0", text="", anchor=W)
fridge_tree.heading("ID", text="ID", anchor=CENTER)
fridge_tree.heading("Składnik", text="Składnik", anchor=CENTER)

# Create Striped Row Tags
fridge_tree.tag_configure('oddrow', background=saved_secondary_color)
fridge_tree.tag_configure('evenrow', background=saved_primary_color)

fridge_tree.bind('<Double 1>', double_open)
# </editor-fold>

# Add Record Entry Boxes
data_frame3 = LabelFrame(tab3, text="Record")
data_frame3.pack(fill="x", expand="yes", padx=20)

product_label = Label(data_frame3, text="Składnik")
product_label.grid(row=1, column=0, padx=5, pady=5)
product_entry = AutocompleteCombobox(data_frame3, completevalues=list_of_ingredients)
product_entry.grid(row=1, column=1, padx=5, pady=5)

add_buttons_tab3()

# </editor-fold>


query_database(1)
query_database(3)

root.mainloop()
