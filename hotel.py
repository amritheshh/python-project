import sqlite3
from datetime import date

conn = sqlite3.connect("hotel.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT NOT NULL UNIQUE,
        room_type TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmed',
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    )
""")

cursor.execute(
    "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
    ("manager", "manager123", "manager")
)


rooms = [
    ("101", "Normal", 2000),
    ("102", "Normal", 2000),
    ("103", "Normal", 2000),
    ("104", "Normal", 2000),
    ("105", "Normal", 2000),
    ("201", "Suite", 5000),
    ("202", "Suite", 5000),
    ("203", "Suite", 5000),
    ("204", "Suite", 5000),
    ("205", "Suite", 5000)
]

cursor.executemany('''INSERT OR IGNORE INTO rooms (room_number, room_type, price) 
    VALUES (?, ?, ?)''',(rooms))
conn.commit()


def register(conn):
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    try:
        conn.execute(
            "INSERT INTO users (username, password, role) "
            "VALUES (?, ?, ?)",
            (username, password, "customer")
        )
        conn.commit()
        print("User registration successful.")

    except sqlite3.IntegrityError:
        print("That username is already being used.")


def login(conn):
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    cursor = conn.execute(
        '''SELECT user_id, username, role FROM users WHERE username = ? AND password = ?''',
        (username, password) )

    user = cursor.fetchone()

    if user is None:
        print("Invalid username or password.")
        return None

    return user


def room_det(conn):
    cursor = conn.execute(
        "SELECT room_id, room_number, room_type, price "
        "FROM rooms ORDER BY room_number"
    )
    rooms = cursor.fetchall()

    print("\nAll rooms")

    if not rooms:
        print("There are no rooms.")
        return

    for room in rooms:
        print(
            f"ID: {room[0]} | Room: {room[1]} | "
            f"Type: {room[2]} | Price per night: {room[3]:.2f}"
        )


def get_dates():
    try:
        check_in = date.fromisoformat(
            input("Check-in date (YYYY-MM-DD): ").strip()
        )
        check_out = date.fromisoformat(
            input("Check-out date (YYYY-MM-DD): ").strip()
        )

        if check_out <= check_in:
            print("Check-out must be after check-in.")
            return None, None

        return check_in.isoformat(), check_out.isoformat()

    except ValueError:
        print("Enter dates in YYYY-MM-DD format.")
        return None, None


def get_available_rooms(conn, check_in, check_out):
    cursor = conn.execute("""
        SELECT room_id, room_number, room_type, price
        FROM rooms
        WHERE room_id NOT IN (
            SELECT room_id
            FROM bookings
            WHERE status = 'Confirmed'
              AND check_in < ?
              AND check_out > ?
        )
        ORDER BY room_number
    """, (check_out, check_in))

    return cursor.fetchall()


def show_available_rooms(conn):
    print("\nEnter dates to check availability")
    check_in, check_out = get_dates()

    if check_in is None:
        return

    rooms = get_available_rooms(conn, check_in, check_out)

    print("\nAvailable rooms")
    if not rooms:
        print("No rooms are available for those dates.")
        return

    for room in rooms:
        print(
            f"ID: {room[0]} | Room: {room[1]} | "
            f"Type: {room[2]} | Price per night: {room[3]:.2f}"
        )


def add_room(conn):
    print("\nAdd a room")
    room_number = input("Room number: ").strip()
    room_type = input("Room type: ").strip()

    try:
        price = float(input("Price per night: "))
        if price <= 0:
            print("Price must be greater than zero.")
            return
    except ValueError:
        print("Enter a valid price.")
        return

    try:
        conn.execute(
            "INSERT INTO rooms (room_number, room_type, price) "
            "VALUES (?, ?, ?)",
            (room_number, room_type, price)
        )
        conn.commit()
        print("Room added.")

    except sqlite3.IntegrityError:
        print("That room number already exists.")


def update_room(conn):
    try:
        room_id = int(input("Enter the room ID to edit: "))
    except ValueError:
        print("Enter a valid room ID.")
        return

    cursor = conn.execute(
        "SELECT room_id FROM rooms WHERE room_id = ?",
        (room_id,)
    )

    if cursor.fetchone() is None:
        print("No room has that ID.")
        return

    room_number = input("Enter the new room number: ").strip()
    room_type = input("Enter the new room type: ").strip()

    try:
        price = float(input("Enter the new price per night: "))
        if price <= 0:
            print("Price must be greater than zero.")
            return
    except ValueError:
        print("Enter a valid price.")
        return

    try:
        conn.execute(
            "UPDATE rooms SET room_number = ?, room_type = ?, price = ? "
            "WHERE room_id = ?",
            (room_number, room_type, price, room_id)
        )
        conn.commit()
        print("Room updated.")

    except sqlite3.IntegrityError:
        print("That room number is already being used.")


def delete_room(conn):
    room_det(conn)

    try:
        room_id = int(input("\nEnter the room ID to delete: "))
    except ValueError:
        print("Enter a valid room ID.")
        return

    try:
        cursor = conn.execute(
            "DELETE FROM rooms WHERE room_id = ?",
            (room_id,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            print("No room has that ID.")
        else:
            print("Room deleted.")

    except sqlite3.IntegrityError:
        print("This room has a booking, so it cannot be deleted.")


def book_room(conn, user_id):
    print("\nEnter the dates for your stay")
    check_in, check_out = get_dates()

    if check_in is None:
        return

    rooms = get_available_rooms(conn, check_in, check_out)

    if not rooms:
        print("No rooms are available for those dates.")
        return

    print("\nAvailable rooms")
    for room in rooms:
        print(
            f"ID: {room[0]} | Room: {room[1]} | "
            f"Type: {room[2]} | Price per night: {room[3]:.2f}"
        )

    try:
        room_id = int(input("Enter the ID of the room to book: "))
    except ValueError:
        print("Enter a valid room ID.")
        return

    available_room_ids = [room[0] for room in rooms]

    if room_id not in available_room_ids:
        print("Choose an ID from the available rooms.")
        return

    conn.execute(
        "INSERT INTO bookings (user_id, room_id, check_in, check_out) "
        "VALUES (?, ?, ?, ?)",
        (user_id, room_id, check_in, check_out)
    )
    conn.commit()
    print("Room booked successfully.")


def show_customer_bookings(conn, user_id):
    cursor = conn.execute("""
        SELECT bookings.booking_id, rooms.room_number,
               bookings.check_in, bookings.check_out, bookings.status
        FROM bookings
        JOIN rooms ON bookings.room_id = rooms.room_id
        WHERE bookings.user_id = ?
        ORDER BY bookings.check_in
    """, (user_id,))

    bookings = cursor.fetchall()

    print("\nYour bookings")
    if not bookings:
        print("You have no bookings.")
        return

    for booking in bookings:
        print(
            f"Booking ID: {booking[0]} | Room: {booking[1]} | "
            f"{booking[2]} to {booking[3]} | Status: {booking[4]}"
        )


def cancel_customer_booking(conn, user_id):
    show_customer_bookings(conn, user_id)

    try:
        booking_id = int(input("Enter the booking ID to cancel: "))
    except ValueError:
        print("Enter a valid booking ID.")
        return

    cursor = conn.execute("""
        UPDATE bookings
        SET status = 'Cancelled'
        WHERE booking_id = ?
          AND user_id = ?
          AND status = 'Confirmed'
    """, (booking_id, user_id))

    conn.commit()

    if cursor.rowcount == 0:
        print("No active booking with that ID was found.")
    else:
        print("Booking cancelled.")


def show_all_bookings(conn):
    cursor = conn.execute("""
        SELECT bookings.booking_id, users.username, rooms.room_number,
               bookings.check_in, bookings.check_out, bookings.status
        FROM bookings
        JOIN users ON bookings.user_id = users.user_id
        JOIN rooms ON bookings.room_id = rooms.room_id
        ORDER BY bookings.check_in
    """)

    bookings = cursor.fetchall()

    print("\nAll bookings")
    if not bookings:
        print("There are no bookings.")
        return

    for booking in bookings:
        print(
            f"Booking ID: {booking[0]} | Customer: {booking[1]} | "
            f"Room: {booking[2]} | {booking[3]} to {booking[4]} | "
            f"Status: {booking[5]}"
        )


def cancel_booking_as_manager(conn):
    show_all_bookings(conn)

    try:
        booking_id = int(input("Enter the booking ID to cancel: "))
    except ValueError:
        print("Enter a valid booking ID.")
        return

    cursor = conn.execute("""
        UPDATE bookings
        SET status = 'Cancelled'
        WHERE booking_id = ? AND status = 'Confirmed'
    """, (booking_id,))

    conn.commit()

    if cursor.rowcount == 0:
        print("No active booking with that ID was found.")
    else:
        print("Booking cancelled.")


def customer_menu(conn, user):
    user_id, username, role = user

    while True:
        print(f"\nCustomer menu - {username}")
        print("1. Check rooms and make a booking")
        print("2. View my bookings")
        print("3. Cancel my booking")
        print("4. Log out")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            book_room(conn, user_id)
        elif choice == "2":
            show_customer_bookings(conn, user_id)
        elif choice == "3":
            cancel_customer_booking(conn, user_id)
        elif choice == "4":
            break
        else:
            print("Choose an option from 1 to 4.")


def manager_menu(conn, user):
    while True:
        print(f"\nManager menu - {user[1]}")
        print("1. Check available rooms for dates")
        print("2. View all rooms")
        print("3. Add a room")
        print("4. Edit a room")
        print("5. Delete a room")
        print("6. View all bookings")
        print("7. Cancel a booking")
        print("8. Log out")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_available_rooms(conn)
        elif choice == "2":
            room_det(conn)
        elif choice == "3":
            add_room(conn)
        elif choice == "4":
            update_room(conn)
        elif choice == "5":
            delete_room(conn)
        elif choice == "6":
            show_all_bookings(conn)
        elif choice == "7":
            cancel_booking_as_manager(conn)
        elif choice == "8":
            break
        else:
            print("Choose an option from 1 to 8.")


def main():
    print("Welcome to the Hotel Management System")
    while True:
        print("\nMain menu")
        print("1. Register as a customer")
        print("2. Log in")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register(conn)

        elif choice == "2":
            user = login(conn)

            if user is None:
                print("Login failed.")
            elif user[2] == "manager":
                manager_menu(conn, user)
            else:
                customer_menu(conn, user)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Choose 1, 2, or 3.")


try:
    main()
except sqlite3.Error as error:
    print("A database error occurred:", error)
finally:
    conn.close()