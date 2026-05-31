import sqlite3
from datetime import datetime

# Підключаємось до бази даних (створюється якщо немає)
conn = sqlite3.connect("finances.db")

# Створюємо таблицю якщо ще не існує
conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        amount   REAL NOT NULL,
        category TEXT NOT NULL,
        note     TEXT,
        date     TEXT NOT NULL
    )
""")
conn.commit()


def add_transaction():
    try:
        # Зчитуємо суму від користувача
        amount = float(input("Сума (- витрата, + прибуток): "))
        if amount == 0:
            return print("Сума не може бути 0")

        category = input("Категорія: ").strip() or "Інше"  # якщо порожньо — "Інше"
        note = input("Примітка: ").strip()
        date = datetime.now().strftime("%Y-%m-%d")  # сьогоднішня дата

        # Зберігаємо запис у базу, ? захищає від помилок введення
        conn.execute(
            "INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?)",
            (amount, category, note, date)
        )
        conn.commit()
        print("✓ Збережено")

    except ValueError:
        print("Помилка: введи число")


def show_summary():
    # Отримуємо всі суми і категорії з бази
    rows = conn.execute("SELECT amount, category FROM transactions").fetchall()
    if not rows:
        return print("Записів ще немає")

    total = sum(a for a, _ in rows)  # рахуємо загальний баланс

    # Підраховуємо суму по кожній категорії
    cats = {}
    for amount, category in rows:
        cats[category] = cats.get(category, 0) + amount

    print(f"\nБаланс: {total:+.2f} грн")
    for category, amount in cats.items():
        print(f"  {category}: {amount:+.2f} грн")


def show_transactions():
    # Отримуємо всі транзакції, найновіші спочатку
    rows = conn.execute(
        "SELECT amount, category, note, date FROM transactions ORDER BY id DESC"
    ).fetchall()
    if not rows:
        return print("Немає транзакцій")

    # Виводимо таблицю з вирівнюванням
    print(f"\n{'Сума':>10}  {'Категорія':<15}  {'Примітка':<20}  Дата")
    print("-" * 65)
    for amount, category, note, date in rows:
        print(f"{amount:>+10.2f}  {category:<15}  {note:<20}  {date}")


# Словник: цифра меню → функція яку викликати
MENU = {
    "1": add_transaction,
    "2": show_summary,
    "3": show_transactions,
}

# Головний цикл програми
while True:
    print("\n=== Трекер фінансів ===")
    print("1. Додати транзакцію")
    print("2. Зведення")
    print("3. Всі транзакції")
    print("0. Вийти")

    choice = input("Вибір: ").strip()

    if choice == "0":
        conn.close()  # закриваємо базу перед виходом
        print("До побачення!")
        break
    elif choice in MENU:
        MENU[choice]()  # викликаємо потрібну функцію
    else:
        print("Невідомий пункт")
