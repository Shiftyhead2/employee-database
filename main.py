from tkinter import *
from modules.app import App
import os

IMAGES_FOLDER:str = "images"
IMAGES_EXTENSION:str= "jpg"
DATABASES_FOLDER:str = "databases"
EMPLOYEES_DATABASE:str = "employees.db"

def main() -> None:
  root:Tk = Tk()
  root.title("Employee Database")
  root.geometry("1280x720")

  App(root,IMAGES_FOLDER,IMAGES_EXTENSION,DATABASES_FOLDER,EMPLOYEES_DATABASE)

  root.mainloop()


if __name__ == "__main__":
  os.makedirs(DATABASES_FOLDER,exist_ok=True)
  os.makedirs(IMAGES_FOLDER,exist_ok=True)

  main()