#login.py
from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox
from auth import login

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"C:\Users\EfrenLamostejr\Documents\Study\case study oop\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0")

#---------- LOGIN ----------------
def start_login():
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()

    window.geometry("1920x1080")
    window.configure(bg="#3A97E2")

    canvas = Canvas(
        window,
        bg="#3A97E2",
        height=1080,
        width=1920,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        517.0,
        250.0,
        1402.0,
        830.0,
        fill="#FFFFFF",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    #BUTTON----------------
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: do_login(l_username.get(), l_password.get()),
        relief="flat",
    )
    button_1.place(
        x=557.0,
        y=656.0,
        width=804.0,
        height=71.0
    )

    canvas.create_text(
        712.0,
        307.0,
        anchor="nw",
        text="P2SERVE LOGIN FORM",
        fill="#000000",
        font=("SFPro Semibold", 48 * -1)
    )
    ## SIGN IN PATH -------------------
    link_label = tk.Label(window, text="Don’t have an account?",
                          font=("SFPro Regular", 36 * -1, "underline"), fg="#5F97FE", bg="#FFFFFF", cursor="hand2")
    canvas.create_window(1009.0, 759.0, anchor="nw", window=link_label)

    def on_enter(e): link_label.config(fg="#3b6ed5")
    def on_leave(e): link_label.config(fg="#5F97FE")
    def on_click(e):
        window.destroy()
        #----- tang ina lilipat lang pala import amp
        from signups import start_signup
        start_signup()

    link_label.bind("<Enter>", on_enter)
    link_label.bind("<Leave>", on_leave)
    link_label.bind("<Button-1>", on_click)

    ## FORGOT IN PATH --------------------
    link_label = tk.Label(window, text="Forgot Password?",
                          font=("SFPro Regular", 36 * -1, "underline"), fg="#5F97FE", bg="#FFFFFF", cursor="hand2")
    canvas.create_window(557.0, 759.0, anchor="nw", window=link_label)

    def on_enter(e): link_label.config(fg="#3b6ed5")
    def on_leave(e): link_label.config(fg="#5F97FE")
    def on_click(e):
        window.destroy()

    link_label.bind("<Enter>", on_enter)
    link_label.bind("<Leave>", on_leave)
    link_label.bind("<Button-1>", on_click)

    canvas.create_rectangle(
        542.0,
        260.0,
        690.0,
        410.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        1234.0,
        260.0,
        1384.0,
        410.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        557.0,
        424.0,
        anchor="nw",
        text="Username or Email",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        958.0,
        493.0,
        image=entry_image_1
    )
    l_username = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    l_username.place(
        x=571.0,
        y=462.0,
        width=774.0,
        height=60.0
    )

    canvas.create_text(
        557.0,
        524.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        958.0,
        593.0,
        image=entry_image_2
    )
    l_password = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    l_password.place(
        x=571.0,
        y=562.0,
        width=774.0,
        height=60.0
    )

    window.resizable(False, False)
    window.mainloop()


#------------ CONDITION -----------

def do_login(log_user, log_pass):

    ok, msg = login(log_user, log_pass)
    if ok:
        messagebox.showinfo("Logaqsdasdin", msg)
    else:
        messagebox.showerror("Login", msg)