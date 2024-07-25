# Address-Book-App
Address Book App in Python

>This application is a simple Address Book implemented using Python's tkinter library for the graphical user interface (GUI) and pandas for handling CSV file operations. The Address Book allows users to add, view, edit, and delete contacts. Contacts are stored in a CSV file named data.csv.

**Features**
1. Add New Contact: Open a window to enter details for a new contact.
2. View Contact: View details of a selected contact.
3. Edit Contact: Modify details of a selected contact.
4. Delete Contact: Remove a selected contact from the address book.
5. Contact Display: Show a list of contacts in a listbox.
   
**Requirements**
1. Python 3.x
2. pandas library (install via pip install pandas)
3. tkinter library (comes pre-installed with Python)

**Installation**
1. Clone the repository:
git clone https://github.com/your_username/address-book-app.git
2. Navigate to the project directory:
cd address-book-app
3. Install dependencies:
pip install pandas

**Usage**
1. python address_book_app.py
2. Functionality:
   + Add New Contact:
      - Click the "Add" button.
      - Enter details (Name, Address, Phone, Email, Date of Birth) in the new window that appears.
      - Click "Submit" to save the contact.
   + View Contact:
      - Select a contact from the list.
      - Click the "View" button.
      - The details of the selected contact will be displayed, and you can choose to "Edit" or "Cancel".
   + Edit Contact:
      - Select a contact from the list.
      - Click the "Edit" button.
      - Modify details in the window that appears.
      - Click "Confirm changes" to save updates or "Cancel" to discard changes.
   + Delete Contact:
      - Select a contact from the list.
      - Click the "Delete" button.
      - Confirm the deletion in the window that appears by clicking "Confirm Delete" or "Cancel".
   + Contact Display:
      - Contacts are displayed in the main window's listbox. If no contacts are present, "No Contact Added" will be shown.

**File Format**
The contact data is stored in data.csv with the following headers:
- Name
- Address
- Phone
- Email
- Date of Birth
Each contact is stored as a row in the CSV file.

**Code Structure**
+ AddressBookApp Class: Contains methods for initializing the application, setting up the GUI, and handling button clicks.
+ Initialization and Setup: Methods for setting up buttons, the contact display, and entry fields.
+ Button Actions: Methods for adding, viewing, editing, and deleting contacts.
+ UI Helpers: Methods for creating and managing GUI elements like windows, labels, and entries.

**Contributing**
Feel free to fork the repository and submit pull requests. Contributions and improvements are welcome!


>This README file provides a comprehensive overview of the Address Book application, covering setup, usage, and contribution guidelines. Adjust any sections as needed to fit the specifics of your project.




