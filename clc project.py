from tkinter import *
import customtkinter
userdata_list = [] 
expense_list = [] 
income_list = []
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
app_width = 500
app_height = 500
Column = 2

task_var = customtkinter.StringVar()
income_var =  customtkinter.StringVar()
expense_var = customtkinter.StringVar()
income_description = customtkinter.StringVar()
expense_description = customtkinter.StringVar() 
username_var = customtkinter.StringVar()
name_var = customtkinter.StringVar()
age_var = customtkinter.StringVar()
password_var =  customtkinter.StringVar()
root.title('Develop Thy Self')
root.geometry(f'{app_width}x{app_height}')


def new_user_login():
    username = username_var.get()
    name = name_var.get()
    age = age_var.get()
    password = password_var.get()
    userdata_list.append([name, age, username, password]) 
    for item in root.winfo_children(): 
        item.destroy() 
    labelline = customtkinter.CTkLabel(root, text="Welcome " + name + " to Develop Thy Self")
    labelline.place(x=130, y=30)
    budget_planner = customtkinter.CTkButton(root, text="Budget Planner", command=user_budget)
    budget_planner.place(x=160, y=120)
    quit = customtkinter.CTkButton(root, text="Quit", command=root.destroy)
    quit.place(x=160, y=160)

def user_tasks():
  tm.open_task_manager(root)

def user_budget(): 
    global check
    for item in root.winfo_children(): 
        item.destroy()
    labelline = customtkinter.CTkLabel(root, text="Welcome to Budget Planner")
    labelline.place(x=150, y=30)
    labeltwo = customtkinter.CTkLabel(root, text="Please firstly enter your initial expenses and incomes down below")
    labeltwo.place(x=80, y=60)
    numbers = int(input("How many income entries would you like to add: "))
    for i in range(0, numbers): 
        income = int(input("Enter an income: ")) 
        entry_income = input("Where did it came from: ")
        income_list.append([income, entry_income])
        income_list.sort()
    print("")
    numbers = int(input("How many expenses entries would you like to add: "))
    for i in range(0, numbers): 
        expense = int(input("Enter an expense: ")) 
        entry_expense = input("What did you spend it on: ")
        expense_list.append([expense, entry_expense]) 
        expense_list.sort()
    check = int(input("What is your expense limit: ")) 
    print("")
    menu_orders() 

def menu_orders():
    while True: 
        print("Here is a list of functions")
        print("Type 1 - Add expenses and incomes")
        print("Type 2 - Remove an expense or income")
        print("Type 3 - List and print out all expenses and incomes")
        print("Type 4 - Update expenses or incomes ") 
        print("Type 5 - To end the program and leave")
        userinput = int(input("Please enter a number: ")) 
        if userinput == 1: 
            add_expenses_income()
        elif userinput == 2: 
            remove_expenses_income() 
        elif userinput == 3: 
            list_expenses_income() 
        elif userinput == 4:
            update_expenses_income()
        elif userinput == 5: 
            print("Thank you for using our program. See you soon!") 
        break 

def add_expenses_income(): 
  print("Would you like to add a expense or income entry?")
  add_entry = input("Press I for income or E for expense: ") 
  if add_entry == "I": 
    numbers = int(input("How many income entries would you like to add: ")) 
    for i in range(0, numbers): 
      income = int(input("Enter an income: ")) 
      entry_income = input("Where did it came from: ") 
      income_list.append([income, entry_income]) 
      income_list.sort() 
    print("")
  elif add_entry == "E": 
    numbers = int(input("How many expenses entries would you like to add: ")) 
    for i in range(0, numbers): 
      expense = int(input("Enter an expense: ")) 
      entry_expense = input("What did you spend it on: ")
      expense_list.append([expense, entry_expense]) 
      expense_list.sort() 
    print("")
  else: 
    print("Invalid input. Please try again") 
    print("")
  checker(check)
  menu_orders() 

def remove_expenses_income(): 
  counter = 0 
  print("Here is a list of all your expenses: ") 
  print("------------------------------------")
  for i in range(0, len(expense_list)): 
    print("#", counter, "-" , "$" +str(expense_list[i][0]), " - " , expense_list[i][1]) 
    counter += 1 
  print("------------------------------------")
  print("Here is a list of all your incomes: ")
  counter = 0 
  i = 0 
  for i in range(0, len(income_list)): 
    print("#", counter, "-" , "$" +str(income_list[i][0]), " - " , income_list[i][1]) 
    counter += 1
  print("------------------------------------")
  print("Would you like to remove a expense or income entry?")
  remove_entry = input("Press I for income or E for expense: ") 
  if remove_entry == "I": 
    remove_income_entry = int(input("Which entry would you like to remove: ")) 
    for i in range(0, len(income_list)): 
      if remove_income_entry == i: 
        income_list.pop(remove_income_entry) 
        print("This income entry has been removed") 
        if len(income_list) == 0: 
          print("There is no more income entry")
          print("Please add an income entry")
          add_expenses_income() 
        income_list.sort() 
        print("")
        print("This is the updated version: ")
        counter = 0 
        for i in range(0, len(income_list)): 
          print("#", counter, "-" , "$" +str(income_list[i][0]), " - " , income_list[i][1])
          counter += 1
          print("")
        break 
      elif remove_income_entry > len(income_list): 
        print("Invalid entry")
        break 
      elif remove_income_entry == len(income_list): 
        print("Invalid entry")
        break  
  elif remove_entry == "E": 
    remove_expense_entry = int(input("Which entry would you like to remove: ")) 
    for i in range(0, len(expense_list)): 
      if remove_expense_entry == i: 
        expense_list.pop(remove_expense_entry) 
        print("This expense entry has been removed")
        if len(expense_list) == 0: 
          print("There is no more expense entry")
          print("Please add an expense entry")
          add_expenses_income()
        expense_list.sort() 
        print("")
        print("This is the updated version: ")
        counter = 0 
        for i in range(0, len(expense_list)): 
          print("#", counter, "-" , "$" +str(expense_list[i][0]), " - " , expense_list[i][1])
          counter += 1
          print("")
        break  
      elif remove_expense_entry > len(expense_list): 
        print("Invalid entry")
        break 
      elif remove_expense_entry == len(expense_list): 
        print("Invalid entry") 
        break 
  else: 
    print("Invalid")   
  menu_orders() 

def update_expenses_income():
  counter = 0
  print("Here is a list of all your expenses: ")
  print("------------------------------------")
  for i in range(0, len(expense_list)): 
    print("#", counter, "-" , "$" +str(expense_list[i][0]), " - " , expense_list[i][1])
    counter += 1
  print("------------------------------------")
  print("Here is a list of all your incomes: ")
  counter = 0 
  for i in range(0, len(income_list)): 
    print("#", counter, "-" , "$" +str(income_list[i][0]), " - " , income_list[i][1]) 
    counter += 1
  print("------------------------------------")
  print("Would you like to update a expense or income entry")
  update = input("Press I for income or E for expense: ") 

  if update == "I": 
    update_income_entry = int(input("Which income entry would you like to update: ")) 
    for i in range(0, len(income_list)): 
      if update_income_entry == i: 
        update_income = int(input("How much would you like to update it to: ")) 
        income_list[i][0] = update_income 
        income_list.sort() 
        print("")
        print("This is the updated version: ")
        counter = 0 
        for i in range(0, len(income_list)): 
          print("#", counter, "-" , "$" +str(income_list[i][0]), " - " , income_list[i][1])
          counter += 1
          print("")
        break 
      elif update_income_entry > len(income_list): 
        print("Invalid entry")
        break
      elif update_income_entry == len(income_list): 
        print("Invalid entry") 
        break
  elif update == "E": 
    update_entry = int(input("Which expense entry would you like to update: "))
    for i in range(0, len(expense_list)): 
      if update_entry == i: 
        update_expense = int(input("How much would you like to update it to: "))
        expense_list[i][0] = update_expense  
        expense_list.sort() 
        print("")
        print("This is the updated version: ")
        counter = 0 
        for i in range(0, len(expense_list)): 
          print("#", counter, "-" , "$" +str(expense_list[i][0]), " - " , expense_list[i][1])
          counter += 1
          print("")
        break 
      elif update_entry > len(expense_list): 
        print("Invalid entry")
        break 
      elif update_entry == len(expense_list):  
        print("Invalid entry") 
        break 
  else: 
    print("Invalid")
  checker(check)
  menu_orders() 

def list_expenses_income():
  max = 0 
  sum = 0 
  counter = 0 
  print("")
  print("Here is a list of all your expenses: ")
  print("------------------------------------")
  for i in range(0, len(expense_list)): 
    print("#", counter, "-" , "$" +str(expense_list[i][0]), " - " , expense_list[i][1])
    counter += 1
    max = max + expense_list[i][0] 
  print("") 
  print("Here is a list of all your incomes: ")
  print("------------------------------------")
  counter = 0 
  for i in range(0, len(income_list)): 
    print("#", counter, "-" , "$" +str(income_list[i][0]), " - " , income_list[i][1]) 
    sum = sum + income_list[i][0] 
    counter += 1
  print("------------------------------------")
  print("The total amount of money you have spent is: ",  round(max, 2))
  print("The total amount of income: ",  round(sum, 2))
  print("This is the amount of money left: ", round(sum - max, 2)) 
  print("------------------------------------") 
  checker(check)
  menu_orders()  
    
def user_journal(): 
    print("J") 

def user_tasks():
    pass 

def checker(check): 
  max = 0 
  for i in range(0, len(expense_list)): 
    max = max + expense_list[i][0]
  if max >= check:
    print("")
    print("Warning!! Your expenses have gone over the limit")

#Main Program
startlabel = customtkinter.CTkLabel(root, text="User, please input your details")
startlabel.place(x=160, y=30)
nameLabel = customtkinter.CTkLabel(root, text="Name")
nameLabel.place(x=110, y=80)

nameEntry = customtkinter.CTkEntry(root, textvariable=name_var)
nameEntry.place(x=190, y=80)

ageLabel = customtkinter.CTkLabel(root, text="Age")
ageLabel.place(x=110,y=140 )

ageEntry = customtkinter.CTkEntry(root,textvariable=age_var)
ageEntry.place(x=190, y=140)

usernameLabel = customtkinter.CTkLabel(root, text="User Name")
usernameLabel.place(x=110, y=200)

usernameEntry = customtkinter.CTkEntry(root, textvariable=username_var)
usernameEntry.place(x=190, y=200)

passwordLabel = customtkinter.CTkLabel(root, text="Password")
passwordLabel.place(x=110, y=260)

passwordEntry = customtkinter.CTkEntry(root, textvariable=password_var, show="*")
passwordEntry.place(x=190, y=260)

login_button = customtkinter.CTkButton(root, text="Login", command=new_user_login)
login_button.place(x=160, y=320)

income = 0 
check = 0 
expense = 0 





root.mainloop()
