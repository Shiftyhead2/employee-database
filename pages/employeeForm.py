import tkinter as tk
from tkinter import Frame,Label,Entry,Button,ttk, filedialog,messagebox
from tkcalendar import *
import sqlite3

GENDER_OPTIONS:list[str] = ["Muško","Žensko"]
CONTRACT_TYPES:list[str] = ["Određeno","Neodređeno"]

class EmployeeForm(Frame):
  def __init__(self,master,controller):
    super().__init__(master)

    self.master = master
    self.controller = controller

    self.user_id:int = 0
    self.employee = None

    self.first_name_label = Label(self,text = "Ime:")
    self.first_name_entry = Entry(self,width=25)

    self.last_name_label = Label(self,text = "Prezime:")
    self.last_name_entry = Entry(self, width= 25)

    self.picture_label = Label(self,text = "Slika")
    self.picture_entry = Entry(self,width=25)
    self.browse_picture_button = Button(self,text = "Odaberi sliku", command= self.browse_picture)

    self.gender_label = Label(self,text = "Spol")
    self.gender_selection = ttk.Combobox(self,state="readonly",values= GENDER_OPTIONS)

    self.birth_year_label = Label(self,text = "Godina rođenja:")
    self.birth_year_entry = Entry(self,width= 25)
    
    self.start_date_label = Label(self,text = "Početak Rada:")
    self.start_date_entry = Entry(self,width= 25)
    self.start_date_button = Button(self,text = "Odaberi datum" , command= self.pick_date)

    self.contract_type_label = Label(self,text = "Vrsta ugovora:")
    self.contract_type_selection = ttk.Combobox(self,state="readonly",values= CONTRACT_TYPES)

    self.contract_duration_label = Label(self,text = "Trajanje ugovora:")
    self.contract_duration_entry = Entry(self, width= 25)

    self.department_label = Label(self,text = "Odjel:")
    self.department_entry = Entry(self,width=25)

    self.holiday_days_label = Label(self,text = "Broj dana godišnjeg odmora:")
    self.holiday_days_entry = Entry(self,width= 25)

    self.free_days_label = Label(self,text = "Broj slobodnih dana:")
    self.free_days_entry = Entry(self,width=25)

    self.paid_leave_label = Label(self,text="Broj plaćenog dopusta:")
    self.paid_leave_entry = Entry(self,width=25)

    self.submit_button = Button(self,text = "Napravi zaposlenika", command= self.submit_data)

    self.pack_widgets()



  def show(self,user_id: int = 0) -> None:
    self.master.update_idletasks()
    self.place(relx=0.5, rely=0.5,anchor="center")
    self.user_id = user_id
    self.update_UI_accordingly()

  def hide(self) -> None:
    self.place_forget()
  
  def pack_widgets(self) -> None:
    
    self.first_name_label.grid(row=0,column=0,sticky="N")
    self.first_name_entry.grid(row=1,column=0,sticky="N")

    self.last_name_label.grid(row=2,column=0,sticky="N")
    self.last_name_entry.grid(row=3,column=0,sticky="N")

    self.picture_label.grid(row=4,column=0,sticky="N")
    self.picture_entry.grid(row=5,column=0,sticky="N")
    self.browse_picture_button.grid(row=5,column=1,sticky="N")

    self.gender_label.grid(row=6,column=0,sticky="N")
    self.gender_selection.grid(row=7,column=0,sticky="N")

    self.birth_year_label.grid(row=8,column=0,sticky="N")
    self.birth_year_entry.grid(row=9,column=0,sticky="N")

    self.start_date_label.grid(row=10,column=0,sticky="N")
    self.start_date_entry.grid(row=11,column=0,sticky="N")
    self.start_date_button.grid(row=11, column=1 ,sticky= "N")


    self.contract_type_label.grid(row=12,column=0,sticky="N")
    self.contract_type_selection.grid(row=13,column=0,sticky="N")

    self.contract_duration_label.grid(row=14,column=0,sticky="N")
    self.contract_duration_entry.grid(row = 15,column= 0 ,sticky= "N")

    self.department_label.grid(row=16,column=0,sticky="N")
    self.department_entry.grid(row=17,column=0,sticky="N")

    self.holiday_days_label.grid(row = 18 , column= 0 , sticky= "N")
    self.holiday_days_entry.grid(row = 19, column= 0 , sticky= "N")

    self.free_days_label.grid(row=20,column=0,sticky="N")
    self.free_days_entry.grid(row=21,column=0,sticky="N")

    self.paid_leave_label.grid(row=22,column=0,sticky="N")
    self.paid_leave_entry.grid(row=23,column=0,sticky="N")

    self.submit_button.grid(row=24,column=0,sticky="N")
  
  def update_UI_accordingly(self) -> None:
    with sqlite3.connect(self.controller.db_user_path) as conn:
      cursor = conn.cursor()

      try:
        cursor.execute("SELECT * FROM employees WHERE id=?",(self.user_id,))
      except sqlite3.Error as e:
        messagebox.showerror("Greška!",f"Nešto je otišlo po zlu: {e}")
      else:
        self.employee = cursor.fetchone()
        self.first_name_entry.delete(0,'end')
        self.last_name_entry.delete(0,'end')
        self.picture_entry.delete(0,'end')
        self.gender_selection.set(GENDER_OPTIONS[0])
        self.birth_year_entry.delete(0,'end')
        self.start_date_entry.delete(0 , 'end')
        self.contract_type_selection.set(CONTRACT_TYPES[0])
        self.contract_duration_entry.delete(0,'end')
        self.department_entry.delete(0,'end')
        self.holiday_days_entry.delete(0,'end')
        self.free_days_entry.delete(0,'end')
        self.paid_leave_entry.delete(0,'end')
      finally:
        cursor.close()


  
  def pick_date(self) -> None:
    global date_window,cal
    date_window = tk.Toplevel(self)
    date_window.grab_set()
    date_window.title("Izaberi datum")
    date_window.geometry("250x220")

    cal = Calendar(date_window,selectmode = "day", date_pattern = "dd/mm/y")
    cal.place(x = 0, y = 0)

    submit_btn = Button(date_window, text = "Submit", command = self.grab_date)
    submit_btn.place(x = 80,y = 190)

  def grab_date(self) -> None:
    self.start_date_entry.delete(0,'end')
    self.start_date_entry.insert(0,cal.get_date())
    date_window.destroy()
  
  def browse_picture(self) -> None:
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
    self.picture_entry.delete(0,'end')
    self.picture_entry.insert(0,file_path)
  
  def submit_data(self) -> None:
    first_name:str = self.first_name_entry.get()
    last_name:str = self.last_name_entry.get()
    picture_path:str = self.picture_entry.get()
    gender:str = self.gender_selection.get()
    birth_year:str = self.birth_year_entry.get()
    start_date:str = self.start_date_entry.get()
    contract_type:str = self.contract_type_selection.get()
    contract_duration:str = self.contract_duration_entry.get()
    department:str = self.department_entry.get();
    holiday_days:str = self.holiday_days_entry.get()
    free_days:str = self.free_days_entry.get()
    paid_leave:str = self.paid_leave_entry.get()

    self.controller.create_or_update_user(first_name,last_name,picture_path,gender,birth_year,start_date,contract_type,contract_duration,holiday_days,free_days,paid_leave,department)
