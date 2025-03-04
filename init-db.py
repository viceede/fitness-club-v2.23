import sqlite3

def create_database():
    # Подключение к SQLite или создание базы данных, если она отсутствует
    conn = sqlite3.connect("fitness_club.db")
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        membership_type TEXT NOT NULL,
        registration_date DATE NOT NULL,
        status TEXT DEFAULT 'active'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS administrators (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        hire_date DATE NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        shift_schedule TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS managers (
        manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        position TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        document_id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type TEXT NOT NULL,
        creation_date DATE NOT NULL,
        related_entity TEXT NOT NULL,
        status TEXT DEFAULT 'in_progress',
        file_path TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_processes (
        process_id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_name TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        status TEXT DEFAULT 'in_progress',
        responsible_admin INTEGER,
        FOREIGN KEY (responsible_admin) REFERENCES administrators(admin_id) ON DELETE SET NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        payment_date DATE NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT DEFAULT 'completed',
        FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
    );
    """)

    # Добавление начальных данных
    cursor.executemany("""
    INSERT INTO clients (first_name, last_name, date_of_birth, phone_number, email, membership_type, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, [
        ('Иван', 'Иванов', '1980-01-01', '+79991234567', 'ivanov@example.com', 'annual', '2023-10-10'),
        ('Анна', 'Смирнова', '1985-05-15', '+79997654321', 'smirnova@example.com', 'monthly', '2023-11-15')
    ])

    cursor.executemany("""
    INSERT INTO administrators (first_name, last_name, hire_date, phone_number, email, shift_schedule) VALUES (?, ?, ?, ?, ?, ?);
    """, [
        ('Алексей', 'Петров', '2020-02-15', '+79993334455', 'petrov@example.com', '2/2'),
        ('Мария', 'Кузнецова', '2021-05-01', '+79996667788', 'kuznetsova@example.com', '5/2')
    ])

    cursor.executemany("""
    INSERT INTO managers (first_name, last_name, position, phone_number, email) VALUES (?, ?, ?, ?, ?);
    """, [
        ('Сергей', 'Орлов', 'Head of Sales', '+79999990011', 'orlov@example.com'),
        ('Ольга', 'Лебедева', 'HR Manager', '+79999990022', 'lebedeva@example.com')
    ])

    cursor.executemany("""
    INSERT INTO documents (document_type, creation_date, related_entity, status, file_path) VALUES (?, ?, ?, ?, ?);
    """, [
        ('contract', '2023-12-01', 'client_1', 'signed', '/path/to/file1.pdf'),
        ('report', '2023-11-15', 'manager_1', 'in_progress', '/path/to/file2.xlsx')
    ])

    cursor.executemany("""
    INSERT INTO system_processes (process_name, start_date, end_date, status, responsible_admin) VALUES (?, ?, ?, ?, ?);
    """, [
        ('Onboarding Process', '2023-10-01', '2023-10-15', 'completed', 1),
        ('Customer Support', '2023-11-01', '2023-11-30', 'in_progress', 2)
    ])

    cursor.executemany("""
    INSERT INTO payments (client_id, payment_date, amount, payment_method, status) VALUES (?, ?, ?, ?, ?);
    """, [
        (1, '2023-10-15', 12000.00, 'bank_transfer', 'completed'),
        (2, '2023-11-20', 6000.00, 'credit_card', 'completed')
    ])

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена начальными данными!")

# Запуск скрипта
if __name__ == "__main__":
    create_database()
