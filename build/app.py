import tkinter as tk
from tkinter import messagebox
from auth import signup, login


# ---------- Helper Functions ----------
def draw_gradient(canvas, width, height, color1, color2):
    """Draw a vertical gradient on the canvas."""
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = float(r2 - r1) / height
    g_ratio = float(g2 - g1) / height
    b_ratio = float(b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr >> 8:02x}{ng >> 8:02x}{nb >> 8:02x}"
        canvas.create_line(0, i, width, i, fill=color)


def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Draw a rounded rectangle on a Tkinter canvas."""
    points = [
        (x1+radius, y1),
        (x2-radius, y1),
        (x2, y1),
        (x2, y1+radius),
        (x2, y2-radius),
        (x2, y2),
        (x2-radius, y2),
        (x1+radius, y2),
        (x1, y2),
        (x1, y2-radius),
        (x1, y1+radius),
        (x1, y1),
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def add_placeholder(entry, placeholder, is_password=False):
    """Add placeholder text inside an Entry widget."""
    entry.insert(0, placeholder)
    entry.config(fg="grey")

    def on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# ---------- Login Window ----------
def open_login():
    window = tk.Tk()
    window.geometry("1000x600")
    window.title("Login")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=1000, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Gradient background
    draw_gradient(canvas, 1000, 600, "#CFFFE2", "#FFE1E1")

    # Card shadow + container
    create_rounded_rect(canvas, 305, 125, 705, 425, radius=20, fill="#bfbfbf", outline="")
    create_rounded_rect(canvas, 300, 120, 700, 420, radius=20, fill="#FFFFFF", outline="")

    # Title
    canvas.create_text(500, 150, text="Login", font=("Arial", 24, "bold"), fill="black")

    # Username
    canvas.create_text(330, 190, text="Username", anchor="w", font=("Arial", 12), fill="black")
    create_rounded_rect(canvas, 325, 215, 675, 255, radius=15, fill="#DDDDDD", outline="")
    username_login = tk.Entry(window, bd=0, bg="#DDDDDD", fg="black", font=("Arial", 12))
    canvas.create_window(330, 220, anchor="nw", width=340, height=30, window=username_login)
    add_placeholder(username_login, "Enter Username")

    # Password
    canvas.create_text(330, 265, text="Password", anchor="w", font=("Arial", 12), fill="black")
    create_rounded_rect(canvas, 325, 285, 675, 325, radius=15, fill="#DDDDDD", outline="")
    password_login = tk.Entry(window, bd=0, bg="#DDDDDD", fg="black", font=("Arial", 12))
    canvas.create_window(330, 290, anchor="nw", width=340, height=30, window=password_login)
    add_placeholder(password_login, "Enter Password", is_password=True)

    # Login Button
    create_rounded_rect(canvas, 330, 350, 450, 390, radius=15, fill="#5F97FE", outline="")
    login_btn = tk.Button(window, text="Login", bg="#5F97FE", fg="white",
                          font=("Arial", 12, "bold"), bd=0, relief="flat", command=lambda: do_login(username_login.get(), password_login.get())) ######
    canvas.create_window(330, 355, anchor="nw", width=120, height=30, window=login_btn)

    # Link to Sign Up
    link_label = tk.Label(window, text="Don’t have an account?",
                          font=("Arial", 11, "underline"), fg="#5F97FE", bg="#FFFFFF", cursor="hand2")
    canvas.create_window(470, 360, anchor="nw", window=link_label)

    def on_enter(e): link_label.config(fg="#3b6ed5")
    def on_leave(e): link_label.config(fg="#5F97FE")
    def on_click(e):
        window.destroy()
        open_signup()

    link_label.bind("<Enter>", on_enter)
    link_label.bind("<Leave>", on_leave)
    link_label.bind("<Button-1>", on_click)

    window.mainloop()



# ---------- Sign Up Window ----------
def open_signup():
    window = tk.Tk()
    window.geometry("1000x600")
    window.title("Sign Up")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=1000, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Gradient background
    draw_gradient(canvas, 1000, 600, "#CFFFE2", "#FFE1E1")

    # Card shadow + container
    create_rounded_rect(canvas, 305, 125, 705, 425, radius=20, fill="#bfbfbf", outline="")
    create_rounded_rect(canvas, 300, 120, 700, 420, radius=20, fill="#FFFFFF", outline="")

    # Title
    canvas.create_text(500, 150, text="Sign Up", font=("Arial", 24, "bold"), fill="black")

    # Username
    canvas.create_text(330, 190, text="Username", anchor="w", font=("Arial", 12), fill="black")
    create_rounded_rect(canvas, 325, 215, 675, 255, radius=15, fill="#DDDDDD", outline="")
    username_signup = tk.Entry(window, bd=0, bg="#DDDDDD", fg="black", font=("Arial", 12))
    canvas.create_window(330, 220, anchor="nw", width=340, height=30, window=username_signup)
    add_placeholder(username_signup, "Enter Username")

    # Password
    canvas.create_text(330, 265, text="Password", anchor="w", font=("Arial", 12), fill="black")
    create_rounded_rect(canvas, 325, 285, 675, 325, radius=15, fill="#DDDDDD", outline="")
    password_signup = tk.Entry(window, bd=0, bg="#DDDDDD", fg="black", font=("Arial", 12))
    canvas.create_window(330, 290, anchor="nw", width=340, height=30, window=password_signup)
    add_placeholder(password_signup, "Enter Password", is_password=True)


    # convert to text
    #signup_user: str = username_signup.get()
    #signup_pass: str = password_signup.get()

    # Sign Up Button
    create_rounded_rect(canvas, 330, 350, 450, 390, radius=15, fill="#5F97FE", outline="")
    signup_btn = tk.Button(window, text="Sign up", bg="#5F97FE", fg="white",
                           font=("Arial", 12, "bold"), bd=0, relief="flat", command=lambda: do_signup(username_signup.get(), password_signup.get()))####
    canvas.create_window(330, 355, anchor="nw", width=120, height=30, window=signup_btn)

    # Link to Login
    link_label = tk.Label(window, text="Already have an account?",
                          font=("Arial", 11, "underline"), fg="#5F97FE", bg="#FFFFFF", cursor="hand2")
    canvas.create_window(470, 360, anchor="nw", window=link_label)

    def on_enter(e): link_label.config(fg="#3b6ed5")
    def on_leave(e): link_label.config(fg="#5F97FE")
    def on_click(e):
        window.destroy()
        open_login()

    link_label.bind("<Enter>", on_enter)
    link_label.bind("<Leave>", on_leave)
    link_label.bind("<Button-1>", on_click)

    window.mainloop()




# ---------- Start App ----------
def do_signup(sign_user, sign_pass):
    ok, msg = signup(sign_user, sign_pass)
    if ok:
        messagebox.showinfo("Sign-Up", msg)
        open_login()
    else:
        messagebox.showerror("Sign-Up", msg)

def do_login(log_user, log_pass):
    ok, msg = login(log_user, log_pass)
    if ok:
        messagebox.showinfo("Login", msg)
    else:
        messagebox.showerror("Login", msg)


open_login()