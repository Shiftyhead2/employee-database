from tkinter import Label,Frame,Button
from handlers.messageHandler import display_error_message
from PIL import Image,ImageTk
import sqlite3

class EmployeeView(Frame):
  def __init__(self,master,controller):
    super().__init__(master)

    self.master = master
    self.controller = controller

    self.employee_id:int = 0
    self.employee = None

    self.name_label = Label(self, text= "Ime i prezime")
    self.employee_picture = Label(self, text= "Slika")
    self.gender_label = Label(self, text="Spol")
    self.birth_year_label = Label(self,text="Godina rođenja")
    self.start_date_label = Label(self,text="Početak rada")
    self.contract_type_label = Label(self,text="Vrsta ugovora")
    self.contract_duration_label = Label(self,text="Duljina ugovora")
    self.department_label = Label(self,text="Odjel")
    self.holiday_days_label = Label(self,text="Broj dana godišnjeg odmora")
    self.free_days_label = Label(self,text="Broj slobodnih dana")
    self.paid_leave_label = Label(self,text="Broj dana plaćenog dopusta")
    self.update_data_button = Button(self,text = "Ažuriraj podatke zaposlenika", command= self.update_employee)

    self.pack_widgets()  

    

    
  
  def show(self,employee_id:int = 0) -> None:
    self.master.update_idletasks()
    self.place(relx=0.5, rely=0.5,anchor="center")

    self.employee_id = employee_id
    self.get_employee()
  

  def pack_widgets(self):
    self.name_label.grid(row=0, column=1, sticky="W")
    self.employee_picture.grid(row=0, column=0, rowspan=11, sticky="W")  
    self.gender_label.grid(row=2, column=1, sticky="W")
    self.birth_year_label.grid(row=3, column=1, sticky="W")
    self.start_date_label.grid(row=4, column=1, sticky="W")
    self.contract_type_label.grid(row=5, column=1, sticky="W")
    self.contract_duration_label.grid(row=6, column=1, sticky="W")
    self.department_label.grid(row=7, column=1, sticky="W")
    self.holiday_days_label.grid(row=8, column=1, sticky="W")
    self.free_days_label.grid(row=9, column=1, sticky="W")
    self.paid_leave_label.grid(row=10, column=1, sticky="W")
    self.update_data_button.grid(row=11, column=1, sticky="W") 



  def hide(self) -> None:
    self.place_forget()
  
  def get_employee(self) -> None:
    with sqlite3.connect(self.controller.db_employee_path) as conn:
      cursor = conn.cursor()

      try:
        cursor.execute("SELECT * FROM employees WHERE id=?",(self.employee_id,))
      except sqlite3.Error as e:
        display_error_message("Greška!", f"Nešto je otišlo po zlu: {e}")
        return
      else:
        self.employee = cursor.fetchone()

        if not self.employee:
          display_error_message("Greška!", "Zaposlenik nije pronađen")
          return

        self.name_label.configure(text=f"Ime i prezime: {self.employee[1]} {self.employee[2]}")
        self.gender_label.configure(text=f"Spol: {self.employee[4]}")
        self.birth_year_label.configure(text=f"Godina rođenja: {self.employee[5]}")
        self.start_date_label.configure(text=f"Početak rada: {self.employee[6]}")
        self.contract_type_label.configure(text=f"Vrsta ugovora: {self.employee[7]}")
        self.contract_duration_label.configure(text=f"Duljina ugovora: {self.employee[8]} mjeseci")
        self.department_label.configure(text=f"Odjel: {self.employee[9]}")
        self.holiday_days_label.configure(text=f"Broj dana godišnjeg odmora: {self.employee[10]}")
        self.free_days_label.configure(text=f"Broj slobodnih dana: {self.employee[11]}")
        self.paid_leave_label.configure(text=f"Broj dana plaćenog dopusta: {self.employee[12]}")


        image_path = self.employee[3]
        try:
          image = Image.open(image_path)
          image.verify()
          image = Image.open(image_path)
        except FileNotFoundError as e:
          display_error_message("Greška!", f"Nismo mogli naći sliku na ovoj putanji {image_path}")
        except IOError as e:
          display_error_message("Greška!", f"Nismo mogli naći sliku na ovoj putanji {image_path}")
        except Exception as e:
          display_error_message("Greška!", f"Neočekivana greška: {e}")
        else:
          image = image.resize((150, 150))
          photo = ImageTk.PhotoImage(image)
          self.employee_picture.config(image=photo)
          self.employee_picture.image = photo  

        
  
  def update_employee(self) -> None:
    self.controller.employee_id = self.employee_id
    self.controller.switch_to_employee_form()