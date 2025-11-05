# Reset_password_GUI
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re
from PIL import Image, ImageTk
import requests
from io import BytesIO


# ----------------- NEW FUNCTION STARTS HERE -----------------
def go_back_to_login(current_window):
    current_window.destroy()
    from Log_In_GUI import start_login1
    start_login1()


# ----------------- NEW FUNCTION ENDS HERE -----------------


def start_resetpass():
    # --- App Configuration ---
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("P2SERVE - Forgot Password")

    WIDTH, HEIGHT = 800, 500
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(True, True)

    # --- Main Content Frame ---
    main_content_area = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
    main_content_area.pack(fill="both", expand=True)

    # --- Content Frame inside Main Area ---
    content_frame = ctk.CTkFrame(main_content_area, fg_color="white")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- LEFT COLUMN (Entry Fields) ---
    entry_column = ctk.CTkFrame(content_frame, fg_color="white")
    entry_column.pack(side="left", padx=20, pady=20, fill="y")

    # Title
    title = ctk.CTkLabel(entry_column, text="RESET PASSWORD", text_color="black",
                         font=("Nirmala UI", 24, "bold"))
    title.pack(pady=(0, 30))

    # --- Input Fields ---
    email_label = ctk.CTkLabel(entry_column, text="Registered Email Address:", text_color="black", anchor="w",
                               font=("Nirmala UI", 11))
    email_label.pack(fill="x", padx=10, pady=(5, 0))
    email_entry = ctk.CTkEntry(entry_column, width=420, height=35, corner_radius=10, font=("Nirmala UI", 11))
    email_entry.pack(padx=10, pady=(0, 15))

    new_pass_label = ctk.CTkLabel(entry_column, text="Enter New Password:", text_color="black", anchor="w",
                                  font=("Nirmala UI", 11))
    new_pass_label.pack(fill="x", padx=10, pady=(5, 0))
    new_pass_entry = ctk.CTkEntry(entry_column, width=420, height=35, corner_radius=10, show="*",
                                  font=("Nirmala UI", 11))
    new_pass_entry.pack(padx=10, pady=(0, 15))

    def load_image_from_url(url, size=None):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            pil_img = Image.open(img_data)
            if size:  # optional resize
                pil_img = pil_img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print("❌ Error loading image:", e)
            return None
    view_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/view.png"
    hide_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/hide.png"

    # --- Eye icon toggle ---
    view_img = load_image_from_url(view_url, size=(20, 20))
    hide_img = load_image_from_url(hide_url, size=(20, 20))
    eye_label_new_pass = tk.Label(entry_column, image=view_img, bg="white", cursor="hand2")
    eye_label_new_pass.place(in_=new_pass_entry, relx=1.0, x=-2, rely=0.5, anchor="e")

    def toggle_new_pass():
        if new_pass_entry.cget("show") == "*":
            new_pass_entry.configure(show="")
            eye_label_new_pass.config(image=hide_img)
        else:
            new_pass_entry.configure(show="*")
            eye_label_new_pass.config(image=view_img)

    eye_label_new_pass.bind("<Button-1>", lambda e: toggle_new_pass())

    confirm_pass_label = ctk.CTkLabel(entry_column, text="Confirm New Password:", text_color="black", anchor="w",
                                      font=("Nirmala UI", 11))
    confirm_pass_label.pack(fill="x", padx=10, pady=(5, 0))
    confirm_pass_entry = ctk.CTkEntry(entry_column, width=420, height=35, corner_radius=10, show="*",
                                      font=("Nirmala UI", 11))
    confirm_pass_entry.pack(padx=10, pady=(0, 20))

    eye_label_confirm_pass = tk.Label(entry_column, image=view_img, bg="white", cursor="hand2")
    eye_label_confirm_pass.place(in_=confirm_pass_entry, relx=1.0, x=-2, rely=0.5, anchor="e")

    def toggle_confirm_pass():
        if confirm_pass_entry.cget("show") == "*":
            confirm_pass_entry.configure(show="")
            eye_label_confirm_pass.config(image=hide_img)
        else:
            confirm_pass_entry.configure(show="*")
            eye_label_confirm_pass.config(image=view_img)

    eye_label_confirm_pass.bind("<Button-1>", lambda e: toggle_confirm_pass())

    error_label = ctk.CTkLabel(
        entry_column, text="", text_color="#C0392B", font=("Nirmala UI", 11, "bold")
    )
    error_label.pack(pady=(5, 5))
    #----------- VALIDATION
    def confirm_reset():
        error_label.configure(text="")
        email = email_entry.get()
        new_pass = new_pass_entry.get()
        confirm_pass = confirm_pass_entry.get()

        if not email or not new_pass or not confirm_pass:
            error_label.configure(text="Error: All fields are required.")
            return

        if new_pass != confirm_pass:
            error_label.configure(text="Error: New passwords do not match.")
            return

        if len(new_pass) < 8 or not any(char.isalpha() for char in new_pass) or not any(
                char.isdigit() for char in new_pass):
            error_label.configure(text="Error: Password must be at least 8 chars and include letters and numbers.")
            return

        print(f"Password reset request confirmed for {email}.")
        do_forgotpass(email, new_pass, root)

        error_label.configure(text="Success! Proceeding to OTP verification.", text_color="#27AE60")
        email_entry.delete(0, 'end')
        new_pass_entry.delete(0, 'end')
        confirm_pass_entry.delete(0, 'end')

    confirm_btn = ctk.CTkButton(
        entry_column, text="CONFIRM", width=420, height=40, corner_radius=20,
        fg_color="#007BFF", hover_color="#0056D6", font=("Nirmala UI", 12, "bold"),
        command=confirm_reset
    )
    confirm_btn.pack(pady=(20, 5))

    # ----------------- NEW WIDGET STARTS HERE -----------------
    # --- Back to Login Link ---
    back_to_login_label = ctk.CTkLabel(
        entry_column,
        text="Back to Log In",
        text_color="#007BFF",
        font=("Nirmala UI", 11),
        cursor="hand2"
    )
    back_to_login_label.pack(pady=10)
    back_to_login_label.bind("<Button-1>", lambda e: go_back_to_login(root))
    # ----------------- NEW WIDGET ENDS HERE -----------------

    # --- RIGHT COLUMN (Logo/Image Section) ---
    image_column = ctk.CTkFrame(content_frame, width=250, fg_color="#3498db", corner_radius=10)
    image_column.pack(side="right", fill="y", padx=(0, 20), pady=20)

    try:
        logo_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/P2SERVE_LOGO.png"
        logo_img = load_image_from_url(logo_url)
        logo_lbl = tk.Label(image_column, image=logo_img, bg="#3498db")
        logo_lbl.image = logo_img
        logo_lbl.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        logo_lbl = ctk.CTkLabel(image_column, text="[P2SERVE Logo]", text_color="white", font=("Nirmala UI", 16))
        logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

    # --- Center window ---
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (WIDTH // 2)
    y = (root.winfo_screenheight() // 2) - (HEIGHT // 2)
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    root.mainloop()

#------------ Path papunta OTP form
def do_forgotpass(email, new_password, window):
    if email.endswith("@gmail.com"):
        window.destroy()
        from OTP_FormResetPass_GUI import start_otpForgotpage
        start_otpForgotpage(email, new_password)