#signups.py
from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox
from auth import signup

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"C:\Users\EfrenLamostejr\Documents\Study\case study oop\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame1")


# ---------- SIGN IN ----------------

def start_signup():
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
        411.0,
        120.0,
        1509.0,
        961.0,
        fill="#FFFFFF",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    #--------- BUTTON
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: do_signup(fullname.get(), username.get(), email.get(), b_address.get(),password.get() ,c_password.get()),
        relief="flat"
    )
    button_1.place(
        x=448.0,
        y=867.0,
        width=276.0,
        height=73.0
    )

    #------------- LOGIN PATH
    link_label = tk.Label(window, text="Already have an account?",
                          font=("SFPro Regular", 40 * -1, "underline"), fg="#5F97FE", bg="#FFFFFF", cursor="hand2")
    canvas.create_window(1031.0, 882.0, anchor="nw", window=link_label)

    def on_enter(e): link_label.config(fg="#3b6ed5")
    def on_leave(e): link_label.config(fg="#5F97FE")
    def on_click(e):
        window.destroy()

        from login import start_login
        start_login()

    link_label.bind("<Enter>", on_enter)
    link_label.bind("<Leave>", on_leave)
    link_label.bind("<Button-1>", on_click)

    canvas.create_text(
        623.0,
        186.0,
        anchor="nw",
        text="P2SERVE SIGN UP FORM",
        fill="#000000",
        font=("SFPro Semibold", 60 * -1)
    )

    canvas.create_rectangle(
        448.0,
        143.0,
        596.0,
        293.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        1323.0,
        143.0,
        1473.0,
        293.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        1323.0,
        143.0,
        1473.0,
        293.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        451.0,
        406.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        962.0,
        469.0,
        image=entry_image_1
    )
    username = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    username.place(
        x=467.0,
        y=444.0,
        width=990.0,
        height=48.0
    )

    canvas.create_text(
        452.0,
        318.0,
        anchor="nw",
        text="Full Name",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        963.0,
        381.0,
        image=entry_image_2
    )
    fullname = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    fullname.place(
        x=468.0,
        y=356.0,
        width=990.0,
        height=48.0
    )

    canvas.create_text(
        451.0,
        494.0,
        anchor="nw",
        text="Email Address",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        962.0,
        557.0,
        image=entry_image_3
    )
    email = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    email .place(
        x=467.0,
        y=532.0,
        width=990.0,
        height=48.0
    )

    canvas.create_text(
        448.0,
        758.0,
        anchor="nw",
        text="Confirm Password",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        959.0,
        820.0,
        image=entry_image_5
    )
    c_password = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    c_password.place(
        x=464.0,
        y=795.0,
        width=990.0,
        height=48.0
    )

    canvas.create_text(
        451.0,
        670.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        959.0,
        733.0,
        image=entry_image_6
    )
    password = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    password.place(
        x=464.0,
        y=708.0,
        width=990.0,
        height=48.0
    )

    canvas.create_text(
        451.0,
        582.0,
        anchor="nw",
        text="Barangay Address",
        fill="#000000",
        font=("SFPro Regular", 32 * -1)
    )

    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        959.0,
        645.0,
        image=entry_image_7
    )
    b_address = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    b_address.place(
        x=464.0,
        y=620.0,
        width=990.0,
        height=48.0
    )
    window.resizable(False, False)
    window.mainloop()

#------------ CONDITION -----------
def do_signup(fullname,username,email,b_address,password,c_password):
    ok, msg = signup(fullname,username,email,b_address,password)
    if ok:
        messagebox.showinfo("Sign-Up", msg)
    else:
        messagebox.showerror("Sign-Up", msg)




