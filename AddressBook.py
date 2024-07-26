from tkinter import *
from tkinter import messagebox
import pandas
import os

# Constants for UI appearance and file path
COLOR = 'darkgrey'  # Background color for the application
FONT = ('Arial', 25)  # Font style for main labels and headings
FONT2 = ('Arial', 15)  # Font style for entry fields and listbox
CSV_FILE = 'data.csv'  # Path to the CSV file where contacts are stored


class AddressBookApp(Tk):
    def __init__(self):
        # Initialize the Tk class and set up the main application window
        super().__init__()
        # Set the title and background color of the window
        self.title("Address Book App")
        self.configure(background=COLOR)
        # Set up the buttons for the application
        self.setup_buttons()
        # Initialize variables for entry fields and labels
        self.entry_vars = [StringVar() for _ in range(5)]  # Variables to store user input
        self.labels = ["Name", "Address", "Phone", "Email", "Date of Birth"]  # Labels for the entry fields
        # Create and position the listbox to display contacts
        self.display_contact = Listbox(self, bg="black", fg="white", width=60, height=20, font=FONT2)
        self.display_contact.grid(column=1, row=1, rowspan=4, padx=20, pady=20)
        # Initialize an empty list to hold contact details
        self.contacts = []
        # Load and display existing contacts
        self.setup_contact_display()

    def setup_buttons(self):
        """Create and place buttons on the UI and connect them to the relevant commands"""
        # Button to add a new contact
        add_button = Button(self, text="Add", command=self.on_add_button_click, height=2, width=10)
        add_button.grid(column=0, row=1, padx=10, pady=10)

        # Button to view a selected contact
        view_button = Button(self, text="View", command=self.on_view_button_click, height=2, width=10)
        view_button.grid(column=0, row=2, padx=10, pady=10)

        # Button to edit a selected contact
        edit_button = Button(self, text="Edit", command=self.on_edit_button_click, height=2, width=10)
        edit_button.grid(column=0, row=3, padx=10, pady=10)

        # Button to delete a selected contact
        delete_button = Button(self, text="Delete", command=self.on_delete_button_click, height=2, width=10)
        delete_button.grid(column=0, row=4, padx=10, pady=10)

    def get_selected_contact(self):
        """Return the selected contact from the listbox or display window"""
        for index in self.display_contact.curselection():
            return self.display_contact.get(index), index

    def add_entry(self, master, should_not_disable):
        """Create entry fields for user input and optionally disable them"""
        for index, var in enumerate(self.entry_vars, start=2):
            entry = Entry(master, font=FONT2, textvariable=var, width=30)
            entry.grid(column=1, row=index, padx=10, pady=10)
            if not should_not_disable:
                entry.config(state="disabled")  # Disable the entry field if needed

    def add_labels(self, master):
        """Create and place labels for the entry fields"""
        for index, label_text in enumerate(self.labels, start=2):
            label = Label(master, text=label_text, background=COLOR, font=FONT)
            label.grid(column=0, row=index, padx=10, pady=10)

    def create_alert_box(self, title, should_not_disable, command, button_text):
        """Create a toplevel alert window with submit and cancel buttons"""
        window = Toplevel(self)  # Create a new top-level window
        window.title(title)  # Set the title of the alert window
        window.configure(background=COLOR)  # Set the background color
        self.add_labels(window)  # Add labels to the alert window
        self.add_entry(window, should_not_disable=should_not_disable)  # Add entry fields
        # Button to submit the data
        submit_button = Button(window, text=button_text, command=command, height=2, width=10)
        submit_button.grid(column=0, row=7, pady=20)
        # Button to cancel and close the alert window
        cancel_button = Button(window, text="Cancel", command=window.destroy, height=2, width=10)
        cancel_button.grid(column=1, row=7, pady=20)



    def secondary_alert_box(self, title, text):
        """Create a secondary alert box for displaying messages"""
        window = Toplevel(self)  # Create a new top-level window
        window.title(title)  # Set the title of the alert window
        window.configure(background=COLOR)  # Set the background color
        # Label to display the message
        label = Label(window, text=text, background=COLOR, font=FONT)
        label.grid(column=0, row=7, padx=10, pady=10)
        # Button to close the alert window
        ok_button = Button(window, text="ok", command=window.destroy, height=2, width=10)
        ok_button.grid(column=0, row=8, pady=20)

    def on_add_button_click(self):
        """Handle the click event for the 'Add' button"""
        self.create_alert_box(title="Add New Contact", should_not_disable=True, command=self.submit_contact,
                              button_text="Submit")

    def on_button_click(self, title_text, should_not_disable, on_button_func, button_text):
        """Handle click events for view, edit, and delete buttons"""
        try:
            edit_contact, index = self.get_selected_contact()  # Get the selected contact
        except TypeError:
            messagebox.showerror("No contact selected",
                                 "Please select a contact card")  # Show error if no contact is selected
            return
        try:
            df = pandas.read_csv(CSV_FILE)  # Read the contact data from CSV file
            df = df.to_dict()  # Convert DataFrame to dictionary
        except FileNotFoundError:
            messagebox.showerror("Contact list empty",
                                 "There are no contacts in the address book yet")  # Show error if file is not found
            return
        if title_text == "Edit" or title_text == "Delete":
            self.create_alert_box(title=title_text, should_not_disable=should_not_disable,
                                  command=lambda: (on_button_func(index)), button_text=button_text)
        else:
            self.create_alert_box(title=title_text, should_not_disable=should_not_disable, command=on_button_func,
                                  button_text=button_text)

        for count, element in enumerate(self.entry_vars):
            element.set(df[self.labels[count]][index])  # Set entry fields with selected contact's data

    def on_view_button_click(self):
        """Handle the click event for the 'View' button"""
        self.on_button_click(title_text="View", should_not_disable=False, on_button_func=self.on_edit_button_click,
                             button_text="Edit")

    def on_edit_button_click(self):
        """Handle the click event for the 'Edit' button"""
        self.on_button_click(title_text="Edit", should_not_disable=True, on_button_func=self.save_changes,
                             button_text="Confirm")

    def on_delete_button_click(self):
        """Handle the click event for the 'Delete' button"""
        self.on_button_click(title_text="Delete", should_not_disable=False, on_button_func=self.on_delete,
                             button_text="Confirm")

    def submit_contact(self):
        """Submit a new contact to the CSV file"""
        # Check if the CSV file requires headers
        write_headers = not os.path.isfile(CSV_FILE)
        contact_data = {}
        for index, item in enumerate(self.entry_vars, start=0):
            contact_data.update({self.labels[index]: item.get()})  # Collect contact data from entry fields
        df = pandas.DataFrame(contact_data, index=[0])  # Create a DataFrame from the contact data
        df.to_csv(CSV_FILE, mode='a', index=False, header=write_headers)  # Append contact data to the CSV file
        self.secondary_alert_box(title="Alert", text="Record Added Successfully")  # Show success message

        for items in self.entry_vars:
            items.set("")  # Clear the entry fields

        self.setup_contact_display()  # Refresh the contact list display

    def save_changes(self, at_index):
        """Update an existing contact entry in the CSV file"""
        test_data = pandas.read_csv(CSV_FILE)  # Read existing contact data
        test_data.drop([at_index], inplace=True)  # Remove the old contact entry

        test_data.to_csv(CSV_FILE, mode='w+', index=False, header=True)  # Write the updated data back to the CSV file
        contact_data = {}
        for index, item in enumerate(self.entry_vars, start=0):
            contact_data.update({self.labels[index]: item.get()})  # Collect updated contact data
        df = pandas.DataFrame(contact_data, index=[0])  # Create a DataFrame from the updated contact data
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)  # Append updated data to the CSV file
        self.secondary_alert_box(title="Alert", text="Record edited Successfully")  # Show success message

        for items in self.entry_vars:
            items.set("")  # Clear the entry fields

        self.setup_contact_display()  # Refresh the contact list display

    def setup_contact_display(self):
        """Display the stored contacts in the listbox"""
        try:
            df = pandas.read_csv(CSV_FILE)  # Read the contact data from the CSV file
            self.contacts = df.to_dict('records')  # Convert DataFrame to a list of dictionaries

        except FileNotFoundError:
            pass  # Do nothing if the file is not found

        # Clear existing items from the listbox
        self.display_contact.delete(0, END)

        if not self.contacts:
            self.display_contact.insert(0, 'No Contact Added')  # Show a message if no contacts are available
        else:
            for index, item in enumerate(self.contacts):
                data = item['Name']  # Get the name of each contact
                self.display_contact.insert(index, data)  # Insert contact name into the listbox

    def on_delete(self, index):
        """Delete a contact entry from the CSV file"""
        test_data = pandas.read_csv(CSV_FILE)  # Read existing contact data
        test_data.drop([index], inplace=True)  # Remove the contact entry at the specified index

        test_data.to_csv("data.csv", mode='w+', index=False, header=True)  # Write the updated data back to the CSV file
        self.secondary_alert_box(title="Alert", text="Record Deleted Successfully")  # Show success message

        for items in self.entry_vars:
            items.set("")  # Clear the entry fields

        self.setup_contact_display()  # Refresh the contact list display


if __name__ == "__main__":
    app = AddressBookApp()  # Create an instance of the AddressBookApp class
    app.mainloop()  # Start the Tkinter event loop
