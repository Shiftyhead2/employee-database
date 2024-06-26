from tkinter import Tk
from typing import Any
from pages.mainHeader import MainHeader
from pages.employeeHeader import EmployeeHeader
from pages.employeeForm import EmployeeForm
from pages.employeesView import EmployeesView
from pages.employeeView import EmployeeView
from helpers.helpersFunctions import *
from handlers.messageHandler import *
import sqlite3
import os
import shutil

class App:
  def __init__(self,root:Tk, images_folder:str,images_extension:str,databases_folder:str,employees_database):
    self.root:Tk = root

    self.images_folder:str = images_folder
    self.images_extension:str = images_extension
    self.database_folder:str = databases_folder
    self.employees_database:str = employees_database

    self.db_employee_path:str = os.path.join(self.database_folder,self.employees_database)
    self.create_employee_table()

    self.employee_id:int = 0

    self.pages:dict[str,Any] = {
      "MainHeader": MainHeader(self.root,self),
      "EmployeeHeader": EmployeeHeader(self.root,self),
      "EmployeeForm": EmployeeForm(self.root,self),
      "EmployeesView": EmployeesView(self.root,self),
      "EmployeeView": EmployeeView(self.root,self),
    }

    self.current_pages:list[Any] = []

    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_rowconfigure(0, weight=1)

    self.switch_to_employees_view()


  

  def switch_to_page(self,*page_names: str) -> None:
    pages:list[Any] = [self.pages.get(page_name) for page_name in page_names]

    if all(pages):
      for page in self.current_pages:
        page.hide()
      self.current_pages = pages

      for page in self.current_pages:
        page.show(self.employee_id)
    else:
      display_error_message("Greška!",f"Jedna ili više stranica nisu se mogle naći:{page_names}")
  
  def switch_to_employees_view(self) -> None:
    self.employee_id = 0
    self.switch_to_page("MainHeader", "EmployeesView")
    
  
  def switch_to_employee_form(self) -> None:
    self.pages["EmployeeHeader"].is_form = True
    self.switch_to_page("EmployeeHeader","EmployeeForm")
    
  
  def switch_to_employee_view(self) -> None:
    self.pages["EmployeeHeader"].is_form = False
    self.switch_to_page("EmployeeView","EmployeeHeader")
    

  def create_employee_table(self) -> None:
     with sqlite3.connect(self.db_employee_path) as conn:
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
          conn.commit()  
  
  def create_or_update_employee(self,first_name: str,last_name: str ,picture_path: str,gender: str,birth_year: str,start_date :str ,contract_type :str,contract_duration:str,holiday_days:str,free_days:str,paid_leave:str,department:str) -> None:
    if not checkIfNotEmpty(first_name,last_name,picture_path,gender,birth_year,start_date,contract_type,contract_duration,holiday_days,free_days,paid_leave,department):
      display_error_message("Dodavanje korisnika nije uspjelo!","Molimo Vas da unesete sve podatke!")
      return
    
    if not checkIfNoNumbers(first_name,last_name):
      display_error_message("Dodavanje korisnika nije uspjelo!", "Molimo Vas da točno unesete ime i prezime!")
      return
    
    if not checkIfInt(birth_year,contract_duration,holiday_days,free_days,paid_leave):
      display_error_message("Dodavanje korisnika nije uspjelo!", "Molimo Vas da provjerite sve podatke!")
      return
    
    
    with sqlite3.connect(self.db_employee_path) as conn:
      cursor = conn.cursor()
      if self.employee_id is None or self.employee_id == 0:
        try:
          cursor.execute('''
                    INSERT INTO employees(ime,prezime,slika,spol,godinaRođenja,početakRada,vrstaUgovora,trajanjeUgovora,odjel,daniGodišnjegOdmora,slobodniDani,danPlaćenogDopusta)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', (first_name,last_name,self.save_image_locally(picture_path,first_name,last_name),gender,int(birth_year),start_date,contract_type,int(contract_duration),department,int(holiday_days),int(free_days),int(paid_leave)))
        except sqlite3.Error as e:
          display_error_message("Greška!", f"Nešto je pošlo po zlu:{e}")
          return
        else:
          display_info_message("Uspjeh!", "Uspješno ste dodali zaposlenika!")
          conn.commit()
      else:
        try:
          cursor.execute('''
                    UPDATE employees SET ime=?,prezime=?,slika=?,spol=?,godinaRođenja=?,početakRada=?,vrstaUgovora=?,trajanjeUgovora=?,odjel=?,daniGodišnjegOdmora=?,slobodniDani=?,danPlaćenogDopusta=? WHERE id=?
                    ''', (first_name,last_name,self.save_image_locally(picture_path,first_name,last_name),gender,int(birth_year),start_date,contract_type,int(contract_duration),department,int(holiday_days),int(free_days),int(paid_leave),self.employee_id))
        except sqlite3.Error as e:
          display_error_message("Greška!", f"Nešto je pošlo po zlu:{e}")
          return
        else:
          display_info_message("Uspjeh!", "Uspješno ste ažurirali zaposlenika!")
          conn.commit()
        
    
    self.switch_to_employees_view()
    
  

  def save_image_locally(self, picture:str, first_name:str,last_name:str) -> str:
      filename:str = f"{first_name}-{last_name}.{self.images_extension}"  

      file_path:str = os.path.join(self.images_folder, filename)

      try:
          shutil.copy2(picture, file_path)
      except shutil.SameFileError:
          pass

      return file_path