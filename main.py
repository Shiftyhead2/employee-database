from tkinter import *
from tkinter import messagebox
from typing import Any
from pages.mainHeader import MainHeader
from pages.userFormHeader import UserFormHeader
from pages.userForm import UserForm
import sqlite3
import os
import shutil


IMAGES_FOLDER:str = "images"
IMAGES_EXTENSION:str= "jpg"
DATABASES_FOLDER:str = "databases"
USERS_DATABASE:str = "employees.db"



class App:
  def __init__(self,root:Tk):
    self.root:Tk = root

    self.db_user_path:str = os.path.join(DATABASES_FOLDER,USERS_DATABASE)
    self.create_user_table()

    self.user_id:int = 0

    self.pages:dict[str,Any] = {
      "MainHeader": MainHeader(self.root,self),
      "UserFormHeader":UserFormHeader(self.root,self),
      "UserForm":UserForm(self.root,self)
    }

    self.current_pages:list[Any] = []

    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=1)

    self.switch_to_users_view()


  

  def switch_to_page(self,*page_names: str) -> None:
    pages:list[Any] = [self.pages.get(page_name) for page_name in page_names]

    if all(pages):
      for page in self.current_pages:
        page.hide()
      self.current_pages = pages

      for page in self.current_pages:
        page.show(self.user_id)
    else:
      messagebox.showerror("Error", f"One or more pages could not be found: {page_names}")
  
  def switch_to_users_view(self) -> None:
    self.switch_to_page("MainHeader")
    self.user_id = 0
  
  def switch_to_user_form(self) -> None:
    self.switch_to_page("UserFormHeader","UserForm")

  def create_user_table(self) -> None:
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
                trajanjeUgovora INT,
                odjel TEXT,
                daniGodišnjegOdmora INT,
                slobodniDani INT,
                danPlaćenogDopusta INT         
            )  
        ''')
    
    conn.commit()
    conn.close()
  
  def create_or_update_user(self,first_name: str,last_name: str ,picture_path: str,gender: str,birth_year: str,start_date :str ,contract_type :str,contract_duration:str,holiday_days:str,free_days:str,paid_leave:str,department:str) -> None:
    if not first_name or not last_name or not picture_path or not gender or not birth_year or not start_date or not contract_type or not contract_duration or not holiday_days or not free_days or not paid_leave or not department:
      messagebox.showerror("Dodavanje korisnika nije uspjelo!", "Molimo Vas da unesete sve podatke!")
      return
    
    if first_name.isalpha() == False or last_name.isalpha() == False:
      messagebox.showerror("Dodavanje korisnika nije uspjelo!", "Molimo Vas da točno unesete ime i prezime!")
      return
    
    try:
      int(birth_year)
      int(contract_duration)
      int(holiday_days)
      int(free_days)
      int(paid_leave)
    except ValueError:
      messagebox.showerror("Dodavanje korisnika nije uspjelo!", "Molimo Vas da provjerite sve podatke!")
      return
    

    conn = sqlite3.connect(self.db_user_path)
    cursor = conn.cursor()

    try:
      cursor.execute('''
                    INSERT INTO employees(ime,prezime,slika,spol,godinaRođenja,početakRada,vrstaUgovora,trajanjeUgovora,odjel,daniGodišnjegOdmora,slobodniDani,danPlaćenogDopusta)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', (first_name,last_name,self.save_image_locally(picture_path,first_name,last_name),gender,int(birth_year),start_date,contract_type,int(contract_duration),department,int(holiday_days),int(free_days),int(paid_leave)))
    except sqlite3.Error as e:
      messagebox.showerror("Greška!", f"Nešto je pošlo po zlu:{e}")
      return
    else:
      messagebox.showinfo("Uspjeh!", "Uspješno ste dodali zaposlenika!")
    
    conn.commit()
    conn.close()

    self.switch_to_users_view()
    
  

  def save_image_locally(self, picture:str, first_name:str,last_name:str) -> str:
      filename:str = f"{first_name}-{last_name}.{IMAGES_EXTENSION}"  

      file_path:str = os.path.join(IMAGES_FOLDER, filename)

      try:
          shutil.copy2(picture, file_path)
      except shutil.SameFileError:
          print("Files are the same")
          pass

      return file_path

  




def main() -> None:
  root:Tk = Tk()
  root.title("Employee Database")
  root.geometry("1280x720")

  App(root)

  root.mainloop()


if __name__ == "__main__":
  os.makedirs(DATABASES_FOLDER,exist_ok=True)
  os.makedirs(IMAGES_FOLDER,exist_ok=True)

  main()