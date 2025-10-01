import tkinter as tk
from tkinter import messagebox
from auth import signup, login

def do_signup():
    ok, msg = signup(entry_user.get(), entry_pass.get())
    if ok:
        messagebox.showinfo("Sign-Up", msg)
    else:
        messagebox.showerror("Sign-Up", msg)

def do_login():
    ok, msg = login(entry_user.get(), entry_pass.get())
    if ok:
        messagebox.showinfo("Login", msg)
    else:
        messagebox.showerror("Login", msg)

root = tk.Tk()
root.title("Barangay E-Service")
root.geometry("300x200")

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Sign-Up", command=do_signup).pack(pady=5)
tk.Button(root, text="Login", command=do_login).pack(pady=5)

root.mainloop()
