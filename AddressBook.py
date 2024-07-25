from tkinter import *
from tkinter import messagebox
import pandas
import os

COLOR = 'darkgrey'
FONT = ('Arial', 25)
FONT2 = ('Arial', 15)


class AddressBookApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Address Book App")
        self.configure(background=COLOR)

        self.setup_buttons()

        self.entry_vars = [StringVar() for _ in range(5)]
        self.labels = ["Name", "Address", "Phone", "Email", "Date of Birth"]

        self.display_contact = Listbox(self, bg="black", fg="white", width=60, height=20, font=FONT2)
        self.display_contact.grid(column=1, row=1, rowspan=4, padx=20, pady=20)

        self.contacts = ""
        self.setup_contact_display()

        self.selected_item = ""

    def setup_buttons(self):
        add_button = Button(self, text="Add", command=self.on_add_button_click, height=2, width=10)
        add_button.grid(column=0, row=1, padx=10, pady=10)

        edit_button = Button(self, text="Edit", command=self.on_edit_button_click, height=2, width=10)
        edit_button.grid(column=0, row=2, padx=10, pady=10)

        delete_button = Button(self, text="Delete", command=self.on_delete_button_click, height=2, width=10)
        delete_button.grid(column=0, row=3, padx=10, pady=10)

    def setup_contact_display(self):

        try:
            df = pandas.read_csv('data.csv')
            self.contacts = df.to_dict('records')

        except FileNotFoundError:
            self.contacts = [{'Name': 'No Contact Added'}]

        for index, item in enumerate(self.contacts):
            data = item['Name']
            self.display_contact.insert(index, data)

    def get_selected_contact(self):
        for index in self.display_contact.curselection():
            return self.display_contact.get(index), index

    def on_add_button_click(self):
        add_window = Toplevel(self)
        add_window.title("Add New Contact")
        add_window.configure(background=COLOR)

        self.add_labels(add_window)
        self.add_entry(add_window)

        submit_button = Button(add_window, text="Submit", command=self.submit_contact, height=2, width=10)
        submit_button.grid(column=0, row=7, pady=20)

        cancel_button = Button(add_window, text="Cancel", command=add_window.destroy, height=2, width=10)
        cancel_button.grid(column=1, row=7, pady=20)

    def add_entry(self, master):
        for index, var in enumerate(self.entry_vars, start=2):
            entry = Entry(master, font=FONT2, textvariable=var, width=30)
            entry.grid(column=1, row=index, padx=10, pady=10)

    def add_labels(self, master):
        for index, label_text in enumerate(self.labels, start=2):
            label = Label(master, text=label_text, background=COLOR, font=FONT)
            label.grid(column=0, row=index, padx=10, pady=10)

    def on_edit_button_click(self):

        self.get_selected_contact()

        try:
            edit_contact, index = self.get_selected_contact()
        except TypeError:
            edit_contact = False
            index = False
        if not edit_contact:
            messagebox.showerror("No contact selected", "Please select a contact card to edit")
        else:
            df = pandas.read_csv('data.csv')
            df = df.to_dict()
            print(df)
            print(index)

            for labels in self.labels:
                print(df[labels][index])

            edit_window = Toplevel(self)
            edit_window.title("Edit Contact")
            edit_window.configure(background=COLOR)
            self.add_labels(edit_window)
            self.add_entry(edit_window)

            for count, element in enumerate(self.entry_vars):
                element.set(df[self.labels[count]][index])

            add_button = Button(edit_window, text="Confirm changes", height=2, width=10)
            add_button.grid(column=0, row=7, pady=20)

            cancel_button = Button(edit_window, text="Cancel", height=2, width=10)
            cancel_button.grid(column=1, row=7, pady=20)

    def on_delete_button_click(self):
        # Placeholder for delete functionality
        pass

    def submit_contact(self):
        # Checking if the file already exists
        write_headers = not os.path.isfile("data.csv")
        contact_data = {}
        for index, item in enumerate(self.entry_vars, start=0):
            contact_data.update({self.labels[index]: item.get()})
        df = pandas.DataFrame(contact_data, index=[0])
        df.to_csv('data.csv', mode='a', index=False, header=write_headers)
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


app = AddressBookApp()
app.mainloop()
