def checkIfNotEmpty(*args:str) -> bool:
  for arg in args:
    if not arg:
      return False
  return True

def checkIfNoNumbers(*args:str) -> bool:
  for arg in args:
    if not arg.isalpha():
      return False
  return True

def checkIfInt(*args:str) -> bool:
  for arg in args:
    try:
      int(arg)
    except ValueError:
      return False
  return True