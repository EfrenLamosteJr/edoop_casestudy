# OTP_FORM_GUI
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re
import random
import smtplib
from email.message import EmailMessage
from auth import signup
from auth import forgotpassword


def start_otpForgotpage(email, new_password):
    # --- App Configuration ---
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # --- Root Window ---
    root = ctk.CTk()
    # --- MODIFICATION: Set the title for the standard window bar ---
    root.title("OTP Verification")

    root.geometry("400x300")
    root.resizable(False, False)

    # --- MODIFICATION: Removed root.overrideredirect(True) ---

    # --- Centering ---
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # --- MODIFICATION: Removed root.attributes('-topmost', True) ---

    # --- OTP Storage ---
    generated_otp = None

    def otp_genetarot():
        nonlocal generated_otp
        generated_otp = ""
        for i in range(6):
            generated_otp += str(random.randint(0, 9))
        print("Your Otp is: " + generated_otp)

        try:
            with open("otp_email.html", "r", encoding="utf-8") as file:
                html_content = file.read()
            html_content = html_content.replace("{{ otp }}", generated_otp)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            from_email = "barangaypoblacion2eservice@gmail.com"
            server.login(from_email, 'veorjdapcuglikhu')
            to_mail = email

            msg = EmailMessage()
            msg['Subject'] = "OTP Verification"
            msg['From'] = from_email
            msg['To'] = to_mail
            msg.set_content("Your OTP is: " + generated_otp)
            msg.add_alternative(html_content, subtype='html')

            server.send_message(msg)
            server.quit()

            print("✅ Email sent successfully!")
            messagebox.showinfo("OTP Sent", "Check your email for the 6-digit code!")
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTP Authentication Error: {e}")
            messagebox.showerror("Email Error",
                                 "Failed to send OTP. Check email settings and try again.\nError: Please log in with your web browser. Ensure 2-Step Verification is enabled and use a valid App Password.")
        except Exception as e:
            print(f"Email sending error: {e}")
            messagebox.showerror("Email Error", f"Failed to send OTP: {str(e)}")

    # --- Frame for Centering ---
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # --- Title ---
    title_label = ctk.CTkLabel(frame, text="OTP Verification", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(20, 10))

    # --- Info Label ---
    info_label = ctk.CTkLabel(
        frame,
        text="We sent an OTP to your email.\nThe OTP will expire within 5 minutes.",
        font=ctk.CTkFont(size=12),
        justify="center"
    )
    info_label.pack(pady=(0, 20))

    # --- OTP Entry Boxes ---
    otp_frame = ctk.CTkFrame(frame, fg_color="transparent")
    otp_frame.pack(pady=(0, 20))

    otp_vars = []
    otp_entries = []
    for i in range(6):
        var = tk.StringVar()
        entry = ctk.CTkEntry(otp_frame, width=40, height=40, justify="center", textvariable=var,
                             font=ctk.CTkFont(size=16))
        entry.grid(row=0, column=i, padx=5)
        otp_vars.append(var)
        otp_entries.append(entry)

    # --- Auto-focus and digit-only handling ---
    def on_key(event, entry_index):
        current = otp_vars[entry_index].get()
        if len(current) > 1:
            otp_vars[entry_index].set(current[-1])
        if len(current) == 1 and entry_index < 5:
            otp_entries[entry_index + 1].focus()

    for i, entry in enumerate(otp_entries):
        entry.bind("<KeyRelease>", lambda e, idx=i: on_key(e, idx))
        entry.bind("<FocusOut>", lambda e, idx=i: otp_vars[idx].set(otp_vars[idx].get().strip()))

    # --- Resend OTP Button ---
    def resend_otp():
        print("OTP Resent!")
        otp_genetarot()
        for var in otp_vars:
            var.set("")
        otp_entries[0].focus()

    resend_btn = ctk.CTkButton(frame, text="Resend OTP", width=120, command=resend_otp, fg_color="transparent",
                               hover_color="#cce5ff", text_color="blue")
    resend_btn.pack(pady=(0, 20))

    # --- Submit Button ---
    def verify_otp():
        if generated_otp is None:
            messagebox.showerror("Error", "No OTP generated. Please request an OTP first.")
            return
        otp = "".join(var.get() for var in otp_vars).strip()
        print("Entered OTP:", otp)
        if len(otp) != 6:
            messagebox.showerror("Error", "Please enter a valid 6-digit OTP.")
            return
        do_otp(generated_otp, otp, email, new_password, root)

    submit_btn = ctk.CTkButton(frame, text="Submit", width=200, command=verify_otp)
    submit_btn.pack(pady=(0, 10))

    # --- Focus on first entry ---
    otp_entries[0].focus()

    # --- Initial OTP Generation ---
    otp_genetarot()

    # --- MODIFICATION: Removed custom close button and its function ---

    root.mainloop()


def do_otp(generated_otp, otp, email, new_password, window):
    if generated_otp == otp:
        forgotpassword(email, new_password)
        messagebox.showinfo("Success", "Your password has been reset successfully!")
        window.destroy()
        from Log_In_GUI import start_login1
        start_login1()
    else:
        messagebox.showerror("OTP Error", "Invalid OTP. Please try again.")