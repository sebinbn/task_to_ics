import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import os

# Function to create an ICS file with scheduled tasks
def create_ics_file(tasks, start_date):
    cal = Calendar()
    current_time = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
    
    for task, duration in tasks:
        remaining_time = duration
        while remaining_time > 0:
            event_duration = min(0.5, remaining_time)  # Each event is 30 mins (0.5 hours)
            event = Event()
            event.add('summary', task)
            event.add('dtstart', current_time)
            event.add('dtend', current_time + timedelta(hours=event_duration))
            event.add('dtstamp', datetime.now())
            cal.add_component(event)
            
            # Update current time for next event segment
            current_time += timedelta(hours=event_duration)
            remaining_time -= event_duration
    
    output_filename = f"SBNCal_{datetime.today().strftime('%Y-%m-%d')}.ics"
    output_path = os.path.join(os.getcwd(),"Output_icals", output_filename)
    
    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())
    
    messagebox.showinfo("Success", f"ICS file '{output_filename}' created successfully in {os.path.join(os.getcwd(),"Output_icals")}.")

# Function to get tasks from user through a GUI
def get_tasks_from_user():
    # Function to collect tasks from input fields and create the ICS file
    def submit_tasks():
        tasks = []
        for i in range(len(task_entries)):
            task = task_entries[i].get().strip()
            duration_text = duration_entries[i].get().strip()
            
            if task and duration_text:
                try:
                    duration = float(duration_text)
                    if duration > 0:
                        tasks.append((task, duration))
                except ValueError:
                    messagebox.showerror("Error", f"Invalid duration for task '{task}'. Please enter a valid number.")
                    return
        
        if tasks:
            start_date = start_date_entry.get().strip()
            if not start_date:
                tomorrow = datetime.now() + timedelta(days=1)
                start_date = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
                messagebox.showinfo("Note", f"Default start date/time set to {start_date} as no date provided")
            root.destroy()
            create_ics_file(tasks, start_date)
        else:
            messagebox.showerror("Error", "No valid tasks entered. Please fill out at least one task.")

    # Function to dynamically add new task input fields
    def add_task_entry():
        task_entry = tk.Entry(root)
        task_entry.grid(row=len(task_entries) + 4, column=0, pady=2)
        duration_entry = tk.Entry(root)
        duration_entry.grid(row=len(duration_entries) + 4, column=1, pady=2)
        
        task_entries.append(task_entry)
        duration_entries.append(duration_entry)

    root = tk.Tk()
    root.title("Task Scheduler")
    
    # Explanation Section
    tk.Label(root, text="This program allows you to create an ICS file for scheduling tasks in your calendar.\
             Enter tasks and duration for tasks. The program splits long tasks into 30 min tasks", wraplength=400, justify="left").grid(row=0, column=0, columnspan=3, pady=10)
    
    # Input Section
    tk.Label(root, text="Enter start date and time (YYYY-MM-DD HH:MM) or leave blank to use default(tomorrow 9 AM):").grid(row=1, column=0, columnspan=3)
    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=2, column=0, columnspan=3, pady=5)
    
    tk.Label(root, text="Task Name").grid(row=3, column=0)
    tk.Label(root, text="Duration (hours)").grid(row=3, column=1)

    # Lists to hold dynamically added entries
    task_entries = []
    duration_entries = []

    # Add initial three rows of input fields
    for i in range(3):
        add_task_entry()

    # Buttons to add more tasks and submit
    add_task_button = tk.Button(root, text="Add More Tasks", command=add_task_entry)
    add_task_button.grid(row= 4, column=3, pady=10)

    submit_button = tk.Button(root, text="Create Calendar", command=submit_tasks)
    submit_button.grid(row= 5, column=3)

    root.mainloop()

# Main function to run the program
def main():
    get_tasks_from_user()

# Entry point of the program
if __name__ == "__main__":
    main()
