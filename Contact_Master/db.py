import sqlite3

def Initialization():
    conn = sqlite3.connect("contacts.db")  # Ensure this matches the filename used elsewhere
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE)    
            ''')
    conn.commit()
    conn.close()

def add_contact(name, phone, email=None):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    try:
        if email:
            c.execute("INSERT INTO contacts(name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        else:
            c.execute("INSERT INTO contacts(name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle duplicate entry error
        print("Error: Contact already exists.")
    conn.close()

def get_all_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return contacts

def get_one_contact(query):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
                SELECT * FROM contacts
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
    contacts = c.fetchall()
    conn.close()
    return contacts

def update_contact(old_name, new_name, new_phone, new_email):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    try:
        c.execute('''
            UPDATE contacts
            SET name = ?, phone = ?, email = ?
            WHERE name = ?
        ''', (new_name, new_phone, new_email, old_name))
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle unique constraint violation
        print("Error: Contact with this information already exists.")
    conn.close()

def delete_contact(name,phone,email):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
            DELETE FROM contacts where name = ? OR phone = ? OR email = ?
              ''',(name, phone, email))
    conn.commit()
    conn.close()