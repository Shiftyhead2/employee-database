from tkinter import *
from typing import Any
from pages.mainHeader import MainHeader
from pages.employeeFormHeader import EmployeeFormHeader
from pages.employeeForm import EmployeeForm
from pages.employeesView import EmployeesView
from helpers.helpersFunctions import *
from handlers.messageHandler import *
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
      "UserFormHeader":EmployeeFormHeader(self.root,self),
      "UserForm":EmployeeForm(self.root,self),
      "EmployeesView": EmployeesView(self.root,self)
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
      display_error_message("Greška!",f"Jedna ili više stranica nisu se mogle naći:{page_names}")
  
  def switch_to_users_view(self) -> None:
    self.switch_to_page("MainHeader", "EmployeesView")
    self.user_id = 0
  
  def switch_to_user_form(self) -> None:
    self.switch_to_page("UserFormHeader","UserForm")

  def create_user_table(self) -> None:
     with sqlite3.connect(self.db_user_path) as conn:
          cursor = conn.cursor()
          cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ime TEXT,
                    prezime TEXT,
                    slika TEXT,
                    spol TEXT,
                    godinaRođenja INTEGER,
                    početakRada TEXT,
                    vrstaUgovora TEXT,
                    trajanjeUgovora INTEGER,
                    odjel TEXT,
                    daniGodišnjegOdmora INTEGER,
                    slobodniDani INTEGER,
                    danPlaćenogDopusta INTEGER         
                )
            ''')
          cursor.close()  
          conn.commit()  
  
  def create_or_update_user(self,first_name: str,last_name: str ,picture_path: str,gender: str,birth_year: str,start_date :str ,contract_type :str,contract_duration:str,holiday_days:str,free_days:str,paid_leave:str,department:str) -> None:
    if not checkIfNotEmpty(first_name,last_name,picture_path,gender,birth_year,start_date,contract_type,contract_duration,holiday_days,free_days,paid_leave,department):
      display_error_message("Dodavanje korisnika nije uspjelo!","Molimo Vas da unesete sve podatke!")
      return
    
    if not checkIfNoNumbers(first_name,last_name):
      display_error_message("Dodavanje korisnika nije uspjelo!", "Molimo Vas da točno unesete ime i prezime!")
      return
    
    if not checkIfInt(birth_year,contract_duration,holiday_days,free_days,paid_leave):
      display_error_message("Dodavanje korisnika nije uspjelo!", "Molimo Vas da točno unesete ime i prezime!")
      return
    
    with sqlite3.connect(self.db_user_path) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute('''
                    INSERT INTO employees(ime,prezime,slika,spol,godinaRođenja,početakRada,vrstaUgovora,trajanjeUgovora,odjel,daniGodišnjegOdmora,slobodniDani,danPlaćenogDopusta)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', (first_name,last_name,self.save_image_locally(picture_path,first_name,last_name),gender,int(birth_year),start_date,contract_type,int(contract_duration),department,int(holiday_days),int(free_days),int(paid_leave)))
      except sqlite3.Error as e:
        display_error_message("Greška!", f"Nešto je pošlo po zlu:{e}")
        cursor.close()
        return
      else:
        display_info_message("Uspjeh!", "Uspješno ste dodali zaposlenika!")
      finally:
        cursor.close()
        conn.commit()
    
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