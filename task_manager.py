from tkinter import * 
from tkinter import messagebox
tasks_list = []
counter = 1 
root = Tk()
root.title('Develop Thy Self')
root.geometry(f'{500}x{500}')
root.configure(bg = "black")

def clear():
    taskNumberField.delete(0.0, END) 

def delete(): 
    global counter 
    if len(tasks_list) == 0: 
        messagebox.showerror(title="No Tasks", message="You need to add a task")
        return
    digit = taskNumberField.get(1.0, END)
    if digit == "\n":
        messagebox.showerror(title="Input Error", message="There is an error with your input message")
        return 
    else: 
        task_number = int(digit)
    clear() 
    tasks_list.pop(task_number - 1)
    counter -= 1
    TextArea.delete(1.0, END)
    for i in range(len(tasks_list)) :
        TextArea.insert('end -1 chars', str(i+1)+ ". " + tasks_list[i])


def Userinput_clear(): 
    Userinput.delete(0, END)

def Input_error(): 
    if Userinput.get() == "": 
        messagebox.showerror(title="Input Error", message="There is an error with your input message")
        return 0
    return 1

def submit():
    global counter 
    value = Input_error()
    if value == 0: 
        return 
    input = Userinput.get() + "\n"
    tasks_list.append(input)
    TextArea.insert('end -1 chars', str(counter)+ ". " + input)
    counter += 1 
    Userinput_clear()

WelcomeLabel = Label(root, text="Welcome to Task Manager")
WelcomeLabel.place(x=160, y=70)
Inputlabel = Label(root, text="Please input your tasks")
Inputlabel.place(x=170, y=100)
Userinput = Entry(root, text="")
Userinput.place(x=160, y=130)
TextArea = Text(root, height = 5, width = 25, font = "lucida 13")
TextArea.place(x=130, y=160)
taskNumber = Label(root, text = "Delete Task Number", bg = "white")
taskNumber.place(x=80, y=270)
taskNumberField = Text(root, height = 1, width = 2, font = "lucida 13")
taskNumberField.place(x=130, y=300)
submit_button = Button(root, text = "Submit", fg = "White", bg = "Black", command = submit)
submit_button.place(x=300, y=270)
delete_button = Button(root, text = "Delete", fg = "White", bg = "Black", command = delete)
delete_button.place(x=300, y=310)
Exit_button = Button(root, text="Exit", fg = "White", bg = "Black", command = root.destroy )
Exit_button.place(x=310, y=350)

root.mainloop()