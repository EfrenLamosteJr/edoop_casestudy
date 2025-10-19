# Log_In_GUI
import tkinter as tk
from tkinter import ttk, messagebox
from auth import login
from PIL import Image, ImageTk
import requests
from io import BytesIO

def open_admin_login(current_window):
    """Closes the current window and opens the admin login window."""
    print("Switching to Admin Login...")
    current_window.destroy()
    # ADMIN GUI
    from Admin_Log_In_GUI import start_admin_login
    start_admin_login()


def start_login1():
    root = tk.Tk()
    # --- MODIFICATION: Added title for the standard window bar ---
    root.title("P2SERVE Log In")

    # --- MODIFICATION: Removed root.overrideredirect(True) ---

    root.geometry("700x400")
    root.configure(bg="#2b2b2b")

    # --- Center window ---
    root.update_idletasks()
    width, height = 700, 400
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # --- MODIFICATION: Removed draggable window logic ---

    # --- Frames ---
    container = tk.Frame(root, bg="white")
    container.place(relwidth=1, relheight=1)

    left_frame = tk.Frame(container, bg="#3498db", width=250)
    left_frame.pack(side="left", fill="y")

    def load_image_from_url(url, size=None):
        try:
            response = requests.get(url)
            response.raise_for_status()  # will throw error if request failed
            img_data = BytesIO(response.content)
            pil_img = Image.open(img_data)
            if size:  # optional resize
                pil_img = pil_img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print("❌ Error loading image:", e)
            return None

    logo_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/P2SERVE_LOGO.png"
    logo_img = load_image_from_url(logo_url)
    logo_lbl = tk.Label(left_frame, image=logo_img, bg="#3498db")
    logo_lbl.image = logo_img
    logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

    right_frame = tk.Frame(container, bg="white")
    right_frame.pack(side="right", fill="both", expand=True)

    # --- MODIFICATION: Removed custom minimize and close buttons ---

    # --- ADMIN ICON BUTTON ---
    admin_btn = tk.Button(
        right_frame,
        text="⚙️",  # Gear emoji as an icon
        bg="white",
        fg="black",
        bd=0,
        font=("Segoe UI Emoji", 16),  # Font that supports emojis
        activebackground="#e0e0e0",
        cursor="hand2",
        command=lambda: open_admin_login(root)  # Calls the new function
    )
    admin_btn.place(x=10, y=5)  # Position in the top-left corner

    # --- TITLE OF THE WINDOWS FORM ---
    title = tk.Label(right_frame, text="P2SERVE LOG IN", bg="white", fg="black", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 10))

    # --- ENTRY / TEXTBOXES ---
    style = ttk.Style()
    style.configure("Rounded.TEntry", borderwidth=0, relief="flat", padding=6, font=("Arial", 10))
    align_frame = tk.Frame(right_frame, bg="white")
    align_frame.pack(anchor="center", padx=40)

    # --- Username ---
    tk.Label(align_frame, text="Username or Email", bg="white", fg="black", anchor="w").pack(fill="x", pady=(10, 0))
    l_username = ttk.Entry(align_frame, style="Rounded.TEntry", width=40)
    l_username.pack(pady=(0, 10))

    # --- Password ---
    tk.Label(align_frame, text="Password", bg="white", fg="black", anchor="w").pack(fill="x", pady=(10, 0))
    l_password = ttk.Entry(align_frame, style="Rounded.TEntry", show="*", width=40)
    l_password.pack(pady=(0, 10))

    view_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/view.png"
    hide_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/hide.png"

    # --- Eye icon toggle ---
    view_img = load_image_from_url(view_url, size=(20, 20))
    hide_img = load_image_from_url(hide_url, size=(20, 20))
    eye_label = tk.Label(align_frame, image=view_img, bg="white", cursor="hand2")
    eye_label.place(in_=l_password, relx=1.0, x=-2, rely=0.5, anchor="e")

    def toggle_password():
        if l_password.cget("show") == "*":
            l_password.config(show="")
            eye_label.config(image=hide_img)
            eye_label.image = hide_img
        else:
            l_password.config(show="*")
            eye_label.config(image=view_img)
            eye_label.image = view_img

    eye_label.bind("<Button-1>", lambda e: toggle_password())

    # --- Forgot Password ---
    forgotpass_label = tk.Label(align_frame, text="Forgot Password?", fg="#3498db", bg="white", cursor="hand2")
    forgotpass_label.pack(anchor="e")

    def forgot_on_enter(e):
        forgotpass_label.config(fg="#3b6ed5")

    def forgot_on_leave(e):
        forgotpass_label.config(fg="#3498db")

    def forgot_on_click(e):
        root.destroy()
        from Reset_password_GUI import start_resetpass
        start_resetpass()

    forgotpass_label.bind("<Enter>", forgot_on_enter)
    forgotpass_label.bind("<Leave>", forgot_on_leave)
    forgotpass_label.bind("<Button-1>", forgot_on_click)

    # --- Sign in button ---
    signin_btn = tk.Button(right_frame, text="Sign in", bg="#007BFF", fg="white", font=("Arial", 10, "bold"),
                           relief="flat", width=30, height=2, activebackground="#0056d6", cursor="hand2",
                           command=lambda: do_login(l_username.get(), l_password.get(), root))
    signin_btn.pack(pady=(20, 10))
    signin_btn.configure(highlightthickness=0, bd=0)

    # --- Bottom labels ---
    signup_label = tk.Label(right_frame, text="Don’t have an account?", bg="white", fg="#5DA7FF", cursor="hand2")
    signup_label.pack()

    def signup_on_enter(e):
        signup_label.config(fg="#3b6ed5")

    def signup_on_leave(e):
        signup_label.config(fg="#5F97FE")

    def signup_on_click(e):
        root.destroy()
        from Register_GUI import start_signup1
        start_signup1()

    signup_label.bind("<Enter>", signup_on_enter)
    signup_label.bind("<Leave>", signup_on_leave)
    signup_label.bind("<Button-1>", signup_on_click)

    tk.Label(right_frame, text="BARANGAY POBLACION II © 2025", bg="white", fg="gray").pack(side="bottom", pady=10)

    root.mainloop()


def do_login(log_user, log_pass, window):
    if log_user.strip() and log_pass.strip():
        if len(log_user) >= 5 and len(log_pass) >= 5:
            ok, msg = login(log_user, log_pass)
            if ok:
                messagebox.showinfo("Login", msg)
                window.destroy()
                from Main_page_GUI import start_mainhomepage, get_current_user_data
                start_mainhomepage(log_user)
            else:
                messagebox.showerror("Login", msg)
        else:
            messagebox.showerror("Error", "Please enter username and password.")
    else:
        messagebox.showerror("Error", "All fields are required. Please enter username and password.")