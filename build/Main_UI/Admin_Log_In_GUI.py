# Admin_Log_In_GUI.py
import tkinter as tk
from tkinter import ttk, messagebox


def go_to_resident_login(current_window):
    """Closes the admin login and opens the resident login window."""
    print("Switching back to Resident Login...")
    current_window.destroy()
    from Log_In_GUI import start_login1
    start_login1()


def start_admin_login():
    root = tk.Tk()
    # --- MODIFICATION: Added title for the standard window bar ---
    root.title("P2SERVE Admin Log In")

    # --- MODIFICATION: Removed root.overrideredirect(True) ---

    root.geometry("700x400")

    # --- Center the window on the screen ---
    root.update_idletasks()
    width, height = 700, 400
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # --- MODIFICATION: Removed draggable window logic ---

    # --- Main container frame ---
    container = tk.Frame(root, bg="white")
    container.place(relwidth=1, relheight=1)

    # --- Left Sidebar Frame (Blue) ---
    left_frame = tk.Frame(container, bg="#3498db", width=250)
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(False)

    # --- Logo/Seal ---
    try:
        logo_path = r"C:\Users\Bryan\Downloads\PythonProject-20251015T135346Z-1-001\PythonProject\build\Image_Resources\P2SERVE_LOGO.png"
        logo_img = tk.PhotoImage(file=logo_path)
        logo_lbl = tk.Label(left_frame, image=logo_img, bg="#3498db")
        logo_lbl.image = logo_img  # Keep a reference
        logo_lbl.pack(expand=True)
    except tk.TclError:
        logo_lbl = tk.Label(left_frame, text="[BARANGAY SEAL]", bg="#3498db", fg="white", font=("Arial", 14, "bold"))
        logo_lbl.pack(expand=True)

    # --- Right Login Form Frame (White) ---
    right_frame = tk.Frame(container, bg="white")
    right_frame.pack(side="right", fill="both", expand=True)

    # --- MODIFICATION: Removed custom window control buttons ---

    # --- "Go Back" Icon ---
    resident_btn = tk.Button(
        right_frame, text="👤", bg="white", fg="black", bd=0,
        font=("Segoe UI Emoji", 16), activebackground="#e0e0e0", cursor="hand2",
        command=lambda: go_to_resident_login(root)
    )
    resident_btn.place(x=10, y=10)  # Position in top-left corner

    # --- Login Form Content ---
    title = tk.Label(right_frame, text="P2SERVE ADMIN LOG IN", bg="white", fg="black", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 15))

    align_frame = tk.Frame(right_frame, bg="white")
    align_frame.pack(pady=5)

    style = ttk.Style()
    style.configure("TEntry", borderwidth=1, relief="solid", padding=8, font=("Arial", 11))
    style.map("TEntry", bordercolor=[('focus', '#3498db')])

    tk.Label(align_frame, text="Username or Email", bg="white", fg="black", font=("Arial", 10)).pack(anchor="w")
    username_entry = ttk.Entry(align_frame, width=40)
    username_entry.pack(pady=(5, 10))

    tk.Label(align_frame, text="Password", bg="white", fg="black", font=("Arial", 10)).pack(anchor="w")
    password_entry = ttk.Entry(align_frame, show="*", width=40)
    password_entry.pack(pady=(5, 5))

    eye_label = tk.Label(align_frame, text="👁️", bg="white", font=("Segoe UI Emoji", 10), cursor="hand2")
    eye_label.place(in_=password_entry, relx=1.0, x=-25, rely=0.5, anchor="center")

    def toggle_password():
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    eye_label.bind("<Button-1>", lambda e: toggle_password())

    forgot_label = tk.Label(align_frame, text="Forgot Password?", bg="white", fg="#007BFF", font=("Arial", 9),
                            cursor="hand2")
    forgot_label.pack(anchor="e", pady=(0, 5))

    def admin_login_logic():
        user = username_entry.get()
        pwd = password_entry.get()
        if user == "admin" and pwd == "password":  # Placeholder logic
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            root.destroy()
            from Admin_Dashboard_GUI import start_admin_dashboard
            start_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    signin_btn = tk.Button(right_frame, text="Sign in", bg="#007BFF", fg="white", font=("Arial", 12, "bold"),
                           relief="flat", width=25, height=2, activebackground="#0056d6", cursor="hand2",
                           command=admin_login_logic)
    signin_btn.pack(pady=15)
    signin_btn.configure(highlightthickness=0, bd=0)

    # --- COPYRIGHT FOOTER ---
    tk.Label(right_frame, text="BARANGAY POBLACION II © 2025",
             bg="white", fg="gray").pack(side="bottom", pady=10)

    root.mainloop()


# --- To run this file directly for testing ---
if __name__ == "__main__":
    start_admin_login()