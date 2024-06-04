from tkinter import Frame,Label,Button

class UserFormHeader(Frame):
  def __init__(self,master,controller):
    super().__init__(master)
    self.master = master
    self.controller = controller

    self.header_label = Label(self, bg = "lightgray", height= 2)
    self.title_label = Label(self,text = "Forma zaposlenika", bg= "lightgray")
    self.back_button = Button(self, text = "Natrag", command=self.controller.switch_to_users_view)

    self.pack_widgets()

  def pack_widgets(self) -> None:
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)

    self.header_label.grid(row=0, column=0, columnspan=5, sticky="NSEW")
    self.title_label.grid(row=0, column=1)
    self.back_button.grid(row = 0, column= 3 , sticky= "E" , padx=10)
  

  def show(self,user_id = 0) -> None:
    self.grid(sticky="NSEW")
  
  def hide(self) -> None:
    self.grid_remove()