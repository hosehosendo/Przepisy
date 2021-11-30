import sqlite3
import pandas as pd
from sqlalchemy import create_engine

conn = sqlite3.connect('przepisy.db')
c = conn.cursor()


def create_tables():
    # stworzenie tabeli przepisow
    c.execute(
        '''CREATE TABLE if not exists przepisy(ID integer PRIMARY KEY, nazwa TEXT, kategoria TEXT, ulubione BIT)''')

    # stworzenie tabeli składnikow
    c.execute(
        '''CREATE TABLE if not exists składniki(ID INT, nazwa TEXT, kcal REAL, białka REAL, tłuszcze REAL, węglowodany REAL, rodzaj INT, na stanie NULL)''')

    # stworzenie tabeli rodzajow jednostek
    c.execute('''CREATE TABLE if not exists rodzaje_jednostek(ID INT, nazwa TEXT, skrót TEXT,	rodzaj TEXT)''')

    # stworzenie tabeli przepisow ze skladnikami i ich iloscia. jednostką i rodzajem jednostki many-to-many relation
    c.execute(
        '''CREATE TABLE if not exists przepis_z_składnikami(przepis INT,	składnik INT, ilość REAL, jednostka INT)''')

    # stworzenie tabeli z kategoriami przepisów
    c.execute('''CREATE TABLE if not exists kategorie(ID integer PRIMARY KEY, nazwa_kategorii TEXT)''')


def add_data():
    data = ["śniadanie", "obiad", "kolacja", "przekąska", "zupa", "deser", "wegetariańskie"]
    id_number = 1
    for record in data:
        c.execute("INSERT INTO kategorie VALUES (:ID, :nazwa_kategorii)",
                  {
                      'ID': id_number,
                      'nazwa_kategorii': record
                  }
                  )
        id_number += 1

    conn.commit()

def write_data_to_table():
    # Wczytanie do tabeli wartości z excela
    file = 'pliki/Lista produktow.xlsx'
    df = pd.read_excel(file, sheet_name='Produkty')
    #
    for i in range(0, len(df.index)):
        c.execute('''INSERT INTO składniki VALUES(?,?,?,?,?,?,?,?)''', (
        int(df.iat[i, 0]), df.iat[i, 1], int(df.iat[i, 2]), float(df.iat[i, 3]), float(df.iat[i, 4]),
        float(df.iat[i, 5]), df.iat[i, 6], 0))
        conn.commit()
        print(i)


def delete_values():
    # usuniecie wszystkich elementow z tabeli przez bialka
    c.execute('DELETE FROM kategorie WHERE ID>0')
    # c.execute('DELETE FROM przepis_z_składnikami WHERE składnik=0') #usuniecie z tabeli "wartosci" gdzie bialaka > 0
    conn.commit()


def delete_table():
    # usun tabele
    c.execute(('DROP TABLE kategorie'))
    conn.commit()


def show_values():
    # wyswietlenie wartosci
    c.execute('''SELECT nazwa FROM wartosci''')
    results = c.fetchall()
    print(results)


# delete_table()
# create_tables()
# add_data()
# write_data_to_table()
