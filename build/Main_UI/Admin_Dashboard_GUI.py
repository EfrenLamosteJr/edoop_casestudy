# Admin_Dashboard_GUI.py (Corrected scope for action functions)
import customtkinter as ctk

# --- Color Palette ---
SIDEBAR_BG = "#3498db"
SIDEBAR_BTN_HOVER = "#2980b9"
ACTIVE_BTN_BG = "#ffffff"
ACTIVE_BTN_TEXT = "#3498db"
CONTENT_BG = "#f2f2f2"
TEXT_COLOR_DARK = "black"
APPROVE_COLOR = "#2ECC71" # Green
REJECT_COLOR = "#E74C3C" # Red
VIEW_COLOR = "#3498DB" # Blue
EDIT_COLOR = "#F1C40F" # Yellow/Orange
DEACTIVATE_COLOR = "#95A5A6" # Gray

# Global dictionary to hold references to sidebar buttons
button_widgets = {}

# =============================================================================
# --- Content Creation Functions for Each Page ---
# =============================================================================

def show_dashboard_content(parent_frame):
    """Creates and displays the widgets for the Dashboard Overview page."""
    # (Dashboard content function - collapsed for brevity)
    stats_frame = ctk.CTkFrame(parent_frame, fg_color="transparent"); stats_frame.pack(fill="x", pady=(0, 20)); stats_frame.columnconfigure((0, 1, 2), weight=1)
    def create_stat_card(parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10); card.grid(sticky="ew", padx=10)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(pady=(15, 5), padx=20, anchor="w")
        value_frame = ctk.CTkFrame(card, fg_color="transparent"); value_frame.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(value_frame, text=value, font=ctk.CTkFont(size=36, weight="bold")).pack(side="left")
        ctk.CTkLabel(value_frame, text=icon, font=ctk.CTkFont(size=36), text_color=color).pack(side="right")
        return card
    create_stat_card(stats_frame, "New Registrations (Pending)", "--", "➕", "#E74C3C").grid(row=0, column=0)
    create_stat_card(stats_frame, "Pending Requests to Process", "--", "📂", "#F1C40F").grid(row=0, column=1)
    create_stat_card(stats_frame, "Total Registered Residents", "--", "🏠", "#3498DB").grid(row=0, column=2)
    urgent_banner = ctk.CTkFrame(parent_frame, fg_color="#FADBD8", border_color="#E74C3C", border_width=1, corner_radius=10); urgent_banner.pack(fill="x", pady=(0, 20))
    urgent_label = ctk.CTkLabel(urgent_banner, text="You have '--' new resident accounts pending approval...", font=ctk.CTkFont(size=14), text_color="#C03B2B", anchor="center"); urgent_label.pack(pady=10, padx=20)
    ctk.CTkLabel(parent_frame, text="Quick Actions", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(fill="x", pady=(0, 10))
    actions_frame = ctk.CTkFrame(parent_frame, fg_color="transparent"); actions_frame.pack(fill="x"); actions_frame.columnconfigure((0, 1, 2, 3), weight=1)
    def create_action_button(parent, text, color, command=None):
        cmd = command if command else lambda t=text: print(f"Quick action clicked: {t}")
        button = ctk.CTkButton(parent, text=text, fg_color=color, height=50, font=ctk.CTkFont(size=14, weight="bold"), command=cmd); button.grid(sticky="ew", padx=10)
        return button
    create_action_button(actions_frame, "✅  Approve Residents", "#2ECC71", command=None).grid(row=0, column=0)
    create_action_button(actions_frame, "▶️  Process Requests", "#3498DB", command=None).grid(row=0, column=1)
    create_action_button(actions_frame, "👁️  View All Residents", "#3498DB", command=None).grid(row=0, column=2)
    create_action_button(actions_frame, "⚙️  Manage Staff", "#95A5A6", command=None).grid(row=0, column=3)


def show_request_management_content(parent_frame):
    """Creates and displays the content for the Request Management page."""
    # (Request Management content function - collapsed for brevity)
    no_requests_banner = ctk.CTkFrame(parent_frame, fg_color="#D4EDDA", border_color="#28A745", border_width=1, corner_radius=10)
    no_requests_banner.pack(fill="x", pady=(20, 0), padx=20)
    ctk.CTkLabel(no_requests_banner, text="✅ Good job! There are currently no pending requests to process.", font=ctk.CTkFont(size=14, weight="bold"), text_color="#155724", anchor="center").pack(pady=10, padx=20)


def show_resident_accounts_content(parent_frame):
    """Creates and displays the UI for managing resident accounts."""
    pending_residents = [
        {"id": 3, "name": "Eulysses Domantay", "email": "domantayeulysses23@gmail.com", "contact": "096086327971"},
    ]
    approved_residents = [
        {"id": 4, "name": "Glesie Domantay", "email": "glesied33@gmail.com", "contact": "09026392156"},
    ]

    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True)

    pending_title_text = f"New Registrations Pending Approval ({len(pending_residents)})"
    pending_title = ctk.CTkLabel(scrollable_frame, text=pending_title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    pending_title.pack(fill="x", pady=(10, 5), padx=10)

    pending_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    pending_container.pack(fill="x", pady=(0, 20), padx=10)

    if not pending_residents:
        ctk.CTkLabel(pending_container, text="No pending registrations.", text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_pending = ctk.CTkFrame(pending_container, fg_color="transparent")
        header_frame_pending.pack(fill="x", padx=10, pady=(10, 5))
        header_frame_pending.grid_columnconfigure((1, 2, 3), weight=1)
        header_frame_pending.grid_columnconfigure(4, weight=0)

        ctk.CTkLabel(header_frame_pending, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="EMAIL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="CONTACT NO.", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="ACTION", font=ctk.CTkFont(weight="bold")).grid(row=0, column=4, sticky="e", padx=5)

        for resident in pending_residents:
            row_frame = ctk.CTkFrame(pending_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure((1, 2, 3), weight=1)
            row_frame.grid_columnconfigure(4, weight=0)

            ctk.CTkLabel(row_frame, text=f"#{resident['id']}").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['name']).grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['email']).grid(row=0, column=2, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['contact']).grid(row=0, column=3, sticky="w", padx=5)

            action_buttons_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_buttons_frame.grid(row=0, column=4, sticky="e")

            # --- >>> CORRECTED: Define actions on separate lines <<< ---
            def view_action(res_id):
                print(f"View resident {res_id}")
            def approve_action(res_id):
                print(f"Approve resident {res_id}")
            def reject_action(res_id):
                print(f"Reject resident {res_id}")
            # --- >>>-------------------------------------------<<< ---

            # Assign commands using the defined functions
            ctk.CTkButton(action_buttons_frame, text="View", width=60, height=25, fg_color=VIEW_COLOR, font=ctk.CTkFont(size=10), command=lambda id=resident['id']: view_action(id)).pack(side="left", padx=2)
            ctk.CTkButton(action_buttons_frame, text="Approve", width=60, height=25, fg_color=APPROVE_COLOR, font=ctk.CTkFont(size=10), command=lambda id=resident['id']: approve_action(id)).pack(side="left", padx=2)
            ctk.CTkButton(action_buttons_frame, text="Reject", width=60, height=25, fg_color=REJECT_COLOR, font=ctk.CTkFont(size=10), command=lambda id=resident['id']: reject_action(id)).pack(side="left", padx=2)

    approved_title_text = f"All Approved Resident Accounts ({len(approved_residents)})"
    approved_title = ctk.CTkLabel(scrollable_frame, text=approved_title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    approved_title.pack(fill="x", pady=(20, 5), padx=10)

    approved_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    approved_container.pack(fill="x", pady=(0, 20), padx=10)

    if not approved_residents:
        ctk.CTkLabel(approved_container, text="No approved residents found.", text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_approved = ctk.CTkFrame(approved_container, fg_color="transparent"); header_frame_approved.pack(fill="x", padx=10, pady=(10, 5)); header_frame_approved.grid_columnconfigure((1, 2, 3), weight=1)
        ctk.CTkLabel(header_frame_approved, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5); ctk.CTkLabel(header_frame_approved, text="NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5); ctk.CTkLabel(header_frame_approved, text="EMAIL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5); ctk.CTkLabel(header_frame_approved, text="CONTACT NO.", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="w", padx=5)
        for resident in approved_residents:
            row_frame = ctk.CTkFrame(approved_container, fg_color="transparent"); row_frame.pack(fill="x", padx=10, pady=5); row_frame.grid_columnconfigure((1, 2, 3), weight=1)
            ctk.CTkLabel(row_frame, text=f"#{resident['id']}").grid(row=0, column=0, sticky="w", padx=5); ctk.CTkLabel(row_frame, text=resident['name']).grid(row=0, column=1, sticky="w", padx=5); ctk.CTkLabel(row_frame, text=resident['email']).grid(row=0, column=2, sticky="w", padx=5); ctk.CTkLabel(row_frame, text=resident['contact']).grid(row=0, column=3, sticky="w", padx=5)


def show_staff_accounts_content(parent_frame):
    """Creates and displays the UI for managing staff accounts."""
    # (Staff Accounts content function - collapsed for brevity)
    existing_staff = [{"id": 1, "name": "Barangay Staff Admin", "username": "barangay_admin", "position": "Admin", "role": "Admin", "status": "Active"}]
    staff_roles = ["Admin", "Staff", "Treasurer"]
    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent"); scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
    create_frame = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5); create_frame.pack(fill="x", pady=(0, 20), padx=0)
    ctk.CTkLabel(create_frame, text="Create New Staff Account", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(fill="x", padx=20, pady=(15, 10))
    form_grid = ctk.CTkFrame(create_frame, fg_color="transparent"); form_grid.pack(fill="x", padx=20, pady=(0, 20)); form_grid.columnconfigure(0, weight=1)
    def create_form_row(parent, label_text, widget_type="entry", options=None, show_char=None):
        ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", pady=(5, 2))
        if widget_type == "entry": entry = ctk.CTkEntry(parent, height=35, corner_radius=5, show=show_char); entry.pack(fill="x"); return entry
        elif widget_type == "combobox": combobox = ctk.CTkComboBox(parent, height=35, corner_radius=5, values=options, state="readonly"); combobox.pack(fill="x"); combobox.set("-Select Role-"); return combobox
    full_name_entry = create_form_row(form_grid, "Full Name"); username_entry = create_form_row(form_grid, "Username"); password_entry = create_form_row(form_grid, "Password (Temporary)", show_char="*"); position_entry = create_form_row(form_grid, "Position (Optional)"); role_combobox = create_form_row(form_grid, "Staff Role", widget_type="combobox", options=staff_roles)
    def create_account_action():
        print(f"Creating Staff...") # Simplified action
        full_name_entry.delete(0, 'end'); username_entry.delete(0, 'end'); password_entry.delete(0, 'end'); position_entry.delete(0, 'end'); role_combobox.set("-Select Role-")
    create_button = ctk.CTkButton(form_grid, text="+ Create Account", height=40, font=ctk.CTkFont(weight="bold"), command=create_account_action); create_button.pack(fill="x", pady=(20, 5))
    existing_title_text = f"Existing Staff Accounts ({len(existing_staff)})"; existing_title = ctk.CTkLabel(scrollable_frame, text=existing_title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w"); existing_title.pack(fill="x", pady=(10, 5), padx=0)
    existing_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5); existing_container.pack(fill="x", pady=(0, 20), padx=0)
    if not existing_staff: ctk.CTkLabel(existing_container, text="No existing staff accounts found.", text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_existing = ctk.CTkFrame(existing_container, fg_color="transparent", height=30); header_frame_existing.pack(fill="x", padx=10, pady=(10, 5)); header_frame_existing.grid_columnconfigure((1, 2, 3), weight=1); header_frame_existing.grid_columnconfigure((0, 4, 5, 6), weight=0)
        headers = ["ID", "NAME", "USERNAME", "POSITION", "ROLE", "STATUS", "ACTION"]
        for i, header in enumerate(headers): sticky_val = "w" if i < len(headers) -1 else "e"; ctk.CTkLabel(header_frame_existing, text=header, font=ctk.CTkFont(weight="bold", size=11)).grid(row=0, column=i, sticky=sticky_val, padx=5)
        for staff in existing_staff:
            row_frame = ctk.CTkFrame(existing_container, fg_color="transparent", height=30); row_frame.pack(fill="x", padx=10, pady=2); row_frame.grid_columnconfigure((1, 2, 3), weight=1); row_frame.grid_columnconfigure((0, 4, 5, 6), weight=0)
            ctk.CTkLabel(row_frame, text=f"#{staff['id']}", font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", padx=5); ctk.CTkLabel(row_frame, text=staff['name'], font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=1, sticky="ew", padx=5); ctk.CTkLabel(row_frame, text=staff['username'], font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=2, sticky="ew", padx=5); ctk.CTkLabel(row_frame, text=staff['position'] or "-", font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=3, sticky="ew", padx=5)
            role_label = ctk.CTkLabel(row_frame, text=staff['role'], font=ctk.CTkFont(size=10, weight="bold"), corner_radius=5, width=50); role_label.grid(row=0, column=4, sticky="w", padx=5); role_color = REJECT_COLOR if staff['role'].lower() == 'admin' else VIEW_COLOR; role_label.configure(fg_color=role_color, text_color="white")
            status_label = ctk.CTkLabel(row_frame, text=staff['status'], font=ctk.CTkFont(size=10, weight="bold"), corner_radius=5, width=50); status_label.grid(row=0, column=5, sticky="w", padx=5); status_color = APPROVE_COLOR if staff['status'].lower() == 'active' else DEACTIVATE_COLOR; status_label.configure(fg_color=status_color, text_color="white")
            action_buttons_frame = ctk.CTkFrame(row_frame, fg_color="transparent"); action_buttons_frame.grid(row=0, column=6, sticky="e")
            def view_staff_action(staff_id): print(f"View staff {staff_id}")
            ctk.CTkButton(action_buttons_frame, text="View", width=50, height=25, fg_color=VIEW_COLOR, font=ctk.CTkFont(size=10), command=lambda id=staff['id']: view_staff_action(id)).pack(side="left", padx=2)


def show_system_settings_content(parent_frame):
    """Placeholder function to display content for the System Settings page."""
    show_placeholder_content(parent_frame, "System Settings")


def show_placeholder_content(parent_frame, page_name):
    """Shows simple placeholder text for pages that are not fully built yet."""
    # (Placeholder function - collapsed for brevity)
    ctk.CTkLabel(parent_frame, text=f"Content for {page_name} goes here.", font=ctk.CTkFont(size=18), text_color="gray").pack(pady=50)

# =============================================================================
# --- Main Application Window ---
# =============================================================================

def start_admin_dashboard():
    # (Main app setup - collapsed for brevity)
    ctk.set_appearance_mode("light"); ctk.set_default_color_theme("blue")
    root = ctk.CTk(); root.title("P2SERVE Admin Panel"); root.geometry("1200x700")
    root.grid_columnconfigure(1, weight=1); root.grid_rowconfigure(0, weight=1)
    sidebar_frame = ctk.CTkFrame(root, width=250, fg_color=SIDEBAR_BG, corner_radius=0); sidebar_frame.grid(row=0, column=0, sticky="nsw"); sidebar_frame.grid_propagate(False)
    content_container = ctk.CTkFrame(root, fg_color=CONTENT_BG, corner_radius=0); content_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20); content_container.grid_rowconfigure(1, weight=1); content_container.grid_columnconfigure(0, weight=1)
    main_header_label = ctk.CTkLabel(content_container, text="", font=ctk.CTkFont(size=24, weight="bold"), anchor="w", text_color=TEXT_COLOR_DARK); main_header_label.grid(row=0, column=0, sticky="ew", pady=(0, 20))
    dynamic_content_frame = ctk.CTkFrame(content_container, fg_color="transparent"); dynamic_content_frame.grid(row=1, column=0, sticky="nsew")

    # --- Navigation Logic ---
    nav_buttons = {
        "dashboard": ["📊", "Dashboard Overview"],
        "requests": ["📁", "Request Management"],
        "residents": ["👥", "Resident Accounts"],
        "staff": ["👤", "Staff Accounts"],
        "settings": ["⚙️", "System Settings"]
    }

    def update_sidebar_selection(active_key):
        # (Function remains the same - collapsed)
        for key, button_widget in button_widgets.items():
            is_active = (key == active_key)
            button_widget.configure(fg_color=ACTIVE_BTN_BG if is_active else "transparent", text_color=ACTIVE_BTN_TEXT if is_active else "white", font=ctk.CTkFont(size=14, weight="bold" if is_active else "normal"))

    def navigate_to(page_key):
        # (Function remains the same)
        print(f"Navigating to {page_key}")
        if page_key not in nav_buttons: print(f"Error: Page key '{page_key}' not found."); return
        main_header_label.configure(text=nav_buttons[page_key][1])
        update_sidebar_selection(page_key)
        for widget in dynamic_content_frame.winfo_children(): widget.destroy()

        if page_key == "dashboard": show_dashboard_content(dynamic_content_frame)
        elif page_key == "requests": show_request_management_content(dynamic_content_frame)
        elif page_key == "residents": show_resident_accounts_content(dynamic_content_frame)
        elif page_key == "staff": show_staff_accounts_content(dynamic_content_frame)
        elif page_key == "settings": show_system_settings_content(dynamic_content_frame)
        else: show_placeholder_content(dynamic_content_frame, "Unknown Page")

    # --- Sidebar Widgets ---
    # (Sidebar creation remains the same - collapsed)
    sidebar_title = ctk.CTkLabel(sidebar_frame, text="P2SERVE Admin Panel", font=ctk.CTkFont(size=20, weight="bold"), text_color="white"); sidebar_title.pack(pady=20, padx=20, anchor="w")
    for key, (icon, text) in nav_buttons.items():
        button = ctk.CTkButton(sidebar_frame, text=f" {icon}  {text}", fg_color="transparent", text_color="white", hover_color=SIDEBAR_BTN_HOVER, font=ctk.CTkFont(size=14), anchor="w", height=40, corner_radius=8, command=lambda k=key: navigate_to(k)); button.pack(fill="x", padx=10, pady=5); button_widgets[key] = button
    def logout_action():
        print("Admin logged out."); root.destroy()
        try: from Admin_Log_In_GUI import start_admin_login; start_admin_login()
        except ImportError: print("Error: Could not import Admin_Log_In_GUI.py")
    logout_btn = ctk.CTkButton(sidebar_frame, text="➡️  Log Out", fg_color="transparent", text_color="white", hover_color=SIDEBAR_BTN_HOVER, font=ctk.CTkFont(size=14), anchor="w", height=40, corner_radius=8, command=logout_action); logout_btn.pack(side="bottom", fill="x", padx=10, pady=20)

    # --- Initial Page Load ---
    navigate_to("dashboard")

    # --- Center & Maximize Window ---
    # (Centering/Maximize logic remains the same - collapsed)
    root.update_idletasks(); width = 1200; height = 700; x = (root.winfo_screenwidth() // 2) - (width // 2); y = (root.winfo_screenheight() // 2) - (height // 2); root.geometry(f"{width}x{height}+{x}+{y}")
    root.state('zoomed')

    root.mainloop()

# --- To run the application ---
if __name__ == "__main__":
    start_admin_dashboard()