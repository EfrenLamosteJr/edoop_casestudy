# Admin_Dashboard_GUI.py
import customtkinter as ctk
from database_connector import get_connection

# --- Color Palette ---
SIDEBAR_BG = "#3498db"
SIDEBAR_BTN_HOVER = "#2980b9"
ACTIVE_BTN_BG = "#ffffff"
ACTIVE_BTN_TEXT = "#3498db"
CONTENT_BG = "#f2f2f2"
TEXT_COLOR_DARK = "black"
APPROVE_COLOR = "#2ECC71"  # Green
REJECT_COLOR = "#E74C3C"  # Red
VIEW_COLOR = "#3498DB"  # Blue
EDIT_COLOR = "#F1C40F"  # Yellow/Orange
DEACTIVATE_COLOR = "#95A5A6"  # Gray

# Global dictionary to hold references to sidebar buttons
button_widgets = {}


# --- Database Functions ---
def get_pending_requests_count():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM document_requests WHERE status = 'Pending'")
        row = cur.fetchone()
        return row[0] if row else 0
    except Exception as error:
        print(f"Error fetching pending requests count: {error}")
        return 0
    finally:
        cur.close()
        conn.close()


def get_total_residents_count():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM resident")
        row = cur.fetchone()
        return row[0] if row else 0
    except Exception as error:
        print(f"Error fetching total residents count: {error}")
        return 0
    finally:
        cur.close()
        conn.close()


def get_pending_requests():
    """Fetch all pending document requests with resident full names."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT dr.id, CONCAT(r.firstname, ' ', r.lastname) AS full_name, dr.document_name
            FROM document_requests dr
            JOIN resident r ON dr.user_id = r.id
            WHERE dr.status = 'Pending'
        """)
        rows = cur.fetchall()
        return [{"id": row[0], "full_name": row[1], "document_name": row[2]} for row in rows]
    except Exception as error:
        print(f"Error fetching pending requests: {error}")
        return []
    finally:
        cur.close()
        conn.close()


# --- Content Creation Functions for Each Page ---
def show_dashboard_content(parent_frame):
    pending_requests = get_pending_requests_count()
    total_residents = get_total_residents_count()

    stats_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    stats_frame.pack(fill="x", pady=(0, 20))
    stats_frame.columnconfigure((0, 1, 2), weight=1)

    def create_stat_card(parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(sticky="ew", padx=10)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(pady=(15, 5), padx=20, anchor="w")
        value_frame = ctk.CTkFrame(card, fg_color="transparent")
        value_frame.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(value_frame, text=str(value), font=ctk.CTkFont(size=36, weight="bold")).pack(side="left")
        ctk.CTkLabel(value_frame, text=icon, font=ctk.CTkFont(size=36), text_color=color).pack(side="right")
        return card

    create_stat_card(stats_frame, "New Registrations (Pending)", "--", "➕", "#E74C3C").grid(row=0, column=0)
    create_stat_card(stats_frame, "Pending Requests to Process", pending_requests, "📂", "#F1C40F").grid(row=0, column=1)
    create_stat_card(stats_frame, "Total Registered Residents", total_residents, "🏠", "#3498DB").grid(row=0, column=2)

    urgent_banner = ctk.CTkFrame(parent_frame, fg_color="#FADBD8", border_color="#E74C3C", border_width=1,
                                 corner_radius=10)
    urgent_banner.pack(fill="x", pady=(0, 20))
    urgent_label = ctk.CTkLabel(urgent_banner, text=f"You have '{pending_requests}' pending requests to process...",
                                font=ctk.CTkFont(size=14), text_color="#C03B2B", anchor="center")
    urgent_label.pack(pady=10, padx=20)

    ctk.CTkLabel(parent_frame, text="Quick Actions", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(
        fill="x", pady=(0, 10))
    actions_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    actions_frame.pack(fill="x")
    actions_frame.columnconfigure((0, 1, 2, 3), weight=1)

    def create_action_button(parent, text, color, command=None):
        cmd = command if command else lambda t=text: print(f"Quick action clicked: {t}")
        button = ctk.CTkButton(parent, text=text, fg_color=color, height=50, font=ctk.CTkFont(size=14, weight="bold"),
                               command=cmd)
        button.grid(sticky="ew", padx=10)
        return button

    create_action_button(actions_frame, "✅  Approve Residents", "#2ECC71", command=None).grid(row=0, column=0)
    create_action_button(actions_frame, "▶️  Process Requests", "#3498DB", command=None).grid(row=0, column=1)
    create_action_button(actions_frame, "👁️  View All Residents", "#3498DB", command=None).grid(row=0, column=2)
    create_action_button(actions_frame, "⚙️  Manage Staff", "#95A5A6", command=None).grid(row=0, column=3)


def show_request_management_content(parent_frame):
    """Displays all pending document requests from the database."""
    pending_requests = get_pending_requests()

    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    title_text = f"Pending Document Requests ({len(pending_requests)})"
    title_label = ctk.CTkLabel(scrollable_frame, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    title_label.pack(fill="x", pady=(0, 10))

    if not pending_requests:
        no_requests_banner = ctk.CTkFrame(scrollable_frame, fg_color="#D4EDDA", border_color="#28A745", border_width=1,
                                          corner_radius=10)
        no_requests_banner.pack(fill="x", pady=(20, 0))
        ctk.CTkLabel(no_requests_banner, text="✅ Good job! There are currently no pending requests to process.",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#155724", anchor="center").pack(pady=10,
                                                                                                           padx=20)
    else:
        container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
        container.pack(fill="x", pady=(0, 20))

        # Header
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure((1, 2), weight=1)
        header_frame.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(header_frame, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="RESIDENT NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1,
                                                                                               sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="DOCUMENT REQUESTED", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2,
                                                                                                    sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="ACTION", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="e",
                                                                                        padx=5)

        # Rows
        for request in pending_requests:
            row_frame = ctk.CTkFrame(container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure((1, 2), weight=1)
            row_frame.grid_columnconfigure(3, weight=0)

            ctk.CTkLabel(row_frame, text=f"#{request['id']}").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=request['full_name']).grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=request['document_name']).grid(row=0, column=2, sticky="w", padx=5)

            action_buttons_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_buttons_frame.grid(row=0, column=3, sticky="e")

            def view_action(req_id):
                print(f"View request {req_id}")

            def process_action(req_id):
                print(f"Process request {req_id}")

            def reject_action(req_id):
                print(f"Reject request {req_id}")

            ctk.CTkButton(action_buttons_frame, text="View", width=60, height=25, fg_color=VIEW_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=request['id']: view_action(id)).pack(side="left",
                                                                                                            padx=2)
            ctk.CTkButton(action_buttons_frame, text="Process", width=60, height=25, fg_color=APPROVE_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=request['id']: process_action(id)).pack(
                side="left", padx=2)
            ctk.CTkButton(action_buttons_frame, text="Reject", width=60, height=25, fg_color=REJECT_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=request['id']: reject_action(id)).pack(
                side="left", padx=2)


# ... (Rest of the file remains the same, including show_resident_accounts_content, show_staff_accounts_content, etc.)

# --- To run the application ---
if __name__ == "__main__":
    start_admin_dashboard()
