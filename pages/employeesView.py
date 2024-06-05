from tkinter import Frame,Button
from handlers.messageHandler import display_error_message
import sqlite3

class EmployeesView(Frame):
  def __init__(self,master,controller):
    super().__init__(master)
    
    self.master = master
    self.controller = controller

    self.employee_buttons:list[Button] = []

    self.add_employee_button = Button(self,text="Dodaj novog zaposlenika", command=self.controller.switch_to_employee_form)
  

  def create_buttons(self):
    with sqlite3.connect(self.controller.db_employee_path) as conn:
      cursor = conn.cursor()
      try:
        cursor.execute('''SELECT id,ime,prezime FROM employees''')
      except sqlite3.Error as e:
        display_error_message("Greška!", f"Nešto je otišlo po zlu: {e}")
        return
      else:
        employees = cursor.fetchall()

        for button in self.employee_buttons:
          button.destroy()
        
        max_button_rows:int = 3
        num_buttons:int = len(employees)
        num_rows:int = (num_buttons + max_button_rows - 1) // max_button_rows

        for index,employee in enumerate(employees):
          row = index // max_button_rows + 1
          column = index % max_button_rows + 1

          button = Button(self, text= f"{employee[1]} {employee[2]}",command=lambda e=employee:self.show_employee_details(e[0]))
          button.configure(compound="left", padx=10)
          button.grid(row=row, column=column, padx=5, sticky="WE", pady=5)
          self.employee_buttons.append(button)
        self.add_employee_button.grid(row=num_rows + 1, columnspan=max_button_rows, column=1, sticky="WE",pady=10)
  
  def show_employee_details(self,employee_id:int):
    self.controller.employee_id = employee_id
    self.controller.switch_to_employee_view()
  

  def show(self,employee_id:int = 0):
    self.master.update_idletasks()
    self.place(relx=0.5, rely=0.5, anchor="center")
    self.create_buttons()

  def hide(self):
    self.place_forget()

