from tkinter import *
from tkinter import messagebox
import pandas
import os

# Constants
COLOR = 'darkgrey'
FONT = ('Arial', 25)
FONT2 = ('Arial', 15)
CSV_FILE = 'data.csv'


class AddressBookApp(Tk):
    def __init__(self):
        # import Tk class
        super().__init__()
        self.title("Address Book App")
        self.configure(background=COLOR)

        self.setup_buttons()

        self.entry_vars = [StringVar() for _ in range(5)]
        self.labels = ["Name", "Address", "Phone", "Email", "Date of Birth"]

        self.display_contact = Listbox(self, bg="black", fg="white", width=60, height=20, font=FONT2)
        self.display_contact.grid(column=1, row=1, rowspan=4, padx=20, pady=20)

        self.contacts = []
        self.setup_contact_display()

    def setup_buttons(self):
        add_button = Button(self, text="Add", command=self.on_add_button_click, height=2, width=10)
        add_button.grid(column=0, row=1, padx=10, pady=10)

        view_button = Button(self, text="View", command=self.on_view_button_click, height=2, width=10)
        view_button.grid(column=0, row=2, padx=10, pady=10)

        edit_button = Button(self, text="Edit", command=self.on_edit_button_click, height=2, width=10)
        edit_button.grid(column=0, row=3, padx=10, pady=10)

        delete_button = Button(self, text="Delete", command=self.on_delete_button_click, height=2, width=10)
        delete_button.grid(column=0, row=4, padx=10, pady=10)

    def get_selected_contact(self):
        for index in self.display_contact.curselection():
            return self.display_contact.get(index), index

    def add_entry(self, master, should_disable):
        for index, var in enumerate(self.entry_vars, start=2):
            entry = Entry(master, font=FONT2, textvariable=var, width=30)
            entry.grid(column=1, row=index, padx=10, pady=10)
            if not should_disable:
                entry.config(state="disabled")

    def add_labels(self, master):
        for index, label_text in enumerate(self.labels, start=2):
            label = Label(master, text=label_text, background=COLOR, font=FONT)
            label.grid(column=0, row=index, padx=10, pady=10)

    def on_add_button_click(self):
        add_window = Toplevel(self)
        add_window.title("Add New Contact")
        add_window.configure(background=COLOR)

        self.add_labels(add_window)
        self.add_entry(add_window, should_disable=True)

        submit_button = Button(add_window, text="Submit", command=self.submit_contact, height=2, width=10)
        submit_button.grid(column=0, row=7, pady=20)

        cancel_button = Button(add_window, text="Cancel", command=add_window.destroy, height=2, width=10)
        cancel_button.grid(column=1, row=7, pady=20)

    def on_view_button_click(self):
        try:
            edit_contact, index = self.get_selected_contact()
        except TypeError:
            messagebox.showerror("No contact selected", "Please select a contact card to view")
            return
        try:
            df = pandas.read_csv(CSV_FILE)
            df = df.to_dict()
        except FileNotFoundError:
            messagebox.showerror("Contact list empty", "There are no contacts in the address book yet")
            return

        delete_window = Toplevel(self)
        delete_window.title("Delete Contact")
        delete_window.configure(background=COLOR)
        self.add_labels(delete_window)
        self.add_entry(delete_window, should_disable=False)

        for count, element in enumerate(self.entry_vars):
            element.set(df[self.labels[count]][index])

        edit = Button(delete_window, text="Edit", command=self.on_edit_button_click, height=2, width=10)
        edit.grid(column=0, row=7, pady=20)

        cancel_button = Button(delete_window, text="Cancel", command=delete_window.destroy, height=2, width=10)
        cancel_button.grid(column=1, row=7, pady=20)

    def on_edit_button_click(self):
        try:
            edit_contact, index = self.get_selected_contact()
        except TypeError:
            messagebox.showerror("No contact selected", "Please select a contact card to edit")
            return
        try:
            df = pandas.read_csv(CSV_FILE)
            df = df.to_dict()
        except FileNotFoundError:
            messagebox.showerror("Contact list empty", "There are no contacts in the address book yet")
            return

        edit_window = Toplevel(self)
        edit_window.title("Edit Contact")
        edit_window.configure(background=COLOR)
        self.add_labels(edit_window)
        self.add_entry(edit_window, should_disable=True)

        for count, element in enumerate(self.entry_vars):
            element.set(df[self.labels[count]][index])

        add_button = Button(edit_window, text="Confirm changes", command=lambda: (self.save_changes(index)),
                            height=2,
                            width=10)
        add_button.grid(column=0, row=7, pady=20)

        cancel_button = Button(edit_window, text="Cancel", command=edit_window.destroy, height=2, width=10)
        cancel_button.grid(column=1, row=7, pady=20)

    def on_delete_button_click(self):
        try:
            edit_contact, index = self.get_selected_contact()
        except TypeError:
            messagebox.showerror("No contact selected", "Please select a contact card to delete")
            return
        try:
            df = pandas.read_csv(CSV_FILE)
            df = df.to_dict()
        except FileNotFoundError:
            messagebox.showerror("Contact list empty", "There are no contacts in the address book yet")
            return

        delete_window = Toplevel(self)
        delete_window.title("Delete Contact")
        delete_window.configure(background=COLOR)
        self.add_labels(delete_window)
        self.add_entry(delete_window, should_disable=False)

        for count, element in enumerate(self.entry_vars):
            element.set(df[self.labels[count]][index])

        delete = Button(delete_window, text="Confirm Delete", command=lambda: (self.on_delete(index)), height=2,
                        width=10)
        delete.grid(column=0, row=7, pady=20)

        cancel_button = Button(delete_window, text="Cancel", command=delete_window.destroy, height=2, width=10)
        cancel_button.grid(column=1, row=7, pady=20)

    def submit_contact(self):
        # Checking if the file already exists
        write_headers = not os.path.isfile(CSV_FILE)
        contact_data = {}
        for index, item in enumerate(self.entry_vars, start=0):
            contact_data.update({self.labels[index]: item.get()})
        df = pandas.DataFrame(contact_data, index=[0])
        df.to_csv(CSV_FILE, mode='a', index=False, header=write_headers)
        alert_box = Toplevel(self)
        alert_box.title("Alert")
        alert_box.configure(background=COLOR)
        label = Label(alert_box, text="Record Added Successfully", background=COLOR, font=FONT)
        label.grid(column=0, row=7, padx=10, pady=10)
        ok_button = Button(alert_box, text="ok", command=alert_box.destroy, height=2, width=10)
        ok_button.grid(column=0, row=8, pady=20)
        for items in self.entry_vars:
            items.set("")

        self.setup_contact_display()

    def save_changes(self, at_index):
        test_data = pandas.read_csv(CSV_FILE)

        test_data.drop([at_index], inplace=True)

        test_data.to_csv(CSV_FILE, mode='w+', index=False, header=True)
        contact_data = {}
        for index, item in enumerate(self.entry_vars, start=0):
            contact_data.update({self.labels[index]: item.get()})
        df = pandas.DataFrame(contact_data, index=[0])
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)

        alert_box = Toplevel(self)
        alert_box.title("Alert")
        alert_box.configure(background=COLOR)
        label = Label(alert_box, text="Record edited Successfully", background=COLOR, font=FONT)
        label.grid(column=0, row=7, padx=10, pady=10)
        ok_button = Button(alert_box, text="ok", command=alert_box.destroy, height=2, width=10)
        ok_button.grid(column=0, row=8, pady=20)
        for items in self.entry_vars:
            items.set("")

        self.setup_contact_display()

    def on_delete(self, index):
        test_data = pandas.read_csv(CSV_FILE)

        test_data.drop([index], inplace=True)

        test_data.to_csv("data.csv", mode='w+', index=False, header=True)

        alert_box = Toplevel(self)
        alert_box.title("Alert")
        alert_box.configure(background=COLOR)
        label = Label(alert_box, text="Record Deleted Successfully", background=COLOR, font=FONT)
        label.grid(column=0, row=7, padx=10, pady=10)
        ok_button = Button(alert_box, text="ok", command=alert_box.destroy, height=2, width=10)
        ok_button.grid(column=0, row=8, pady=20)
        for items in self.entry_vars:
            items.set("")

        self.setup_contact_display()

    def setup_contact_display(self):

        try:
            df = pandas.read_csv(CSV_FILE)
            self.contacts = df.to_dict('records')

        except FileNotFoundError:
            pass

        # Clearing existing items from the listbox
        self.display_contact.delete(0, END)

        if not self.contacts:
            self.display_contact.insert(0, 'No Contact Added')
        else:
            for index, item in enumerate(self.contacts):
                data = item['Name']
                self.display_contact.insert(index, data)


if __name__ == "__main__":
    app = AddressBookApp()
    app.mainloop()
