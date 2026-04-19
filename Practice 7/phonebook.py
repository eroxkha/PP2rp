from connect import get_connection

conn = get_connection()



def add_contact(name, phone):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()

def search_contact(name):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM contacts WHERE name ILIKE %s",
        (f"%{name}%",)
    )
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()



def update_contact(name, phone):
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (phone, name)
    )
    conn.commit()
    cur.close()


def delete_contact(name):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM contacts WHERE name=%s",
        (name,)
    )
    conn.commit()
    cur.close()

while True:
    
    print("\n1 Add")
    print("2 Search")
    print("3 Update")
    print("4 Delete")
    print("5 Exit")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        add_contact(name, phone)

    elif choice == "2":
        name = input("Search: ")
        search_contact(name)

    elif choice == "3":
        name = input("Name: ")
        phone = input("New phone: ")
        update_contact(name, phone)

    elif choice == "4":
        name = input("Name: ")
        delete_contact(name)

    elif choice == "5":
        break
import csv

def import_csv():
    cur = conn.cursor()

    with open("contacts.csv", newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                row
            )

    conn.commit()
    cur.close()
    print("CSV imported successfully")