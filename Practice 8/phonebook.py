from connect import get_connection

conn = get_connection()
cur = conn.cursor()

def add_contact(name, phone):
    cur.execute(
    "CALL upsert_contact(CAST(%s AS text), CAST(%s AS text))",
    (name, phone)
)
    conn.commit()

def search_contact(name):
    cur.execute("SELECT * FROM search_contacts(%s)", (name,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_contact(name):
    cur.execute("CALL delete_contact(%s)", (name,))
    conn.commit()


while True:
    print("\n1 Add / Update")
    print("2 Search")
    print("3 Delete")
    print("4 Exit")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        add_contact(name, phone)

    elif choice == "2":
        name = input("Search: ")
        search_contact(name)

    elif choice == "3":
        name = input("Delete: ")
        delete_contact(name)

    elif choice == "4":
        break