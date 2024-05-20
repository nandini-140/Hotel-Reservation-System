import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta

class HotelReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation System")

        frame = tk.Frame(root, bg='pink')  
        
        frame.pack(fill=tk.BOTH, expand=True)

        self.create_database()

        self.tabControl = ttk.Notebook(root)
        self.tab_available = ttk.Frame(self.tabControl)
        self.tab_booked = ttk.Frame(self.tabControl)
        self.tab_make_reservation = ttk.Frame(self.tabControl)
        self.tab_cancel_reservation = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_available, text='Available Rooms')
        self.tabControl.add(self.tab_booked, text='Booked Rooms')
        self.tabControl.add(self.tab_make_reservation, text='Make Reservation')
        self.tabControl.add(self.tab_cancel_reservation, text='Cancel Reservation')

        self.tabControl.pack(expand=1, fill="both")

        self.create_tab_available()
        self.create_tab_booked()
        self.create_tab_make_reservation()
        self.create_tab_cancel_reservation()

    def create_database(self):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_number INTEGER PRIMARY KEY,
                capacity INTEGER,
                price_per_night REAL,
                booked BOOLEAN DEFAULT 0
            )
        ''')
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (101, 2, 1000.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (102, 4, 1500.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (103, 1, 800.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (104, 3, 1200.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (105, 4, 1500.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (106, 2, 1000.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (201, 4, 1500.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (202, 1, 800.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (203, 2, 1000.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (204, 3, 1200.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (205, 3, 1200.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (206, 1, 800.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (301, 4, 1500.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (302, 1, 800.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (303, 2, 1000.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (304, 3, 1200.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (305, 3, 1200.0)")
        # cursor.execute("INSERT INTO rooms (room_number, capacity, price_per_night) VALUES (306, 4, 1500.0)")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY,
                room_number INTEGER,
                check_in_date DATE,
                check_out_date DATE,
                FOREIGN KEY (room_number) REFERENCES rooms(room_number)
            )
        ''')

        conn.commit()
        conn.close()

    def create_tab_available(self):
        
        tree_columns = ("Room Number", "Capacity", "Price per Night")
        self.tree_available = ttk.Treeview(self.tab_available, columns=tree_columns, show="headings", height=10)
        for col in tree_columns:
            self.tree_available.heading(col, text=col)
        self.tree_available.pack(padx=20, pady=20)

        self.refresh_tab_available()

    def create_tab_booked(self):
        tree_columns = ("Reservation ID", "Room Number", "Check-in Date", "Check-out Date", "Re-book")
        self.tree_booked = ttk.Treeview(self.tab_booked, columns=tree_columns, show="headings", height=10)
        for col in tree_columns:
            self.tree_booked.heading(col, text=col)
        self.tree_booked.pack(padx=20, pady=20)

        self.refresh_tab_booked()

    def create_tab_make_reservation(self):
        tk.Label(self.tab_make_reservation, text="Room Number:").grid(row=0, column=0, pady=10)
        self.room_number_entry = tk.Entry(self.tab_make_reservation)
        self.room_number_entry.grid(row=0, column=1)

        tk.Label(self.tab_make_reservation, text="Check-in Date (YYYY-MM-DD):").grid(row=1, column=0, pady=10)
        self.check_in_date_entry = tk.Entry(self.tab_make_reservation)
        self.check_in_date_entry.grid(row=1, column=1)

        tk.Label(self.tab_make_reservation, text="Check-out Date (YYYY-MM-DD):").grid(row=2, column=0, pady=10)
        self.check_out_date_entry = tk.Entry(self.tab_make_reservation)
        self.check_out_date_entry.grid(row=2, column=1)

        tk.Button(self.tab_make_reservation, text="Make Reservation", command=self.make_reservation).grid(row=3, column=1, pady=20)

    def create_tab_cancel_reservation(self):
        tk.Label(self.tab_cancel_reservation, text="Reservation ID:").grid(row=0, column=0, pady=10)
        self.reservation_id_entry = tk.Entry(self.tab_cancel_reservation)
        self.reservation_id_entry.grid(row=0, column=1)

        tk.Button(self.tab_cancel_reservation, text="Cancel Reservation", command=self.cancel_reservation).grid(row=1, column=1, pady=20)

    def refresh_tab_available(self):
        self.tree_available.delete(*self.tree_available.get_children())

        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms WHERE booked = 0')
        available_rooms = cursor.fetchall()

        for room in available_rooms:
            self.tree_available.insert("", "end", values=room)

        conn.close()

    def refresh_tab_booked(self):
        self.tree_booked.delete(*self.tree_booked.get_children())

        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM reservations')
        booked_rooms = cursor.fetchall()

        for reservation in booked_rooms:
            row_data = reservation + (tk.Button(self.tab_booked, text="Re-book", command=lambda res=reservation: self.re_book(res)),)
            self.tree_booked.insert("", "end", values=row_data)

        conn.close()

    def make_reservation(self):
        room_number = self.room_number_entry.get()
        check_in_date = self.check_in_date_entry.get()
        check_out_date = self.check_out_date_entry.get()

        try:
            room_number = int(room_number)
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid values.")
            return

        if self.is_valid_reservation(room_number, check_in_date, check_out_date):
            self.make_reservation_db(room_number, check_in_date, check_out_date)
            self.refresh_tab_available()
            self.refresh_tab_booked()

    def is_valid_reservation(self, room_number, check_in_date, check_out_date):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms WHERE room_number = ? AND booked = 0', (room_number,))
        room = cursor.fetchone()

        conn.close()

        if not room:
            messagebox.showerror("Error", "Room not available for the selected dates.")
            return False
        else:
            return True

    def make_reservation_db(self, room_number, check_in_date, check_out_date):
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE rooms SET booked = 1 WHERE room_number = ?', (room_number,))
        cursor.execute('INSERT INTO reservations (room_number, check_in_date, check_out_date) VALUES (?, ?, ?)',
                       (room_number, check_in_date, check_out_date))

        messagebox.showinfo("Reservation Successful", "Reservation successful.")

        conn.commit()
        conn.close()

    def re_book(self, reservation):
        room_number = reservation[1]
        check_out_date = reservation[3]

        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')

        new_check_in_date = check_out_date + timedelta(days=1)
        new_check_out_date = new_check_in_date + timedelta(days=1)

        self.make_reservation_db(room_number, new_check_in_date, new_check_out_date)
        self.refresh_tab_available()
        self.refresh_tab_booked()

    def cancel_reservation(self):
        reservation_id = self.reservation_id_entry.get()

        if reservation_id:
            try:
                reservation_id = int(reservation_id)
            except ValueError:
                messagebox.showerror("Error", "Invalid Reservation ID. Please enter a valid numeric ID.")
                return

            conn = sqlite3.connect('hotel.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM reservations WHERE reservation_id = ?', (reservation_id,))
            existing_reservation = cursor.fetchone()

            if existing_reservation:
                room_number = existing_reservation[1]

                cursor.execute('UPDATE reservations SET check_out_date = ? WHERE reservation_id = ?',
                               (datetime.now().strftime('%Y-%m-%d'), reservation_id))
                cursor.execute('UPDATE rooms SET booked = 0 WHERE room_number = ?', (room_number,))

                for child in self.tree_booked.get_children():
                    if self.tree_booked.item(child, 'values')[0] == reservation_id:
                        self.tree_booked.delete(child)


                messagebox.showinfo("Reservation Canceled", "Reservation canceled successfully. Room is now available.")
                self.refresh_tab_booked()
                self.refresh_tab_available()
            else:
                messagebox.showerror("Error", f"Reservation with ID {reservation_id} not found.")

            conn.commit()
            conn.close()
        else:
            messagebox.showerror("Error", "Please enter a Reservation ID.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelReservationApp(root)
    root.mainloop()
