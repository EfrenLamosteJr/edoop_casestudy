# Register_GUI
import customtkinter as ctk
import tkinter as tk
import re  # REQUIRED for contact number validation


def start_signup1():
    # --- App Configuration ---
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    # --- MODIFICATION: Added title for the standard window bar ---
    root.title("P2SERVE - Register")

    width, height = 800, 500
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)

    # --- MODIFICATION: Removed root.overrideredirect(True) ---
    # --- MODIFICATION: Removed custom top_frame and its buttons ---
    # --- MODIFICATION: Removed draggable window logic ---

    # --- Center window ---
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # --- MODIFICATION: Removed root.attributes('-topmost', True) ---

    # --- Left Frame (Logo Section) ---
    left_frame = ctk.CTkFrame(root, width=250, fg_color="#3498db", corner_radius=0)
    left_frame.pack(side="left", fill="y")

    try:
        logo_img = tk.PhotoImage(
            file=r"C:\Users\EfrenLamostejr\Documents\Study\Oop\build\Image_Resources\P2SERVE_LOGO.png")
        logo_lbl = tk.Label(left_frame, image=logo_img, bg="#3498db")
        logo_lbl.image = logo_img
        logo_lbl.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        logo_lbl = ctk.CTkLabel(left_frame, text="[P2SERVE Logo]", text_color="white", font=("Arial", 16))
        logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

    # --- Right Frame (Form Section) ---
    right_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
    right_frame.pack(side="right", fill="both", expand=True)

    # --- Content Frame inside Right Frame ---
    content_frame = ctk.CTkFrame(right_frame, fg_color="white")
    content_frame.place(relx=0.5, rely=0.45, anchor="center")

    # Title
    title = ctk.CTkLabel(content_frame, text="CREATE ACCOUNT", text_color="black",
                         font=("Arial", 24, "bold"))
    title.pack(pady=(0, 15))

    # --- Helper function to create a field ---
    def create_field(frame, label_text):
        field_frame = ctk.CTkFrame(frame, fg_color="white")
        field_frame.pack(side="left", padx=10, pady=5)
        label = ctk.CTkLabel(field_frame, text=label_text, text_color="black", anchor="w", font=("Arial", 11))
        label.pack(anchor="w")
        entry = ctk.CTkEntry(field_frame, width=200, height=35, corner_radius=10)
        entry.pack()
        return entry

    # Row 1: Username & Email
    row1 = ctk.CTkFrame(content_frame, fg_color="white")
    row1.pack(fill="x", pady=5)
    username_entry = create_field(row1, "Username")
    email_entry = create_field(row1, "Email")

    # Row 2: Firstname & Lastname
    row2 = ctk.CTkFrame(content_frame, fg_color="white")
    row2.pack(fill="x", pady=5)
    firstname_entry = create_field(row2, "Firstname")
    lastname_entry = create_field(row2, "Lastname")

    # Row 3: Contact No. & Address
    row3 = ctk.CTkFrame(content_frame, fg_color="white")
    row3.pack(fill="x", pady=5)
    contact_entry = create_field(row3, "Contact No.")
    address_entry = create_field(row3, "Address")

    # Row 4: Password & Confirm Password with Eye Icons
    row4 = ctk.CTkFrame(content_frame, fg_color="white")
    row4.pack(fill="x", pady=5)
    password_entry = create_field(row4, "Password")
    password_entry.configure(show="*")

    view_img = tk.PhotoImage(
        file=r"C:\Users\EfrenLamostejr\Documents\Study\Oop\build\Image_Resources\view.png")
    hide_img = tk.PhotoImage(
        file=r"C:\Users\EfrenLamostejr\Documents\Study\Oop\build\Image_Resources\hide.png")
    eye_label_password = tk.Label(row4, image=view_img, bg="white", cursor="hand2")
    eye_label_password.place(in_=password_entry, relx=1.0, x=-2, rely=0.5, anchor="e")

    def toggle_password():
        if password_entry.cget("show") == "*":
            password_entry.configure(show="")
            eye_label_password.config(image=hide_img)
        else:
            password_entry.configure(show="*")
            eye_label_password.config(image=view_img)

    eye_label_password.bind("<Button-1>", lambda e: toggle_password())

    confirm_entry = create_field(row4, "Confirm Password")
    confirm_entry.configure(show="*")

    eye_label_confirm = tk.Label(row4, image=view_img, bg="white", cursor="hand2")
    eye_label_confirm.place(in_=confirm_entry, relx=1.0, x=-2, rely=0.5, anchor="e")

    def toggle_confirm():
        if confirm_entry.cget("show") == "*":
            confirm_entry.configure(show="")
            eye_label_confirm.config(image=hide_img)
        else:
            confirm_entry.configure(show="*")
            eye_label_confirm.config(image=view_img)

    eye_label_confirm.bind("<Button-1>", lambda e: toggle_confirm())

    # --- Error Message Label ---
    error_label = ctk.CTkLabel(
        content_frame,
        text="",
        text_color="#C0392B",
        font=("Arial", 11, "bold")
    )
    error_label.pack(pady=(5, 5))

    # --- Validation Function ---
    def validate_registration():
        error_label.configure(text="")
        values = {
            "username": username_entry.get(),
            "email": email_entry.get(),
            "firstname": firstname_entry.get(),
            "lastname": lastname_entry.get(),
            "contact": contact_entry.get(),
            "address": address_entry.get(),
            "password": password_entry.get(),
            "confirm": confirm_entry.get()
        }

        field_names = {"contact": "Contact No.", "confirm": "Confirm Password"}

        for key, value in values.items():
            if not value.strip():
                display_name = field_names.get(key, key.capitalize())
                error_label.configure(text=f"Error: The {display_name} field is required.")
                return False

        email = values["email"]
        if "@" not in email or "." not in email or email.count("@") > 1:
            error_label.configure(text="Error: Please enter a valid email address.")
            return False

        contact = values["contact"]
        if not re.match(r'^09\d{9}$', contact):
            error_label.configure(text="Error: Contact No. must be 11 digits and start with 09.")
            return False

        username = values["username"]
        if not username.isalnum():
            error_label.configure(text="Error: Username must be alphanumeric.")
            return False

        password = values["password"]
        if len(password) < 8 or not any(char.isalpha() for char in password) or not any(
                char.isdigit() for char in password):
            error_label.configure(text="Error: Password must be at least 8 chars with letters and numbers.")
            return False

        if values["password"] != values["confirm"]:
            error_label.configure(text="Error: Passwords do not match.")
            return False

        do_signup(firstname_entry.get(), lastname_entry.get(), username_entry.get(), contact_entry.get(),
                  email_entry.get(), address_entry.get(), password_entry.get(), root)
        return True

    # --- Register Button Action ---
    def register_action():
        if validate_registration():
            # The do_signup function now handles navigation
            pass

    # --- Register Button ---
    register_btn = ctk.CTkButton(
        content_frame,
        text="REGISTER",
        width=420,
        height=40,
        corner_radius=20,
        fg_color="#007BFF",
        hover_color="#0056D6",
        font=("Arial", 12, "bold"),
        command=register_action
    )
    register_btn.pack(pady=(20, 5))

    # --- Login Link ---
    login_label = tk.Label(
        content_frame,
        text="Already have an account? Log in",
        fg="#5DA7FF",
        bg="white",  # Explicitly set background for tk Label
        cursor="hand2",
        font=("Arial", 10)
    )
    login_label.pack(pady=(0, 5))

    def on_enter(e):
        login_label.config(fg="#3b6ed5")

    def on_leave(e):
        login_label.config(fg="#5F97FE")

    def on_click(e):
        root.destroy()
        from Log_In_GUI import start_login1
        start_login1()

    login_label.bind("<Enter>", on_enter)
    login_label.bind("<Leave>", on_leave)
    login_label.bind("<Button-1>", on_click)

    root.mainloop()


def do_signup(firstname, lastname, username, co_number, email, b_address, password, window):
    # Simplified this function call
    window.destroy()
    from OTP_Form_GUI import start_otppage
    start_otppage(firstname, lastname, username, co_number, email, b_address, password)