import mysql.connector as sql
from argon2 import PasswordHasher, exceptions
import tkinter as tk
from tkinter import messagebox


conn = sql.connect(
    host='localhost',
    user='root',
    passwd='Shrey@505',
    database='Passwords'
)
c = conn.cursor()
ph = PasswordHasher()


root = tk.Tk()
root.title("User Login System")
root.geometry("350x300")


def add_user():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        hashed = ph.hash(password)
        try:
            c.execute("INSERT INTO pass (username, password) VALUES (%s, %s)", (username, hashed))
            conn.commit()
            messagebox.showinfo("Success", "User added successfully.")
        except sql.Error as e:
            messagebox.showerror("Database Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")


def login_user():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        c.execute("SELECT password FROM pass WHERE username = %s", (username,))
        result = c.fetchone()
        if result:
            try:
                if ph.verify(result[0], password):
                    messagebox.showinfo("Login", "Login successful.")
                else:
                    messagebox.showerror("Login Failed", "Incorrect password.")
            except exceptions.VerifyMismatchError:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "User not found.")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")


def clear_fields():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)


tk.Label(root, text="Username").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login_user, width=20).pack(pady=5)
tk.Button(root, text="Add User", command=add_user, width=20).pack(pady=5)
tk.Button(root, text="Clear Fields", command=clear_fields, width=20).pack(pady=5)

tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", width=20).pack(pady=15)


root.mainloop()
