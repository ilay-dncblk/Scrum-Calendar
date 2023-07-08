import tkinter as tk
import json
import tkinter.messagebox
import datetime as dt
import calendar
import uuid
import os
import winsound

class CalendarApp(tk.Tk):
    def __init__(self,user,tckn):
        super().__init__()
        self.root = self
        self.title(user+ "'s Calendar")
        self.resizable(False, False)
        self.events = {}
        self.selected_date = None
        self.tckno=tckn

        # Get the current date
        self.current_date = dt.date.today()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month
        
        

        self.load_events_from_json(tckn)

        self.create_widgets()

        self.generate_calendar()

    def create_widgets(self):
        # Create the calendar label
        calendar_label = tk.Label(self.root, text="Calendar", font=("Arial", 16, "bold"))
        calendar_label.pack(pady=10)
        
        current = dt.datetime.now()
        # Create the current date label
        self.date_label = tk.Label(self.root, text=current.strftime("%A, %B %d, %Y"), font=("Arial", 12))
        self.date_label.pack(pady=10)
        
        current_time = dt.datetime.now()
        # Create the current time label
        self.time_label = tk.Label(self.root, text=current_time.strftime("%H:%M"), font=("Arial", 12))
        self.time_label.pack(pady=10)
        
        #Create the calendar info label
        calendar_info_label = tk.Label(self.root, text="Click on a date to see events", font=("Arial", 8))
        calendar_info_label.pack(pady=10)
        
        # Create year and month navigation buttons 4 by 4
        navigation_frame = tk.Frame(self.root)
        navigation_frame.pack()
        
        # Create the current year label
        self.year_label = tk.Label(navigation_frame, text="Year", font=("Arial", 12))
        self.year_label.grid(row=1,column=1,padx=10)
        
        # Create the previous year button
        previous_year_button = tk.Button(navigation_frame, text="<<", command=self.prev_year)
        previous_year_button.grid(row=1, column=0, padx=10)
        
        # Create the next year button
        next_year_button = tk.Button(navigation_frame, text=">>", command=self.next_year)
        next_year_button.grid(row=1, column=2, padx=10)

        # Create the current month label
        self.month_label = tk.Label(navigation_frame, text="Month", font=("Arial", 12))
        self.month_label.grid(row=3,column=1,padx=10)
        
        # Create the previous month button
        previous_month_button = tk.Button(navigation_frame, text="<", command=self.prev_month)
        previous_month_button.grid(row=3, column=0, padx=10)
        
        # Create the next month button
        next_month_button = tk.Button(navigation_frame, text=">", command=self.next_month)
        next_month_button.grid(row=3, column=2, padx=10)
        
        # Create the calendar frame
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        # Create the event listbox
        self.event_listbox = tk.Listbox(self.root, width=80)
        self.event_listbox.pack(pady=10)
        
        # Create selected event label
        self.selected_event_label_d = tk.Label(self.root, text="No event selected", font=("Arial", 12))
        self.selected_event_label_d.pack(pady=1)
        self.selected_event_label_t = tk.Label(self.root, text="", font=("Arial", 8))
        self.selected_event_label_t.pack(pady=1)
        
        self.selected_event_label_ut = tk.Label(self.root, text="", font=("Arial", 8))
        self.selected_event_label_ut.pack(pady=1)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack()
        # Create buttons
        create_button = tk.Button(buttons_frame, text="Create Event", command=self.create_event)
        create_button.grid(row=0,column=0,pady=5)

        update_button = tk.Button(buttons_frame, text="Update Event", command=self.update_event)
        update_button.grid(row=0,column=1,pady=5)

        delete_button = tk.Button(buttons_frame, text="Delete Event", command=self.delete_event)
        delete_button.grid(row=1,column=0,pady=5)
        
        quit_button = tk.Button(buttons_frame, text="Quit Calendar", command=self.quit_calendar)
        quit_button.grid(row=1,column=1,pady=5)

    def quit_calendar(self):
        self.save_events_to_json(self.tckno)
        print("Calendar closed")
        super().destroy()
    
    def generate_calendar(self):
        # Clear the calendar frame
        for child in self.calendar_frame.winfo_children():
            child.destroy()

        # Generate the calendar grid for the current month
        calendar_grid = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Create the header for the calendar
        header_frame = tk.Frame(self.calendar_frame)
        header_frame.pack()
        
        # Create the labels for the header frame
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            label = tk.Label(header_frame, text=day, width=10, font=("Arial", 10, "bold"))
            label.pack(side=tk.LEFT)
            
        # Create the actual calendar but with buttons
        for week in calendar_grid:
            week_frame = tk.Frame(self.calendar_frame)
            week_frame.pack()
            for day in week:
                if day == 0:
                    label = tk.Label(week_frame, text="", width=10)
                    label.pack(side=tk.LEFT, padx=5, pady=5)
                else:
                    button = tk.Button(week_frame, text=day, width=10, command=lambda day=day:self.select_date(f"{self.current_year}-{self.current_month:02d}-{day:02d}"))
                    button.pack(side=tk.LEFT, padx=3, pady=3)
                    if dt.date(self.current_year, self.current_month, day) == dt.date.today():
                        button.config(bg="lightgreen")
                        button.config(fg="black")
                        button.config(text="Today")

                    # Set color for dates with events
                    for date in self.events:
                        if date == f"{self.current_year}-{self.current_month:02d}-{day:02d}":
                            button.config(bg="lightblue")
                            button.config(fg="black")
                            #add a dot to the date
                            button.config(text=f"{day}*", font=("Arial", 8, "bold"))
                            if dt.date(self.current_year, self.current_month, day) == dt.date.today():
                                winsound.PlaySound("Bell.WAV", winsound.SND_FILENAME)
                            elif dt.date(self.current_year, self.current_month, day) == dt.date.today() + dt.timedelta(days=1):
                                winsound.PlaySound("Bell.WAV", winsound.SND_FILENAME)
                            break
                        

                    # Bind the click event to show events and select date
                    date = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    button.bind("<Button-1>", lambda event, date=date: self.show_events(date), add="+")
                    button.bind("<Button-1>", lambda event, date=date: self.select_date(date), add="+")
                    #change the color of the selected date
                    if date == self.selected_date:
                        button.config(bg="yellow")
                    
                    
        # Update the month and year labels
        self.year_label.config(text=f"Year : {self.current_year}", font=("Arial", 8, "bold"))
        self.month_label.config(text=f"Month : {self.current_month}", font=("Arial", 8, "bold"))

    def create_event(self):
        if self.selected_date:
            time_picker = tk.Toplevel()
            time_picker.title("Select Time")
            time_picker.geometry("200x150")

        # Saat seçmek için bir zaman seçici widget'ı oluştur
            selected_time = tk.StringVar()
            time_picker_label = tk.Label(time_picker, text="Select Time(hh:dd):", font=("Arial", 14))
            time_picker_label.pack(pady=10)
            time_picker_entry = tk.Entry(time_picker, textvariable=selected_time)
            time_picker_entry.pack(pady=10)
            
            def save_time():
                event_time = selected_time.get()
                creation_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Create the create window
                create_window = tk.Toplevel()
                create_window.title("Create Event")
                create_window.geometry("400x450")

        # Create labels and entry boxes for window
                event_label = tk.Label(create_window, text="Event Date:", font=("Arial", 14))
                event_label.pack(pady=10)
                event_entry = tk.Entry(create_window, font=("Arial", 14))
                event_entry.pack(pady=5)
                event_entry.insert(0, self.selected_date)
                event_entry.config(state=tk.DISABLED)
                
                event_label = tk.Label(create_window, text="Event Time:", font=("Arial", 14))
                event_label.pack(pady=10)
            
                event_entry = tk.Entry(create_window, font=("Arial", 14))
                event_entry.pack(pady=5)
                event_entry.insert(0, event_time)
                event_entry.config(state=tk.DISABLED)
                
                event_label = tk.Label(create_window, text="Event Creation Time:", font=("Arial", 14))
                event_label.pack(pady=10)
                event_label = tk.Label(create_window, text=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), font=("Arial", 14))
                event_label.pack(pady=5)
            
                event_label = tk.Label(create_window, text="Event Name:", font=("Arial", 14))
                event_label.pack(pady=10)

                event_entry = tk.Entry(create_window, font=("Arial", 14))
                event_entry.pack(pady=5)

                desc_label = tk.Label(create_window, text="Event Description:", font=("Arial", 14))
                desc_label.pack(pady=10)

                desc_entry = tk.Entry(create_window, font=("Arial", 14))
                desc_entry.pack(pady=5)

        # Create save button
                save_button = tk.Button(create_window, text="Save", command=lambda: self.add_event(self.selected_date, event_entry.get(), event_time, desc_entry.get(), create_window, creation_time))
                save_button.pack(pady=5)

        # Create cancel button
                cancel_button = tk.Button(create_window, text="Cancel", command=create_window.destroy)
                cancel_button.pack(pady=5)
        
                self.show_events(self.selected_date)
                self.generate_calendar()
                
                time_picker.destroy()
            
            time_picker_gride = tk.Frame(time_picker)
            time_picker_gride.pack(pady=10)
            
            time_picker_button = tk.Button(time_picker_gride, text="Save", command=save_time)
            time_picker_button.grid(row=0, column=0, padx=5, pady=5)
            
            time_picker_button = tk.Button(time_picker_gride, text="Cancel", command=time_picker.destroy)
            time_picker_button.grid(row=0, column=1, padx=5, pady=5)
            
        else:
            tk.messagebox.showwarning("No Date Selected", "Please select a date from the calendar.")
    
    def uuid(self):
        return str(uuid.uuid1())
    
    def add_event(self, date, event_name,time, event_description, create_window, creation_time):
        #Create unique id for the event
        event_id = str(uuid.uuid1())
        # Create the event
        event = {
            event_id: {
                "name": event_name,
                "time": time,
                "creation_time": creation_time,
                "description": event_description,
                "update_time": ""
            }
        }
        # Add the event to the events dictionary
        if date in self.events:
            self.events[date].update(event)
        else:
            self.events[date] = event

        self.save_events_to_json(self.tckno)
        create_window.destroy()
        self.show_events(date)  # Update event listbox
        self.generate_calendar()  # Update calendar to reflect the new event

        tk.messagebox.showinfo("Event Created", "Event has been created successfully.")
           
    def delete_event(self):
        sorted_events = sorted(self.events[self.selected_date].items(), key=lambda x: dt.datetime.strptime(x[1]["time"], "%H:%M"))
        
        if tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete selected event?"):
            del self.events[self.selected_date][sorted_events[self.event_listbox.curselection()[0]][0]]
            self.save_events_to_json(self.tckno)
            self.show_events(self.selected_date)
            self.generate_calendar()
            tk.messagebox.showinfo("Event Deleted", "Event has been deleted successfully.")
                 
    def select_date(self, date):
        self.selected_date = date
    
    def update_event(self):
        if self.selected_date and self.event_listbox.curselection():
        # Get the selected event from the listbox
            selected_event = self.events[self.selected_date]
            sorted_events = sorted(selected_event.items(), key=lambda x: dt.datetime.strptime(x[1]["time"], "%H:%M"))
            event_id = sorted_events[self.event_listbox.curselection()[0]][0]

            if selected_event:
            # Get the event details
                event = selected_event[event_id]
                event_date = self.selected_date
                event_name = event["name"]
                event_time = event["time"]
                event_description = event["description"]
                event_creation_time = event["creation_time"]
                event_update_time = event["update_time"]
                
                
                # Create the update window
                update_window = tk.Toplevel()
                update_window.title("Update Event")
                update_window.geometry("400x400")

                # Create labels and entry boxes for window
                event_label = tk.Label(update_window, text="Event Date:", font=("Arial", 14))
                event_label.pack(pady=10)
                event_date_ = tk.Entry(update_window, font=("Arial", 14))
                event_date_.pack(pady=5)
                event_date_.insert(0, self.selected_date)
                event_date_.config(state=tk.DISABLED)
                
                event_label = tk.Label(update_window, text="Event Time:", font=("Arial", 14))
                event_label.pack(pady=10)
                event_time_ = tk.Entry(update_window, font=("Arial", 14))
                event_time_.pack(pady=5)
                event_time_.insert(0, event_time)
                
                event_label = tk.Label(update_window, text="Event Name:", font=("Arial", 14))
                event_label.pack(pady=10)

                event_name_ = tk.Entry(update_window, font=("Arial", 14))
                event_name_.pack(pady=5)
                event_name_.insert(0, event_name)

                desc_label = tk.Label(update_window, text="Event Description:", font=("Arial", 14))
                desc_label.pack(pady=10)

                event_description_ = tk.Entry(update_window, font=("Arial", 14))
                event_description_.pack(pady=5)
                event_description_.insert(0, event_description)

                # Create save button
                save_button = tk.Button(update_window, text="Save", command=lambda: self.save_updated_event(event_date_.get(),event_id, event_time_.get(), event_name_.get(), event_description_.get(), update_window, event_creation_time))
                save_button.pack(pady=5)

                # Create cancel button
                cancel_button = tk.Button(update_window, text="Cancel", command=update_window.destroy)
                cancel_button.pack(pady=5)
                
                self.show_events(self.selected_date)
                self.generate_calendar()
            else:
                tk.messagebox.showwarning("No Event Selected", "Please select an event from the list.")

    def show_events(self, date):
        self.event_listbox.delete(0, tk.END)

        if date in self.events:
            events = self.events[date]
            sorted_events = sorted(events.items(), key=lambda x: dt.datetime.strptime(x[1]["time"], "%H:%M"))
            sorted_events = dict(sorted_events)
           
           #sort the events by time and display them in the listbox properly
            for event_id in sorted_events:
                event = sorted_events[event_id]
                self.event_listbox.insert(tk.END, f"{event['time']} - {event['name']}")
                
                # Bind double click to event
                self.event_listbox.bind("<Double-Button-1>", lambda _: self.update_event())
        
        self.event_listbox.bind("<<ListboxSelect>>", self.on_event_select)
            
    def on_event_select(self, event):
            
        #show the event details in the event details frame(when an event is selected)
        if self.selected_date and self.event_listbox.curselection():
            events = self.events[self.selected_date]
            sorted_events = sorted(events.items(), key=lambda x: dt.datetime.strptime(x[1]["time"], "%H:%M"))
            sorted_events = dict(sorted_events)
            event_id = list(sorted_events.keys())[self.event_listbox.curselection()[0]]
            event = sorted_events[event_id]
            self.selected_event_label_d.config(text=event["description"])
            self.selected_event_label_t.config(text=f"Created: {event['creation_time']}")
            self.selected_event_label_ut.config(text=f"Updated: {event['update_time']}")
        else:
            self.selected_event_label_d.config(text="No event selected")
            self.selected_event_label_t.config(text="")
            self.selected_event_label_ut.config(text="")
            
    def save_updated_event(self, date, id, time, name, desc, update_window,creation_time):
        
        # Get the selected event from the listbox
        selected_event = self.events[self.selected_date]
        event_id = id
        event_name = name
        event_time = time
        event_description = desc
        event_update_time = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Delete the old event
        del self.events[date][event_id]
        
        if not self.events[date]:
            del self.events[date]
            
        # Add the updated event
        event_id = str(uuid.uuid4())
        selected_event[event_id] = {
            "name": event_name,
            "time": event_time,
            "description": event_description,
            "creation_time": creation_time,
            "update_time": event_update_time
        }
        
        self.events[date] = selected_event
        
        # Save the events to the json file
        self.save_events_to_json(self.tckno)
        update_window.destroy()
        self.show_events(date)
        self.generate_calendar()
        tk.messagebox.showinfo("Event Updated", "Event has been updated successfully.")

    def load_events_from_json(self,tckn):
        #Check if the file exists, if not create it and save the events
        if not os.path.exists(f"{tckn}.json"):
            with open(f"{tckn}.json", "w") as file:
                json.dump({}, file)
        else:
            # If the file exists, load the events from it
            with open(f"{tckn}.json", "r") as file:
                self.events = json.load(file)

    def save_events_to_json(self,tckn):
        #Check if the file exists, if not create it and save the events
        if not os.path.exists(f"{tckn}.json"):
            with open(f"{tckn}.json", "w") as file:
                json.dump(self.events, file)
        else:
            # If the file exists, save the events to it
            with open(f"{tckn}.json", "w") as file:
                json.dump(self.events, file)      

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.generate_calendar()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.generate_calendar()

    def next_year(self):
        self.current_year += 1
        self.generate_calendar()

    def prev_year(self):
        self.current_year -= 1
        self.generate_calendar()

class signUpPage(tk.Tk):
    def __init__(self):
        super().__init__()
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
    def __init__(self):
        super().__init__()
        self.geometry("400x250")
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
                    app = CalendarApp(username,users[username]["tckno"])
                    app.mainloop()
                    
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

class AdminPage(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.geometry("250x200")
        self.title("Admin Page")
        self.username = username

        self.welcome_label = tk.Label(self, text=f"Welcome {username}", font=("Arial", 14))
        self.welcome_label.pack(pady=10)

        self.create_user_button = tk.Button(self, text="Create User", command=self.create_user)
        self.create_user_button.pack(pady=5)

        self.delete_user_button = tk.Button(self, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=5)

        self.change_password_button = tk.Button(self, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=5)

        self.logout_button = tk.Button(self, text="Logout", command=self.logout)
        self.logout_button.pack(pady=5)

    def create_user(self):
        global create_user_page
        create_user_page = CreateUserPage()
        create_user_page.mainloop()

    def delete_user(self):
        global delete_user_page
        delete_user_page = DeleteUserPage()
        delete_user_page.mainloop()

    def change_password(self):
        global change_password_page
        change_password_page = ChangePasswordPage()
        change_password_page.mainloop()

    def logout(self):
        confirm = tk.messagebox.askyesno("Logout", "Are you sure you want to Quit the App?")
        if confirm:
            super().destroy()
        else:
            self.destroy()
            main_page = signInPage()
            main_page.mainloop()
            
class CreateUserPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x850")
        self.title("Create User")

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

        self.user_type_label = tk.Label(self, text="User Type:", font=("Arial", 14))
        self.user_type_label.pack(pady=10)
        
        self.user_type = tk.StringVar()
        self.user_type.set("user")
        self.user_type_menu = tk.OptionMenu(self, self.user_type, "user", "admin")
        self.user_type_menu.pack(pady=5)

        self.create_user_button = tk.Button(self, text="Create User", command=self.create_user)
        self.create_user_button.pack(pady=10)
        
    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        tckno = self.tckno_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        user_type = self.user_type.get()
        if username and password and tckno and name and surname and email and phone and address and user_type:
            with open("users.json", "r") as file:
                users = json.load(file)
            if username in users:
                tk.messagebox.showerror("Error", "Username already exists.")      
            else:
                # Check if tckno is already registered to another user
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
                with open("users.json", "w") as file:
                    json.dump(users, file)
                tk.messagebox.showinfo("Success", "User created successfully.")
                self.destroy()
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields.")
        
class DeleteUserPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Delete User")

        self.username_label = tk.Label(self, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.delete_user_button = tk.Button(self, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=10)

    def delete_user(self):
        username = self.username_entry.get()
        if username:
            with open("users.json", "r") as file:
                users = json.load(file)
            if username in users:
                del users[username]
                with open("users.json", "w") as file:
                    json.dump(users, file, indent=4)
                tk.messagebox.showinfo("Success", "User deleted successfully.")
                self.destroy()
            else:
                tk.messagebox.showerror("Error", "Username does not exist.")
        else:
            tk.messagebox.showerror("Error", "Please fill in the field.")
            
class ChangePasswordPage(tk.Tk):
    def __init__(self):
        super().__init__()
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
