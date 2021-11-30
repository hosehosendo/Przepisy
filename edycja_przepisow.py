import tkinter
import tkinter.messagebox
import pickle

class window:

    def __init__(self, root, what):

        self.root = root
        self.what = what

        # Create GUI
        frame_recipes = tkinter.Frame(self.root)
        frame_recipes.pack()

        self.listbox_recipes = tkinter.Listbox(frame_recipes, height=10, width=50)
        self.listbox_recipes.pack(side=tkinter.LEFT)

        scrollbar_recipes = tkinter.Scrollbar(frame_recipes)
        scrollbar_recipes.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.listbox_recipes.config(yscrollcommand=scrollbar_recipes.set)
        scrollbar_recipes.config(command=self.listbox_recipes.yview)

        self.entry_recipe = tkinter.Entry(self.root, width=50)
        self.entry_recipe.pack()

    def add_buttons(self):
        button_add_recipe = tkinter.Button(self.root, text="Dodaj " + str(self.what), width=48, command=self.add_recipe)
        button_add_recipe.pack()

        button_delete_recipe = tkinter.Button(self.root, text="Usuń " + str(self.what), width=48, command=self.delete_recipe)
        button_delete_recipe.pack()

        button_load_recipes = tkinter.Button(self.root, text="Załaduj " + str(self.what), width=48, command=self.load_recipes)
        button_load_recipes.pack()

        button_save_recipes = tkinter.Button(self.root, text="Zapisz " + str(self.what), width=48, command=self.save_recipes)
        button_save_recipes.pack()

    def add_recipe(self):
        recipe = self.entry_recipe.get()
        if recipe != "":
            self.listbox_recipes.insert(tkinter.END, recipe)
            self.entry_recipe.delete(0, tkinter.END)
        else:
            tkinter.messagebox.showwarning(title="Warning!", message="You must enter a recipe.")

    def delete_recipe(self):
        try:
            recipe_index = self.listbox_recipes.curselection()[0]
            self.listbox_recipes.delete(recipe_index)
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="You must select a recipe.")

    def load_recipes(self):
        try:
            recipes = pickle.load(open("recipes.dat", "rb"))
            self.listbox_recipes.delete(0, tkinter.END)
            for recipe in recipes:
                self.listbox_recipes.insert(tkinter.END, recipe)
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="Cannot find recipes.dat.")

    def save_recipes(self):
        recipes = self.listbox_recipes.get(0, self.listbox_recipes.size())
        pickle.dump(recipes, open("recipes.dat", "wb"))

class main_window(window):

    def add_buttons(self):
        super().add_buttons()

        button_open_recipes = tkinter.Button(self.root, text="Otwórz przepis", width=48, command=self.open_recipes)
        button_open_recipes.pack()

    def open_recipes(self):
        root2 = tkinter.Tk()
        root2.title("Składniki")
        okno_skladnikow = window(root2, "składnik")
        okno_skladnikow.add_buttons()


root1 = tkinter.Tk()
root1.title("Lista przepisów")

first_window = main_window(root1, "przepis")
first_window.add_buttons()

root1.mainloop()

