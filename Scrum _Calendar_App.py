import tkinter as tk 
import json 
import tkinter.messagebox
import datetime as dt


class signUpPage(tk.Tk):
    def _init_(self):
        super()._init_()
        self.geometry("400x800")
        self.title("Sign Up")
        
        
        
        self.resizable(False, False)

        self.username_label = tk.Label(self, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self, font=("Arial", 14))
        self.password_entry.pack(pady=5)
        
        self.tckno_label = tk.Label(self, text="TCKNO:", font=("Arial", 14))
        self.tckno_label.pack(pady=10)
        
        self.tckno_entry = tk.Entry(self, font=("Arial", 14))
        self.tckno_entry.pack(pady=5)
        
        self.name_label = tk.Label(self, text="Name:", font=("Arial", 14))
        self.name_label.pack(pady=10)
        
        self.name_entry = tk.Entry(self, font=("Arial", 14))
        self.name_entry.pack(pady=5)
        
        self.surname_label = tk.Label(self, text="Surname:", font=("Arial", 14))
        self.surname_label.pack(pady=10)
        
        self.surname_entry = tk.Entry(self, font=("Arial", 14))
        self.surname_entry.pack(pady=5)
        
        self.email_label = tk.Label(self, text="Email:", font=("Arial", 14))
        self.email_label.pack(pady=10)
        
        self.email_entry = tk.Entry(self, font=("Arial", 14))
        self.email_entry.pack(pady=5)
        
        self.phone_label = tk.Label(self, text="Phone:", font=("Arial", 14))
        self.phone_label.pack(pady=10)
        
        self.phone_entry = tk.Entry(self, font=("Arial", 14))
        self.phone_entry.pack(pady=5)
        
        self.address_label = tk.Label(self, text="Address:", font=("Arial", 14))
        self.address_label.pack(pady=10)

        self.address_entry = tk.Entry(self, font=("Arial", 14))
        self.address_entry.pack(pady=5)

        self.sign_up_button = tk.Button(self, text="Sign Up", command=self.sign_up)
        self.sign_up_button.pack(pady=5)

        self.sign_in_button = tk.Button(self, text="Sign In", command=self.sign_in)
        self.sign_in_button.pack(pady=5)

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        tckno = self.tckno_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        user_type = "user"
        

        if username and password:
            with open("users.json", "r") as file:
                users = json.load(file)

            if username in users:
                tk.messagebox.showerror("Username Exists", "Try a different username.")
            else:
                #chekc if the tckno is exist
                with open("users.json", "r") as file:
                    users = json.load(file)
                for user in users:
                    if tckno == users[user]["tckno"]:
                        tk.messagebox.showerror("TCKNO Exists", "Try a different TCKNO.")
                        return
                users[username] = {
                    "password": password,
                    "tckno": tckno,
                    "name": name,
                    "surname": surname,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "user_type": user_type
                }
                tk.messagebox.showinfo("Success", "Account created successfully.")
                self.destroy()
                with open("users.json", "w") as file:
                    json.dump(users, file)
        else:
            tk.messagebox.showerror("Error", "Please fill all the fields.")

    def sign_in(self):
        self.destroy()
    
class signInPage(tk.Tk):
    def _init_(self):
        super()._init_
        self.geometry("400x400")
        self.title("Sign In")

        self.username_label = tk.Label(self, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=10)
        
        #make password invisible
        self.password_entry = tk.Entry(self, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        self.sign_in_button = tk.Button(self, text="Sign In", command=self.sign_in)
        self.sign_in_button.pack(pady=5)

        self.sign_up_button = tk.Button(self, text="Sign Up", command=self.sign_up)
        self.sign_up_button.pack(pady=5)

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        

        if username and password:
            with open("users.json", "r") as file:
                users = json.load(file)
            if username in users:
                if users[username]["password"] == password:
                    if users[username]["user_type"] == "admin":
                        confirm = tk.messagebox.askyesno("Admin Login Successful", "Do you want to open the admin panel?")
                        if confirm:
                            self.destroy()
                            global admin
                            admin = AdminPage(username)
                            admin.mainloop()                   
                    
                    self.destroy()        
                    global app
                    #This is the calendar app 
                    #app = CalendarApp(username,users[username]["tckno"])
                    #app.mainloop()
                    
                else:
                    tk.messagebox.showerror("Login Failed", "Password is incorrect.")
            else:
                tk.messagebox.showerror("Login Failed", "Username does not exist.")
        else:
            tk.messagebox.showerror("Login Failed", "Please fill in both fields.")

    def sign_up(self):
        global sign_up_page
        
        self.destroy()
        sign_up_page = signUpPage()
        sign_up_page.mainloop()


    def _init_(self):
        super()._init_()
        self.geometry("400x400")
        self.title("Change Password")

        self.username_label = tk.Label(self, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.old_password_label = tk.Label(self, text="Old Password:", font=("Arial", 14))
        self.old_password_label.pack(pady=10)

        self.old_password_entry = tk.Entry(self, font=("Arial", 14))
        self.old_password_entry.pack(pady=5)

        self.new_password_label = tk.Label(self, text="New Password:", font=("Arial", 14))
        self.new_password_label.pack(pady=10)

        self.new_password_entry = tk.Entry(self, font=("Arial", 14))
        self.new_password_entry.pack(pady=5)

        self.change_password_button = tk.Button(self, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=10)

    def change_password(self):
        username = self.username_entry.get()
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        if username and old_password and new_password:
            with open("users.json", "r") as file:
                users = json.load(file)
            if username in users:
                if users[username]["password"] == old_password:
                    users[username]["password"] = new_password
                    with open("users.json", "w") as file:
                        json.dump(users, file, indent=4)
                    tk.messagebox.showinfo("Success", "Password changed successfully.")
                    self.destroy()
                else:
                    tk.messagebox.showerror("Error", "Old password is incorrect.")
            else:
                tk.messagebox.showerror("Error", "Username does not exist.")
        else:
            tk.messagebox.showerror("Error", "Please fill in the fields.")


if __name__ == "__main__":
    signInPage().mainloop()
