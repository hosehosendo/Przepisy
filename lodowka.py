import sqlite3


def find_recipe():
    print("znajdź przepis")

    conn = sqlite3.connect('przepisy.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()

    c.execute('''SELECT produkt FROM lodówka''')
    fridge_list = c.fetchall()
    print(fridge_list)
    conn.commit()
    conn.close()




recipes_list = [(1,2,3,4), (2,3,4,5), (3,4,5, 6)]

print((recipes_list[0]))

fridge = [2,3,4]


#  Sprawdzanie czy lista zawiera listę
for i in range(len(recipes_list)):
    result = all(elem in recipes_list[i] for elem in fridge)
    if result:
        print(i)


# Sprawdzanie ile elementów listy jest w innej liście. Nie mogą się powtarzać numery
list1 = [ 3, 4, 7 ]
list2 = [ 5, 2, 3, 4, 9 ]

c =  len([i for i in list2 if i in list1 ])
c = sum(el in list1 for el in list2)

print(c)