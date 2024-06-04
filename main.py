from tkinter import *
from tkinter import messagebox
from pages.mainHeader import MainHeader
from pages.userFormHeader import UserFormHeader
from pages.userForm import UserForm
import sqlite3
import os


IMAGES_FOLDER: str = "images"
IAMGES_EXTENSION: str= "jpg"
DATABASES_FOLDER: str = "databases"
USERS_DATABASE: str = "employees.db"



class App:
  def __init__(self,root):
    self.root = root

    self.db_user_path: str = os.path.join(DATABASES_FOLDER,USERS_DATABASE)
    self.create_user_table()

    self.user_id = 0

    self.pages = {
      "MainHeader": MainHeader(self.root,self),
      "UserFormHeader":UserFormHeader(self.root,self),
      "UserForm":UserForm(self.root,self)
    }

    self.current_pages = []

    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=1)

    self.switch_to_users_view()


  

  def switch_to_page(self,*page_names: str):
    pages = [self.pages.get(page_name) for page_name in page_names]

    if all(pages):
      for page in self.current_pages:
        page.hide()
      self.current_pages = pages

      for page in self.current_pages:
        page.show(self.user_id)
    else:
      messagebox.showerror("Error", f"One or more pages could not be found: {page_names}")
  
  def switch_to_users_view(self):
    self.switch_to_page("MainHeader")
    self.user_id = 0
  
  def switch_to_user_form(self):
    self.switch_to_page("UserFormHeader","UserForm")

  def create_user_table(self):
    conn = sqlite3.connect(self.db_user_path)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ime TEXT,
                prezime TEXT,
                slika TEXT,
                spol TEXT,
                godinaRođenja TEXT,
                početakRada TEXT,
                vrstaUgovora TEXT,
                trajanjeUgovora TEXT,
                odjel TEXT,
                daniGodišnjegOdmora INT,
                slobodniDani INT,
                danPlaćenogDopusta INT         
            )  
        ''')
    
    conn.commit()
    conn.close()

  




def main():
  root = Tk()
  root.title("Employee Database")
  root.geometry("1280x720")

  App(root)

  root.mainloop()


if __name__ == "__main__":
  os.makedirs(DATABASES_FOLDER,exist_ok=True)
  os.makedirs(IMAGES_FOLDER,exist_ok=True)

  main()