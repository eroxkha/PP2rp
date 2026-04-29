import os
import sys
import io
import psycopg2
import json

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_db_connection():
    try:
        return psycopg2.connect(
            host="127.0.0.1",
            database="phonebook",
            user="postgres",
            password="erok",
            client_encoding='utf8'
        )
    except Exception as e:
        print(f"[!] Ошибка подключения: {e}")
        return None

def advanced_search():
    query = input("Введите запрос (имя или телефон): ")
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.search_contacts(%s::text)", (query,))
        results = cur.fetchall()
        if not results:
            print("Ничего не найдено.")
        else:
            print(f"\nНайдено {len(results)} записей:")
            for r in results:
                print(f"ID: {r[0]} | Имя: {r[1]} | Тел: {r[2]}")
    except Exception as e:
        print(f"[!] Ошибка поиска: {e}.")
    finally:
        conn.close()

def export_to_json():
    filename = input("Введите имя файла для экспорта: ") or "contacts.json"
    if not filename.endswith('.json'): filename += '.json'
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, phone FROM contacts")
        rows = cur.fetchall()
        data = [{"id": r[0], "name": r[1], "phone": r[2]} for r in rows]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[+] Экспорт завершен. Файл: {filename}")
    finally:
        conn.close()

def import_from_json():
    filename = input("Введите путь к JSON файлу (например, 2.json): ")
    if not os.path.exists(filename):
        print(f"[-] Файл '{filename}' не найден.")
        return
    conn = get_db_connection()
    if not conn: return
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        cur = conn.cursor()
        for c in contacts:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (c.get('name'), c.get('phone'))
            )
        conn.commit()
        print(f"[+] Успешно! Импортировано записей: {len(contacts)}")
    except Exception as e:
        print(f"[!] Ошибка импорта: {e}")
    finally:
        conn.close()

def view_paginated():
    limit = 5
    offset = 0
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        while True:
            cur.execute("SELECT id, name, phone FROM contacts ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- Страница {(offset // limit) + 1} ---")
            for r in rows:
                print(f"{r[0]}. {r[1]} | {r[2]}")
            cmd = input("\n[n] Next, [p] Prev, [q] Quit: ").lower()
            if cmd == 'n': offset += limit
            elif cmd == 'p' and offset >= limit: offset -= limit
            elif cmd == 'q': break
    finally:
        conn.close()

def main_menu():
    while True:
        print("\n" + "="*30)
        print("1. Поиск (Advanced Search)")
        print("2. Экспорт в JSON")
        print("3. Импорт из JSON")
        print("4. Просмотр с пагинацией")
        print("0. Выход")
        choice = input("\nВыберите действие: ")
        if choice == '1': advanced_search()
        elif choice == '2': export_to_json()
        elif choice == '3': import_from_json()
        elif choice == '4': view_paginated()
        elif choice == '0': break

if __name__ == "__main__":
    main_menu()