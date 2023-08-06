import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk


# Establishing a connection to the database
db = mysql.connector.connect(user='root', password='yourpassword',
                                host='127.0.0.1')

# Creating a cursor object to interact with the database
cursor = db.cursor()


def add_student():
    name = name_var.get()
    studentId=id_var.get()
    age = age_var.get()
    gender = gender_var.get()
    mail = email_Var.get()
    contact = contact_var.get()

    if name and studentId and age and gender and mail and contact:
        
        cursor.execute(f"SELECT * FROM STUDENT WHERE studentId = \"{studentId}\"")
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"INSERT INTO student VALUES(\"{name}\",\"{studentId}\",{age},\"{gender}\",\"{mail}\",\"{contact}\")")
            db.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            clear_entries()
        else:
            messagebox.showinfo("unSuccess", "Student is Already Exist")
            clear_entries()
            
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
    
    



def delete_student():
    student_id = id_var.get()

    if student_id:
        cursor.execute(f"SELECT * FROM STUDENT WHERE studentId = \"{student_id}\"")
        result = cursor.fetchone()

        if result is None:
            messagebox.showinfo("unSuccess", "Student Not Found")
            clear_entries()
        else:
            cursor.execute(f"DELETE FROM STUDENT WHERE studentId = \"{student_id}\"")
            db.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            clear_entries()
            db.commit()

    else:
        messagebox.showerror("Error", "Please enter the student ID.")



def search_student():
    student_id = id_var.get()

    if student_id:
        cursor.execute(f"SELECT * FROM STUDENT WHERE studentId={student_id}")
        student = cursor.fetchone()
        
        if student:
            messagebox.showinfo("Student Information", f"Student ID: {student[0]}\nName: {student[1]}\nAge: {student[2]}\nGender: {student[3]}\nEmail-Id: {student[4]}\nContact: {student[5]}")
        else:
            messagebox.showinfo("Student Information", "No student found with this ID!")

        id_var.set("")
    else:
        messagebox.showerror("Error", "Please enter a valid Student ID!")
        return
        





def clear_show_all_students():
    for widget in show_all_frame.winfo_children():
        widget.destroy()

def show_all_students():
    clear_show_all_students()  
    cursor.execute("SELECT * FROM STUDENT")
    results = cursor.fetchall()

    if results:
        show_all_frame.config(highlightbackground="black",highlightthickness=3)
        treeview = ttk.Treeview(show_all_frame, height=500, columns=("Student ID", "Name", "Email Id", "Age", "Gender", "Contact"), show="headings" )
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        treeview.heading("Student ID", text="Student ID", anchor=tk.CENTER)
        treeview.heading("Name", text="Name", anchor=tk.CENTER)
        treeview.heading("Email Id", text="Email Id", anchor=tk.CENTER)
        treeview.heading("Age", text="Age", anchor=tk.CENTER)
        treeview.heading("Gender", text="Gender", anchor=tk.CENTER)
        treeview.heading("Contact", text="Contact", anchor=tk.CENTER)

        treeview.column("#0", anchor=tk.CENTER)
        treeview.column("Student ID", anchor=tk.CENTER)
        treeview.column("Name", anchor=tk.CENTER)
        treeview.column("Email Id", anchor=tk.CENTER)
        treeview.column("Age", anchor=tk.CENTER)
        treeview.column("Gender", anchor=tk.CENTER)
        treeview.column("Contact", anchor=tk.CENTER)

        for student in results:
            treeview.insert("", tk.END, values=(student[1], student[0], student[4], student[2], student[3], student[5]))

        scrollbar = tk.Scrollbar(show_all_frame, command=treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        treeview.config(yscrollcommand=scrollbar.set)
    else:
        messagebox.showinfo("All Students", "No students found!")


def fetch_student_for_update():
    student_id = update_id_var.get()

    if student_id!=0 or student_id!="":
        cursor.execute(f"SELECT * FROM STUDENT WHERE studentId = {student_id}")
        student = cursor.fetchone()

        if student:
            update_name_var.set(student[0])
            update_age_var.set(student[2])
            update_gender_var.set(student[3])
            update_email_Var.set(student[4])
            update_contact_var.set(student[5])
            enable_update()
        else:
            messagebox.showinfo("Unsuccessful", "Student Not Found")
            clear_update_entries()
            update_btn.config(state="disabled")  
    else:
        messagebox.showerror("Error", "Please enter the student ID.")

def update_student():
    student_id = update_id_var.get()
    name = update_name_var.get()
    age = update_age_var.get()
    gender = update_gender_var.get()
    mail = update_email_Var.get()
    contact = update_contact_var.get()

    if student_id:
        if name and age and gender and mail and contact:
            cursor.execute("UPDATE STUDENT SET name=%s, age=%s, gender=%s, emailId=%s, contactnumber=%s WHERE studentId = %s",
                           (name, age, gender, mail, contact, student_id))
            db.commit()
            messagebox.showinfo("Success", "Student details updated successfully!")
            clear_update_entries()
            update_btn.config(state="disabled") 
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please enter the student ID.")
    

def clear_update_entries():
    update_id_var.set(0)
    update_name_var.set("")
    update_age_var.set("")
    update_gender_var.set("")
    update_email_Var.set("")
    update_contact_var.set("")
    
def disble_update():
    update_name_entry.config(state="disabled")
    update_age_entry.config(state="disabled")
    update_gender_entry.config(state="disabled")
    update_email_entry.config(state="disabled")
    update_contact_entry.config(state="disabled")
    update_btn.config(state="disabled")
    
def enable_update():
    update_id_entry.config(state="normal")
    update_name_entry.config(state="normal")
    update_age_entry.config(state="normal")
    update_gender_entry.config(state="normal")
    update_email_entry.config(state="normal")
    update_contact_entry.config(state="normal")
    update_btn.config(state="normal")
    

def reset_update_frame():
    clear_update_entries()
    update_frame.grid_forget()

def clear_search_frame():
    for widget in search_frame.winfo_children():
        widget.destroy()

def clear_entries():
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    email_Var.set("")
    contact_var.set("")
    id_var.set("")



def on_option_change(event):
    selected_option = option_var.get()
    if selected_option=="Select":
        pass
    elif selected_option == "Add Student":
        disble_update()
        reset_all_student()
        reset_search_frame()
        reset_update_frame()  
        add_frame.grid(row=2, column=0, columnspan=2)
        delete_frame.grid_forget()
        search_frame.grid_forget()
        show_all_frame.grid_forget()
    elif selected_option == "Delete Student":
        disble_update()
        reset_all_student()
        reset_search_frame()
        reset_update_frame()  
        add_frame.grid_forget()
        delete_frame.grid(row=2, column=0, columnspan=2)
        search_frame.grid_forget()
        show_all_frame.grid_forget()
    elif selected_option == "Search Student":
        disble_update()
        reset_all_student()
        reset_search_frame()
        reset_update_frame()  
        add_frame.grid_forget()
        delete_frame.grid_forget()
        search_frame.grid(row=2, column=0, columnspan=2)
        show_all_frame.grid_forget()
    elif selected_option == "All Students":
        disble_update()
        reset_search_frame()
        reset_update_frame() 
        add_frame.grid_forget()
        search_frame.grid_forget()
        show_all_frame.grid(row=2, column=0, columnspan=2)
        show_all_students()
    elif selected_option == "Update Student":
        reset_all_student()
        reset_search_frame()
        add_frame.grid_forget()
        delete_frame.grid_forget()
        search_frame.grid_forget()
        show_all_frame.grid_forget()
        update_frame.grid(row=2, column=0, columnspan=2)
        
        
def reset_update_frame():
    clear_update_entries()
    update_frame.grid_forget()

def clear_search_frame():
    for widget in search_frame.winfo_children():
        widget.destroy()
        
def reset_search_frame():
    clear_search_frame()
    search_frame.grid(row=10, column=0, columnspan=5, padx=10, pady=10)
    search_frame.grid_forget()
    tk.Label(search_frame, text="Student ID:", font=("Helvetica", 14), bg="skyblue").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(search_frame, textvariable=id_var, font=("Helvetica", 14),width=50).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(search_frame, text="Search Student", font=("Helvetica", 14), command=search_student).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
     
def reset_all_student():
    for widget in show_all_frame.winfo_children():
        widget.destroy()
    show_all_frame.grid_forget()
    
    
# START
if __name__ == "__main__":
    
    cursor.execute("USE college")
    root = tk.Tk()
    root.grid_rowconfigure(1, minsize=10)
    root.geometry("600x500")
    root.configure(bg="skyblue")
    root.title("Student Information Management System")


    option_var = tk.StringVar()
    option_var.set("Select")


    name_var = tk.StringVar()
    age_var = tk.IntVar()
    gender_var = tk.StringVar()
    email_Var = tk.StringVar()
    contact_var = tk.StringVar()
    id_var = tk.IntVar()

    
# Add Student Frame
    add_frame = tk.Frame(root, bg="skyblue",highlightbackground="black",highlightthickness=3)
    add_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    add_frame.grid_forget()

    # Labels
    tk.Label(add_frame, text="Name:", font=("Helvetica", 14), bg="skyblue").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(add_frame, text="Student ID:", font=("Helvetica", 14), bg="skyblue").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(add_frame, text="Age:", font=("Helvetica", 14), bg="skyblue").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(add_frame, text="Gender:", font=("Helvetica", 14), bg="skyblue").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(add_frame, text="Email Id:", font=("Helvetica", 14), bg="skyblue").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(add_frame, text="Contact:", font=("Helvetica", 14), bg="skyblue").grid(row=5, column=0, padx=5, pady=5)

    # Entry fields
    tk.Entry(add_frame, textvariable=name_var, font=("Helvetica", 14),width=50).grid(row=0, column=1, padx=5, pady=5)
    tk.Entry(add_frame, textvariable=id_var, font=("Helvetica", 14),width=50).grid(row=1, column=1, padx=5, pady=5)
    tk.Entry(add_frame, textvariable=age_var, font=("Helvetica", 14),width=50).grid(row=2, column=1, padx=5, pady=5)
    tk.Entry(add_frame, textvariable=gender_var, font=("Helvetica", 14),width=50).grid(row=3, column=1, padx=5, pady=5)
    tk.Entry(add_frame, textvariable=email_Var, font=("Helvetica", 14),width=50).grid(row=4, column=1, padx=5, pady=5)
    tk.Entry(add_frame, textvariable=contact_var, font=("Helvetica", 14),width=50).grid(row=5, column=1, padx=5, pady=5)

    # Buttons
    tk.Button(add_frame, text="Add Student", font=("Helvetica", 14), command=add_student).grid(row=6, column=0, columnspan=2, padx=5, pady=5)


# Delete Student Frame
    delete_frame = tk.Frame(root, bg="skyblue",highlightbackground="black",highlightthickness=3)
    delete_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    delete_frame.grid_forget()

    # Labels
    tk.Label(delete_frame, text="Student ID:", font=("Helvetica", 14), bg="skyblue").grid(row=0, column=0, padx=5, pady=5)

    # Entry fields
    tk.Entry(delete_frame, textvariable=id_var, font=("Helvetica", 14),width=50).grid(row=0, column=1, padx=5, pady=5)

    # Buttons
    tk.Button(delete_frame, text="Delete Student", font=("Helvetica", 14), command=delete_student).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Show All Student Frame
    search_frame = tk.Frame(root, bg="skyblue",height=700,highlightbackground="black",highlightthickness=3)
    search_frame.grid(row=10, column=10, columnspan=5, padx=5, pady=5)
    search_frame.grid_forget()

    # Labels
    tk.Label(search_frame, text="Student ID:", font=("Helvetica", 14), bg="skyblue").grid(row=0, column=0, padx=5, pady=5)

    # Entry fields
    tk.Entry(search_frame, textvariable=id_var, font=("Helvetica", 14),width=50).grid(row=0, column=0, padx=5, pady=5)

    # Buttons
    tk.Button(search_frame, text="Search Student", font=("Helvetica", 14), command=search_student).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    show_all_frame = tk.Frame(root, bg="skyblue")
    show_all_frame.grid(row=2, column=0, columnspan=5, padx=5, pady=5)
    show_all_frame.grid_forget()
    
    
# Update Student Frame
    update_frame = tk.Frame(root, bg="skyblue",highlightbackground="black",highlightthickness=3)
    update_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    update_frame.grid_forget()
    update_id_var = tk.IntVar()
    update_name_var = tk.StringVar()
    update_age_var = tk.IntVar()
    update_gender_var = tk.StringVar()
    update_email_Var = tk.StringVar()
    update_contact_var = tk.StringVar()

    # Labels
    tk.Label(update_frame, text="Student ID:", font=("Helvetica", 14), bg="skyblue").grid(row=0, column=0, padx=5, pady=5)

    # Entry fields
    update_id_entry = tk.Entry(update_frame, textvariable=update_id_var, font=("Helvetica", 14),width=50)
    update_id_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to search for a student for update
    search_btn = tk.Button(update_frame, text="Search Student", font=("Helvetica", 14), command=fetch_student_for_update)
    search_btn.grid(row=0, column=2, padx=5, pady=5)


    # Labels for student details
    tk.Label(update_frame, text="Name:", font=("Helvetica", 14), bg="skyblue").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(update_frame, text="Age:", font=("Helvetica", 14), bg="skyblue").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(update_frame, text="Gender:", font=("Helvetica", 14), bg="skyblue").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(update_frame, text="Email Id:", font=("Helvetica", 14), bg="skyblue").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(update_frame, text="Contact:", font=("Helvetica", 14), bg="skyblue").grid(row=5, column=0, padx=5, pady=5)

    # Entry fields for student details
    update_name_entry = tk.Entry(update_frame, textvariable=update_name_var, font=("Helvetica", 14),width=50, state="disabled")
    update_name_entry.grid(row=1, column=1, padx=5, pady=5)
    update_age_entry = tk.Entry(update_frame, textvariable=update_age_var, font=("Helvetica", 14),width=50, state="disabled")
    update_age_entry.grid(row=2, column=1, padx=5, pady=5)
    update_gender_entry = tk.Entry(update_frame, textvariable=update_gender_var, font=("Helvetica", 14),width=50, state="disabled")
    update_gender_entry.grid(row=3, column=1, padx=5, pady=5)
    update_email_entry = tk.Entry(update_frame, textvariable=update_email_Var, font=("Helvetica", 14),width=50, state="disabled")
    update_email_entry.grid(row=4, column=1, padx=5, pady=5)
    update_contact_entry = tk.Entry(update_frame, textvariable=update_contact_var, font=("Helvetica", 14),width=50, state="disabled")
    update_contact_entry.grid(row=5, column=1, padx=5, pady=5)

    # Update Button
    update_btn = tk.Button(update_frame, text="Update Student", font=("Helvetica", 14), command=update_student, state="disabled")
    update_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


    # Entry fields
    root.grid_rowconfigure(0, weight=0)  # Center row
    root.grid_columnconfigure(0, weight=1)  # Center column

    # Dropdown menu for choosing Add, Delete, Search, or Show All Students
    option_menu = tk.OptionMenu(root, option_var, "Select","Add Student", "Delete Student", "Search Student", "Update Student", "All Students", command=on_option_change)
    option_menu.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ns")
    # n, e, s, and/or w
    
root.mainloop()

