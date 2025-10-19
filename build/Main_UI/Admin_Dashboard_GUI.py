# Admin_Dashboard_GUI.py
import customtkinter as ctk

def start_admin_dashboard():
    # --- App Configuration ---
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("P2SERVE Admin Panel")
    root.geometry("1200x700")

    # --- Color Palette ---
    SIDEBAR_BG = "#3498db"
    SIDEBAR_BTN_HOVER = "#2980b9"
    ACTIVE_BTN_BG = "#ffffff"
    ACTIVE_BTN_TEXT = "#3498db"
    CONTENT_BG = "#f2f2f2"

    # --- Main Layout Frames ---
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    sidebar_frame = ctk.CTkFrame(root, width=250, fg_color=SIDEBAR_BG, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, sticky="nsw")
    sidebar_frame.grid_propagate(False)

    main_content_frame = ctk.CTkFrame(root, fg_color=CONTENT_BG, corner_radius=0)
    main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    # ----------------- NEW FUNCTION STARTS HERE -----------------
    def logout_action():
        """Closes the dashboard and returns to the admin login screen."""
        print("Admin logged out.")
        root.destroy()
        from Admin_Log_In_GUI import start_admin_login
        start_admin_login()
    # ----------------- NEW FUNCTION ENDS HERE -----------------

    # --- Sidebar Widgets ---
    sidebar_title = ctk.CTkLabel(
        sidebar_frame,
        text="P2SERVE Admin Panel",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="white"
    )
    sidebar_title.pack(pady=20, padx=20, anchor="w")

    nav_buttons = {
        "dashboard": ["📊", "Dashboard Overview"],
        "requests": ["📁", "Request Management"],
        "residents": ["👥", "Resident Accounts"],
        "staff": ["👤", "Staff Accounts"],
        "settings": ["⚙️", "System Settings"]
    }

    for key, (icon, text) in nav_buttons.items():
        is_active = (key == "dashboard")
        button = ctk.CTkButton(
            sidebar_frame,
            text=f" {icon}   {text}",
            fg_color=ACTIVE_BTN_BG if is_active else "transparent",
            text_color=ACTIVE_BTN_TEXT if is_active else "white",
            hover_color=SIDEBAR_BTN_HOVER,
            font=ctk.CTkFont(size=14, weight="bold" if is_active else "normal"),
            anchor="w",
            height=40,
            corner_radius=8
        )
        button.pack(fill="x", padx=10, pady=5)

    # Log Out Button (MODIFIED: command added)
    logout_btn = ctk.CTkButton(
        sidebar_frame,
        text="➡️   Log Out",
        fg_color="transparent",
        text_color="white",
        hover_color=SIDEBAR_BTN_HOVER,
        font=ctk.CTkFont(size=14),
        anchor="w",
        height=40,
        corner_radius=8,
        command=logout_action  # Assign the new function here
    )
    logout_btn.pack(side="bottom", fill="x", padx=10, pady=20)

    # --- Main Content Widgets ---
    header_label = ctk.CTkLabel(
        main_content_frame,
        text="Admin Dashboard - Welcome, barangay_admin",
        font=ctk.CTkFont(size=24, weight="bold"),
        anchor="w"
    )
    header_label.pack(fill="x", pady=(0, 20))

    stats_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    stats_frame.pack(fill="x", pady=(0, 20))
    stats_frame.columnconfigure((0, 1, 2), weight=1)

    def create_stat_card(parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(sticky="ew", padx=10)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(pady=(15, 5), padx=20, anchor="w")
        value_frame = ctk.CTkFrame(card, fg_color="transparent")
        value_frame.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(value_frame, text=value, font=ctk.CTkFont(size=36, weight="bold")).pack(side="left")
        ctk.CTkLabel(value_frame, text=icon, font=ctk.CTkFont(size=36), text_color=color).pack(side="right")
        return card

    create_stat_card(stats_frame, "New Registrations (Pending)", "--", "➕", "#E74C3C").grid(row=0, column=0)
    create_stat_card(stats_frame, "Pending Requests to Process", "--", "📂", "#F1C40F").grid(row=0, column=1)
    create_stat_card(stats_frame, "Total Registered Residents", "--", "🏠", "#3498DB").grid(row=0, column=2)

    urgent_banner = ctk.CTkFrame(main_content_frame, fg_color="#FADBD8", border_color="#E74C3C", border_width=1,
                                 corner_radius=10)
    urgent_banner.pack(fill="x", pady=(0, 20), ipady=10)
    ctk.CTkLabel(
        urgent_banner,
        text="You have '--' new resident accounts pending approval. Please review them immediately in the Resident Accounts section.",
        font=ctk.CTkFont(size=14),
        text_color="#C0392B"
    ).pack(padx=20)

    ctk.CTkLabel(main_content_frame, text="Quick Actions", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(
        fill="x", pady=(0, 10))

    actions_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    actions_frame.pack(fill="x")
    actions_frame.columnconfigure((0, 1, 2, 3), weight=1)

    def create_action_button(parent, text, color):
        button = ctk.CTkButton(parent, text=text, fg_color=color, height=50, font=ctk.CTkFont(size=14, weight="bold"))
        button.grid(sticky="ew", padx=10)
        return button

    create_action_button(actions_frame, "✅  Approve Residents", "#2ECC71").grid(row=0, column=0)
    create_action_button(actions_frame, "▶️  Process Requests", "#3498DB").grid(row=0, column=1)
    create_action_button(actions_frame, "👁️  View All Residents", "#3498DB").grid(row=0, column=2)
    create_action_button(actions_frame, "⚙️  Manage Staff", "#95A5A6").grid(row=0, column=3)

    root.mainloop()

# --- To run the application ---



#TANGINAMO
#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO

#TANGINAMO
#TANGINAMO
#pakyu mam burce

if __name__ == "__main__":
    start_admin_dashboard()