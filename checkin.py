""" A simple check-in application for events."""

import csv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import re


# Function to read the guest list from the CSV file
def read_guest_list(file_name):
    """ Reads the guest list from the CSV file. 
        Returns a list of dictionaries containing the guest data.
    """
    guest_list = []
    with open(file_name, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            guest_list.append(row)
    return guest_list

# Function to check if a guest is in the list
def is_guest_in_list(guest_list, first_name, last_name):
    """ Checks if a guest is in the list.
        Returns True if the guest is in the list, False otherwise.
    """
    for guest in guest_list:
        if guest["First Name"] == first_name and guest["Last Name"] == last_name:
            return True
    return False

# Function to add a new guest to the guest list
def add_guest(guest_list, first_name, last_name, phone, email):
    """ Adds a new guest to the guest list.
        Returns True if the guest is added successfully, False otherwise.
    """
    new_guest = {
        "First Name": first_name,
        "Last Name": last_name,
        "Phone": phone,
        "Email": email,
        "Checked In": "Yes" # If we add them, they are checked in
    }
    guest_list.append(new_guest)
    return True

# Function to save the updated guest list to the CSV file
def save_guest_list(file_name, guest_list):
    """ Saves the updated guest list to the CSV file.
        Returns True if the guest list is saved successfully, False otherwise.
    """
    with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["First Name", "Last Name", "Phone", "Email", "Checked In"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for guest in guest_list:
            writer.writerow(guest)

# Function to export guest list data to a CSV file
def export_guest_list():
    """ Exports guest list data to a CSV file.
        Returns True if the guest list is exported successfully, False otherwise.
    """
    try:
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                        filetypes=[("CSV Files",
                                                                    "*.csv")
                                                                   ]
                                                        )
        if export_file_path:
            with open(export_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["First Name", "Last Name", "Phone", "Email", "Checked In"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for guest in guest_list:
                    writer.writerow(guest)
            messagebox.showinfo("Export CSV", "Guest list data exported successfully.")
    except FileNotFoundError as e:
        messagebox.showerror("Export CSV", f"File not found: {e}")
    except PermissionError as e:
        messagebox.showerror("Export CSV", f"Permission denied: {e}")
    except Exception as e:
        messagebox.showerror("Export CSV", f"An unexpected error occurred: {e}")


# Function to handle the Check-in button click
def check_in_button_click():
    """ Handles the Check-in button click."""
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    if not first_name or not last_name:
        messagebox.showinfo("Check-in", "Please enter both First Name and Last Name.")
    elif is_guest_in_list(guest_list, first_name, last_name):
        for guest in guest_list:
            if guest["First Name"] == first_name and guest["Last Name"] == last_name:
                guest["Checked In"] = "Yes"  # Update the check-in status to "Yes"
                break  # Exit the loop once the guest is found and updated
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        save_guest_list(file_name, guest_list)  # Save the updated guest list
        messagebox.showinfo("Check-in", "Guest checked in successfully.")
    else:
        messagebox.showinfo("Check-in", "Guest not found in the list. Please add the guest first.")

# Function to handle the Add Guest button click
def add_guest_button_click():
    """ Handles the Add Guest button click."""
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    # Define regex patterns
    phone_pattern = r'^\+(?:\d{1,4}-)?[\d\s]{4,14}$'  # Matches a phone number (adjust as needed)
    email_pattern = r'^[\w\.-]+@[\w\.-]+$'  # Matches a basic email address (adjust as needed)

    if not first_name or not last_name or not phone or not email:
        messagebox.showerror("Add Guest", "Please fill in all fields.")
    elif is_guest_in_list(guest_list, first_name, last_name):
        messagebox.showinfo("Add Guest", "Guest is already in the list.")
    elif not re.match(phone_pattern, phone):
        messagebox.showerror("Add Guest", "Invalid phone number format.")
    elif not re.match(email_pattern, email):
        messagebox.showerror("Add Guest", "Invalid email address format.")
    else:
        if add_guest(guest_list, first_name, last_name, phone, email):
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            messagebox.showinfo("Add Guest", "Guest added successfully.")
            save_guest_list(file_name, guest_list)
        else:
            messagebox.showerror("Add Guest", "Failed to add the guest. Please check your input.")

# Function to display the list of guests in a new window
def display_guest_list():
    """ Displays the list of guests in a new window."""
    guest_list_window = tk.Toplevel(window)
    guest_list_window.title("Guest List")

    # Create a treeview to display the guest list
    tree = ttk.Treeview(guest_list_window, columns=("First Name",
                                                    "Last Name",
                                                    "Phone",
                                                    "Email",
                                                    "Checked In"
                                                    )
                        )
    tree.heading("#1", text="First Name")
    tree.heading("#2", text="Last Name")
    tree.heading("#3", text="Phone")
    tree.heading("#4", text="Email")
    tree.heading("#5", text="Checked In")

    for guest in guest_list:
        tree.insert("", "end", values=(guest["First Name"],
                                       guest["Last Name"],
                                       guest["Phone"],
                                       guest["Email"],
                                       guest["Checked In"]
                                       )
                    )

    tree.pack()

# Create the main window
window = tk.Tk()
window.title("Check-in Application")
window.geometry("500x580")  # Set the window size

# Read the guest list
file_name = "guests.csv"
guest_list = read_guest_list(file_name)

# Create and configure the input fields and buttons
form_frame = tk.Frame(window, padx=20, pady=20)  # Add padding to the form
form_frame.pack(fill="both", expand=True)  # Expand to fill the window

# Add explanatory labels for user guidance
instructions_label = tk.Label(form_frame,
                              text="First Name + LastName\n&\n Choose an action.",
                              font=("Helvetica", 14, "bold")
                              )
instructions_label.pack(pady=30) # Add padding to the label

first_name_label = tk.Label(form_frame, text="First Name:")
first_name_label.pack()

first_name_entry = tk.Entry(form_frame, width=30)
first_name_entry.pack()

last_name_label = tk.Label(form_frame, text="Last Name:")
last_name_label.pack()

last_name_entry = tk.Entry(form_frame, width=30)
last_name_entry.pack()

phone_label = tk.Label(form_frame, text="Phone:")
phone_label.pack()

phone_entry = tk.Entry(form_frame)
phone_entry.pack()

email_label = tk.Label(form_frame, text="Email:")
email_label.pack()

email_entry = tk.Entry(form_frame, width=30)
email_entry.pack(pady=20)

# Add buttons to check-in and add a new guest
check_in_button = tk.Button(form_frame, text="Check-in",
                            command=check_in_button_click,
                            width=10,
                            bg="green",
                            fg="white",
                            )
check_in_button.pack()

# Add a button to add a new guest
add_guest_button = tk.Button(form_frame, text="Add Guest",
                             command=add_guest_button_click,
                             width=10,
                            bg="blue",
                            fg="white"
                             )
add_guest_button.pack()

# Add a button to display the list of guests
display_guests_button = tk.Button(window, text="Display Guest List",
                                  command=display_guest_list
                                  )
display_guests_button.pack(pady=10)

# Add a button to export guest list data to CSV
export_csv_button = tk.Button(window, text="Export CSV",
                              command=export_guest_list,
                              width=10
                              )
export_csv_button.pack(pady=10)

# Run the main loop
window.mainloop()
