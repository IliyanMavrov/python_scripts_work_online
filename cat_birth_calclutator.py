#!/usr/bin/python3

# # Here’s a simple Python script that takes a date input from the user (the first day of the cat’s pregnancy) and 
# # calculates the expected birth date, assuming a gestation period of 65days:

# from datetime import datetime, timedelta 

# def calculate_birth_date(): 
#     print("Cat Pregnancy Due Date Calculator") 
#     input_date = input("Enter the first day of pregnancy (YYYY-MM-DD): ") 
#     try: 
#         pregnancy_start = datetime.strptime(input_date, "%Y-%m-%d") 
#         birth_date = pregnancy_start + timedelta(days=65) 

#         print(f"Expected date of birth: {birth_date.strftime('%Y-%m-%d')}") 

#     except ValueError: print("Invalid date format. Please use YYYY-MM-DD.") 

# if __name__ == "__main__": calculate_birth_date()


# # How to Use:
# #     Run the script.
# #     Input the start date of pregnancy in the format YYYY-MM-DD (e.g., 2025-03-01).
# #     The script will display the expected birth date, which is 65 days later


# Would you like a version with a graphical calendar input (e.g., using tkinter)?

# Here’s a Python script with a graphical calendar input using tkinter and tkcalendar. 
# It allows the user to pick a date from a calendar, then calculates the expected birth date (65 days later):

# Requirements:

# Make sure you have tkcalendar installed:
# pip install tkcalendar

import tkinter as tk 
from tkinter import messagebox 
from tkcalendar import Calendar 
from datetime import datetime, timedelta 

def calculate_birth_date(): 
    selected_date = cal.get_date() 
    try: 
        pregnancy_start = datetime.strptime(selected_date, "%m/%d/%y") 
        birth_date = pregnancy_start + timedelta(days=65) 

        messagebox.showinfo("Expected Birth Date", f"Expected date of birth: {birth_date.strftime('%Y-%m-%d')}") 

    except ValueError: 
        messagebox.showerror("Error", "Invalid date selected.") 

# GUI setup 
root = tk.Tk() 
root.title("Cat Pregnancy Calculator") 
tk.Label(root, text="Select the first day of pregnancy:").pack(pady=10) 
cal = Calendar(root, selectmode='day', date_pattern='mm/dd/yy') 
cal.pack(pady=10) 
tk.Button(root, text="Calculate Birth Date", command=calculate_birth_date).pack(pady=20) 
root.mainloop()

# What it does:

#     Opens a window with a calendar.
#     Lets you select the first day of pregnancy.
#     Calculates and displays the expected date of birth in a popup.

# Let me know if you’d like to add saving to a file or reminders!