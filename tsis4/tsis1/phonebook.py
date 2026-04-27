import json
from connect import get_connection

def view_contacts():
    limit = 5
    offset = 0
    sort_by = "name"
    filter_group = None
    search_email = None

    while True:
        conn = get_connection()
        cur = conn.cursor()

        # Построение динамического SQL запроса
        query = """
            SELECT c.id, c.name, c.email, c.birthday, g.name 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id 
            WHERE 1=1
        """
        params = []

        if filter_group:
            query += " AND g.name ILIKE %s"
            params.append(filter_group)
        
        if search_email:
            query += " AND c.email ILIKE %s"
            params.append(f"%{search_email}%")

        # Явно указываем алиас c. для сортировки, чтобы избежать AmbiguousColumn
        actual_sort = f"c.{sort_by}" if sort_by in ['name', 'birthday', 'id'] else "c.name"
        
        query += f" ORDER BY {actual_sort} LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cur.execute(query, tuple(params))
        rows = cur.fetchall()  # ОБЯЗАТЕЛЬНО обновляем список строк здесь
        
        print(f"\n--- Контакты (Сортировка: {sort_by}, Фильтр: {filter_group or 'Нет'}) ---")
        if not rows:
            print("Контакты не найдены.")
        else:
            for r in rows:
                print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | BD: {r[3]} | Group: {r[4]}")

        print("\nКоманды: [n]ext, [p]rev, [s]ort, [f]ilter, [e]mail_search, [r]eset, [q]uit")
        cmd = input("Введите команду: ").lower()

        if cmd == 'n':
            offset += limit
        elif cmd == 'p':
            offset = max(0, offset - limit)
        elif cmd == 's':
            choice = input("Сортировать по (name/birthday/id): ").strip()
            if choice in ['name', 'birthday', 'id']:
                sort_by = choice
                offset = 0
        elif cmd == 'f':
            filter_group = input("Введите название группы: ").strip()
            offset = 0
        elif cmd == 'e':
            search_email = input("Введите часть email: ").strip()
            offset = 0
        elif cmd == 'r':
            filter_group, search_email, offset = None, None, 0
        elif cmd == 'q':
            break
        
        cur.close()
        conn.close()

# 3.3.1 Экспорт в JSON
def export_to_json(filename="contacts.json"):
    conn = get_connection()

if __name__ == "__main__":
    # Сначала можно вызвать импорт, если база пустая (раскомментируй при необходимости)
    # import_from_json("contacts.json") 
    
    # Основной запуск интерфейса
    view_contacts()