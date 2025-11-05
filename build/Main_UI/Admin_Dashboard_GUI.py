# Admin_Dashboard_GUI.py
import customtkinter as ctk
from PIL import Image, ImageTk
import io
import os
import requests
from database_connector import get_connection
from auth import (create_staff_account, send_rejection_email, send_approval_email, approve_verification_request, reject_verification_request,
                  send_finish_email, update_request_status, delete_request, get_finished_requests, get_request_details_with_resident, get_pending_requests)

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


button_widgets = {}

barangay_logo_pil = None
barangay_logo_ctk_image = None
barangay_logo_icon = None

def load_image_from_url(url, size):
    """
    Downloads an image from a URL and returns a CTkImage object.
    Returns None if loading fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an error for bad responses

        image_data = response.content
        pil_image = Image.open(io.BytesIO(image_data))
        
        ctk_image = ctk.CTkImage(pil_image, size=size)
        return ctk_image
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# --- ADD THIS CODE TO LOAD THE LOGO GLOBALLY ---
LOGO_URL = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/P2SERVE_LOGO.png"
print("Loading barangay logo from URL...")
barangay_logo_ctk_image = load_image_from_url(LOGO_URL, size=(40, 40))

if barangay_logo_ctk_image:
    print("Barangay logo loaded successfully.")
else:
    print("FAILED to load barangay logo. Check URL or internet connection.")

#----- dito kukunin yung total resident account
def get_total_residents_count():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM resident WHERE verification_status = 'approved'")
        row = cur.fetchone()
        return row[0] if row else 0
    except Exception as error:
        print(f"Error fetching total residents count: {error}")
        return 0
    finally:
        cur.close()
        conn.close()
#--- pending request ng docu informations
def get_pending_requests():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" SELECT dr.id, CONCAT(r.firstname, ' ', r.lastname) AS full_name, dr.document_name
            FROM document_requests dr
            JOIN resident r ON dr.user_id = r.id WHERE dr.status = 'Pending' """)  # Added WHERE
        rows = cur.fetchall()
        return [{"id": row[0], "full_name": row[1], "document_name": row[2]} for row in rows]
    except Exception as error:
        print(f"Error fetching pending requests: {error}")
        return []
    finally:
        cur.close()
        conn.close()
#---- Select lang yung existing staff if meron na
def get_existing_staff():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, full_name, username, position, role, status FROM staff")
        rows = cur.fetchall()
        return [{"id": row[0], "name": row[1], "username": row[2], "position": row[3], "role": row[4], "status": row[5]}
                for row in rows]
    except Exception as error:
        print(f"Error fetching staff: {error}")
        return []
    finally:
        cur.close()
        conn.close()

#----- dito kukunin yung information para mapalabas sa bar
def get_pending_residents():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, firstname, lastname, email, co_number FROM resident WHERE status = 'pending'")
        rows = cur.fetchall()
        return [{"id": row[0], "name": f"{row[1]} {row[2]}", "email": row[3], "contact": row[4]} for row in rows]
    except Exception as error:
        print(f"Error fetching pending residents: {error}")
        return []
    finally:
        cur.close()
        conn.close()
#----- bilang ng pending pa yung request
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
#-- count ng di pa verified na account
def get_pending_verify_count():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM resident WHERE verification_status = 'pending'")
        row = cur.fetchone()
        return row[0] if row else 0
    except Exception as error:
        print(f"Error fetching pending requests count: {error}")
        return 0
    finally:
        cur.close()
        conn.close()

# --- Content Creation Functions for Each Page ---
def show_request_management_content(parent_frame):
    def refresh_content():
        for widget in parent_frame.winfo_children():
            widget.destroy()
        show_request_management_content(parent_frame)

    pending_requests = get_pending_requests()
    finished_requests = get_finished_requests()

    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Pending Requests Section
    title_text = f"Pending Document Requests ({len(pending_requests)})"
    title_label = ctk.CTkLabel(scrollable_frame, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    title_label.pack(fill="x", pady=(0, 10))

    if not pending_requests:
        no_requests_banner = ctk.CTkFrame(scrollable_frame, fg_color="#D4EDDA", border_color="#28A745", border_width=1, corner_radius=10)
        no_requests_banner.pack(fill="x", pady=(20, 0))
        ctk.CTkLabel(no_requests_banner, text="✅ Good job! There are currently no pending requests to process.", font=ctk.CTkFont(size=14, weight="bold"), text_color="#155724", anchor="center").pack(pady=10, padx=20)
    else:
        container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
        container.pack(fill="x", pady=(0, 20))

        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure((1, 2), weight=1)
        header_frame.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(header_frame, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="RESIDENT NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="DOCUMENT REQUESTED", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="ACTION", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="e", padx=5)

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

            # Process button state tracking
            process_btn = ctk.CTkButton(action_buttons_frame, text="Process", width=60, height=25, fg_color=APPROVE_COLOR, font=ctk.CTkFont(size=10))
            process_btn.pack(side="left", padx=2)

            def view_action(req_id):
                details = get_request_details_with_resident(req_id)
                if not details:
                    ctk.CTkLabel(parent_frame, text="Error loading request details.", text_color="red").pack(pady=20)
                    return
                popup = ctk.CTkToplevel(parent_frame)
                popup.title("View Document Request")
                popup.geometry("800x550")
                popup.transient(parent_frame)
                popup.grab_set()
                popup.configure(fg_color="#ffffff")
                popup.config(bg="#ffffff")  # Force white background

                header_frame = ctk.CTkFrame(popup, fg_color=VIEW_COLOR, height=60, corner_radius=0)
                header_frame.pack(side="top", fill="x")
                header_frame.grid_columnconfigure(1, weight=1)
                if barangay_logo_ctk_image:
                    logo_label = ctk.CTkLabel(header_frame, text="", image=barangay_logo_ctk_image)
                    logo_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
                title_label = ctk.CTkLabel(header_frame, text=f"Document Request: {details['document_name']}",
                                           font=ctk.CTkFont(size=18, weight="bold"), text_color="white", anchor="w")
                title_label.grid(row=0, column=1, padx=(10, 20), pady=10, sticky="ew")

                main_content_frame = ctk.CTkFrame(popup, fg_color="transparent")
                main_content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                main_content_frame.grid_columnconfigure(0, weight=1)
                main_content_frame.grid_columnconfigure(1, weight=2)
                main_content_frame.grid_rowconfigure(0, weight=1)
                main_content_frame.grid_rowconfigure(1, weight=0)

                image_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
                image_frame.grid(row=0, column=0, padx=(0, 10), pady=(20, 10), sticky="nsew")
                image_display_size = 250
                image_label = ctk.CTkLabel(image_frame, text="No Image Provided", width=image_display_size,
                                           height=image_display_size, fg_color="transparent", corner_radius=10)
                image_label.pack(expand=True)
                if details['profile_picture']:
                    try:
                        pil_image = Image.open(details['profile_picture'])
                        ctk_image = ctk.CTkImage(pil_image, size=(image_display_size, image_display_size))
                        image_label.configure(text="", image=ctk_image)
                        image_label.image = ctk_image
                    except Exception as e:
                        image_label.configure(text=f"Error loading image.")

                info_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
                info_frame.grid(row=0, column=1, padx=(10, 0), pady=(20, 10), sticky="nsew")
                label_font = ctk.CTkFont(size=16, weight="bold")
                data_font = ctk.CTkFont(size=16)

                # Helper to display image or text
                # Helper to open enlarged image popup
                def open_image_popup(image_path):
                    if not image_path or not os.path.exists(image_path):
                        return
                    try:
                        pil_image = Image.open(image_path)
                        # Get original size or resize if too large (e.g., max 600x800)
                        max_width, max_height = 600, 800
                        pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                        popup = ctk.CTkToplevel(parent_frame)
                        popup.title("Enlarged Image")
                        popup.geometry(f"{pil_image.width}x{pil_image.height + 50}")  # Add space for button
                        popup.transient(parent_frame)
                        popup.grab_set()
                        popup.configure(fg_color="#ffffff")

                        # Display the image
                        ctk_image = ctk.CTkImage(pil_image, size=(pil_image.width, pil_image.height))
                        image_label = ctk.CTkLabel(popup, image=ctk_image, text="")
                        image_label.pack(pady=10)

                        # Close button
                        ctk.CTkButton(popup, text="Close", command=popup.destroy, fg_color=VIEW_COLOR).pack(pady=10)
                    except Exception as e:
                        print(f"Error opening image popup: {e}")

                # Helper to display image or text
                def display_file_or_text(file_path):
                    if file_path and os.path.exists(file_path) and file_path.lower().endswith(
                            ('.png', '.jpg', '.jpeg')):
                        try:
                            pil_img = Image.open(file_path)
                            pil_img.thumbnail((100, 100), Image.Resampling.LANCZOS)
                            ctk_img = ctk.CTkImage(light_image=pil_img, size=(pil_img.width, pil_img.height))
                            label = ctk.CTkLabel(info_frame, text="", image=ctk_img)
                            label.image = ctk_img
                            # Make clickable: bind click to open popup and change cursor
                            label.bind("<Button-1>", lambda e: open_image_popup(file_path))
                            label.configure(cursor="hand2")  # Hand cursor on hover
                            return label
                        except Exception:
                            return ctk.CTkLabel(info_frame, text="Error loading image", font=data_font,
                                                text_color="red")
                    else:
                        return ctk.CTkLabel(info_frame, text=file_path or 'N/A', font=data_font, text_color="black",
                                            wraplength=300)

                info_to_display = {
                    "Name:": f"{details['firstname']} {details['lastname']}",
                    "Age:": str(details['age']) if details['age'] else 'N/A',
                    "Gender:": details['gender'] or 'N/A',
                    "Address:": details['address'] or 'N/A',
                    "Valid ID:": display_file_or_text(details['valid_id']),
                    "2nd Valid ID:": display_file_or_text(details['second_valid_id']),
                    "DTI:": display_file_or_text(details['dti_path']),
                    "Proof of Payment:": display_file_or_text(details['prof_of_payment']),
                    "Purpose:": details['purpose'] or 'N/A'
                }
                for i, (label_text, data_widget) in enumerate(info_to_display.items(), start=1):
                    ctk.CTkLabel(info_frame, text=label_text, font=label_font, text_color="black", anchor="w").grid(
                        row=i, column=0, padx=(0, 10), pady=8, sticky="w")
                    if isinstance(data_widget, str):
                        ctk.CTkLabel(info_frame, text=data_widget, font=data_font, text_color="black", anchor="w",
                                     wraplength=300).grid(row=i, column=1, padx=(0, 10), pady=8, sticky="w")
                    else:
                        # Assume it's a widget (e.g., image label)
                        data_widget.grid(row=i, column=1, padx=(0, 10), pady=8, sticky="w")
                info_frame.grid_rowconfigure(len(info_to_display) + 1, weight=1)

                button_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
                button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")
                button_frame.grid_columnconfigure((0, 1, 2), weight=1)
                ctk.CTkButton(button_frame, text="Close", command=popup.destroy, fg_color=VIEW_COLOR,
                              hover_color=SIDEBAR_BTN_HOVER).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            def process_action(req_id, btn):
                if btn.cget("text") == "Process":
                    if update_request_status(req_id, 'Processing'):
                        btn.configure(text="Finish", fg_color="#F1C40F")
                    else:
                        ctk.CTkLabel(parent_frame, text="Error updating status.", text_color="red").pack(pady=10)
                elif btn.cget("text") == "Finish":
                    details = get_request_details_with_resident(req_id)
                    if update_request_status(req_id, 'Finished') and send_finish_email(details['email']):
                        refresh_content()
                    else:
                        ctk.CTkLabel(parent_frame, text="Error finishing request.", text_color="red").pack(pady=10)

            def reject_action(req_id):
                details = get_request_details_with_resident(req_id)
                if not details:
                    return
                reject_popup = ctk.CTkToplevel(parent_frame)
                reject_popup.title("Reject Request")
                reject_popup.geometry("400x300")
                reject_popup.transient(parent_frame)
                reject_popup.grab_set()
                ctk.CTkLabel(reject_popup, text="Reason for Rejection:", font=ctk.CTkFont(size=14)).pack(pady=(20, 10))
                reason_text = ctk.CTkTextbox(reject_popup, height=100)
                reason_text.pack(pady=(0, 20), padx=20, fill="x")

                def send_reject():
                    reason = reason_text.get("1.0", "end").strip()
                    if not reason:
                        ctk.CTkLabel(reject_popup, text="Please enter a reason.", text_color="red").pack(pady=10)
                        return
                    if send_rejection_email(details['email'], reason) and delete_request(req_id):
                        refresh_content()
                        reject_popup.destroy()  # Close the reject popup
                    else:
                        ctk.CTkLabel(parent_frame, text="Error rejecting request.", text_color="red").pack(pady=10)
                ctk.CTkButton(reject_popup, text="Send Rejection", command=send_reject).pack(pady=10)

            ctk.CTkButton(action_buttons_frame, text="View", width=60, height=25, fg_color=VIEW_COLOR, font=ctk.CTkFont(size=10), command=lambda id=request['id']: view_action(id)).pack(side="left", padx=2)
            process_btn.configure(command=lambda id=request['id'], b=process_btn: process_action(id, b))
            ctk.CTkButton(action_buttons_frame, text="Reject", width=60, height=25, fg_color=REJECT_COLOR, font=ctk.CTkFont(size=10), command=lambda id=request['id']: reject_action(id)).pack(side="left", padx=2)

    # Finished Requests Section
    finished_title_text = f"Finished Requests ({len(finished_requests)})"
    finished_title = ctk.CTkLabel(scrollable_frame, text=finished_title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    finished_title.pack(fill="x", pady=(20, 5))
    finished_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    finished_container.pack(fill="x", pady=(0, 20))
    if not finished_requests:
        ctk.CTkLabel(finished_container, text="No finished requests.", text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_finished = ctk.CTkFrame(finished_container, fg_color="transparent")
        header_frame_finished.pack(fill="x", padx=10, pady=(10, 5))
        header_frame_finished.grid_columnconfigure((1, 2), weight=1)
        ctk.CTkLabel(header_frame_finished, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_finished, text="RESIDENT NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_finished, text="DOCUMENT REQUESTED", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_finished, text="STATUS", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="e", padx=5)

        for request in finished_requests:
            row_frame = ctk.CTkFrame(finished_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure((1, 2), weight=1)
            row_frame.grid_columnconfigure(3, weight=0)
            ctk.CTkLabel(row_frame, text=f"#{request['id']}").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=request['full_name']).grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=request['document_name']).grid(row=0, column=2, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text="Finished", font=ctk.CTkFont(size=10, weight="bold"), fg_color=APPROVE_COLOR, text_color="white", corner_radius=5, width=60).grid(row=0, column=3, sticky="e", padx=5)

# --- Content Creation Functions for Each Page ---
def show_dashboard_content(parent_frame, navigate_callback):
    pending_requests = get_pending_requests_count()
    total_residents = get_total_residents_count()
    pending_verify_account = get_pending_verify_count()

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

    create_stat_card(stats_frame, "New Registrations (Pending)", pending_verify_account, "➕", "#E74C3C").grid(row=0, column=0)
    create_stat_card(stats_frame, "Pending Requests to Process", pending_requests, "📂", "#F1C40F").grid(row=0, column=1)
    create_stat_card(stats_frame, "Total Registered Residents", total_residents, "🏠", "#3498DB").grid(row=0, column=2)

    urgent_banner = ctk.CTkFrame(parent_frame, fg_color="#FADBD8", border_color="#E74C3C", border_width=1,corner_radius=10)
    urgent_banner.pack(fill="x", pady=(0, 20))
    urgent_label = ctk.CTkLabel(urgent_banner, text=f"You have '{pending_requests}' pending requests to process...",font=ctk.CTkFont(size=14), text_color="#C03B2B", anchor="center")
    urgent_label.pack(pady=10, padx=20)

    ctk.CTkLabel(parent_frame, text="Quick Actions", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(fill="x", pady=(0, 10))
    actions_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    actions_frame.pack(fill="x")
    actions_frame.columnconfigure((0, 1, 2, 3), weight=1)

    def create_action_button(parent, text, color, command=None):
        cmd = command if command else lambda t=text: print(f"Quick action clicked: {t}")
        button = ctk.CTkButton(parent, text=text, fg_color=color, height=50, font=ctk.CTkFont(size=14, weight="bold"), command=cmd)
        button.grid(sticky="ew", padx=10)
        return button
    create_action_button(actions_frame, "✅  Approve Residents", "#2ECC71", command=lambda: navigate_callback("residents")).grid(row=0, column=0)
    create_action_button(actions_frame, "▶️  Process Requests", "#3498DB", command=lambda: navigate_callback("requests")).grid(row=0, column=1)
    create_action_button(actions_frame, "👁️  View All Residents", "#3498DB", command=lambda: navigate_callback("residents")).grid(row=0, column=2)
    create_action_button(actions_frame, "⚙️  Manage Staff", "#95A5A6", command=lambda: navigate_callback("staff")).grid(row=0, column=3)


def show_resident_accounts_content(parent_frame):

    global barangay_logo_icon, barangay_logo_ctk_image

    def refresh_content():
        # Clear and reload the content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        show_resident_accounts_content(parent_frame)

    #------------DATABASE FUNCTION DITO KO MUNA NILAGAY HIHILO NA AKO E----------------
    def get_pending_verification_residents():
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, firstname, lastname, email FROM resident WHERE verification_status = 'pending'")
            rows = cur.fetchall()
            return [{"id": row[0], "name": f"{row[1]} {row[2]}", "email": row[3]} for row in rows]
        except Exception as error:
            print(f"Error fetching pending verification residents: {error}")
            return []
        finally:
            cur.close()
            conn.close()

    def get_approved_residents():
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, firstname, lastname, email FROM resident WHERE verification_status = 'approved'")
            rows = cur.fetchall()
            return [{"id": row[0], "name": f"{row[1]} {row[2]}", "email": row[3]} for row in rows]
        except Exception as error:
            print(f"Error fetching approved residents: {error}")
            return []
        finally:
            cur.close()
            conn.close()
        
    def view_action(res_id, parent_frame):
        global barangay_logo_icon, barangay_logo_ctk_image 

        user_data = get_full_user_data_by_id(res_id)
        
        if not user_data:
            print("No verification data found for resident_id:", res_id)
            return

        # --- 1. CREATE THE POPUP WINDOW ---
        popup = ctk.CTkToplevel(parent_frame)
        popup.title("Resident Verification")
        popup.geometry("800x550") 
        popup.grab_set()
        popup.configure(fg_color="white") 
        popup.resizable(False, False)
        
        if barangay_logo_icon:
            try:
                popup.iconphoto(True, barangay_logo_icon)
            except Exception as e:
                print(f"Failed to set window icon: {e}")

        # --- 2. CREATE NEW THEMED HEADER ---
        header_frame = ctk.CTkFrame(popup, fg_color=VIEW_COLOR, height=60, corner_radius=0)
        header_frame.pack(side="top", fill="x")
        header_frame.grid_columnconfigure(1, weight=1)

        if barangay_logo_ctk_image:
            logo_label = ctk.CTkLabel(header_frame, text="", image=barangay_logo_ctk_image)
            logo_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=f"Verification for: {user_data['firstname']} {user_data['lastname']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
            anchor="w"
        )
        title_label.grid(row=0, column=1, padx=(10, 20), pady=10, sticky="ew")

        # --- 3. CREATE MAIN CONTENT FRAME ---
        main_content_frame = ctk.CTkFrame(popup, fg_color="transparent")
        main_content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        main_content_frame.grid_columnconfigure(0, weight=1) 
        main_content_frame.grid_columnconfigure(1, weight=2) 
        main_content_frame.grid_rowconfigure(0, weight=1)    
        main_content_frame.grid_rowconfigure(1, weight=0)    

        # --- 4. CREATE FRAMES for Image, Info, Buttons ---
        image_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        image_frame.grid(row=0, column=0, padx=(0, 10), pady=(20, 10), sticky="nsew")
        image_frame.grid_rowconfigure(0, weight=1)
        image_frame.grid_columnconfigure(0, weight=1)

        info_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, padx=(10, 0), pady=(20, 10), sticky="nsew")
        info_frame.grid_columnconfigure(0, minsize=130) 
        info_frame.grid_columnconfigure(1, weight=1) 
        info_frame.grid_rowconfigure(0, weight=1) 

        button_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # --- 5. POPULATE IMAGE FRAME (No border) ---
        
        image_display_size = 250 # Set the desired size for the image
        
        image_label = ctk.CTkLabel(
            image_frame, 
            text="No Image Provided", 
            width=image_display_size,   # 250
            height=image_display_size,  # 250
            # --- MODIFICATION: Set background to transparent ---
            fg_color="transparent",
            corner_radius=10
        )
        image_label.grid(row=0, column=0, sticky="") # This centers the label

        image_path = user_data.get('profile_picture')
        if image_path:
            try:
                pil_image = Image.open(image_path)
                # --- MODIFICATION: Image size matches label size ---
                ctk_image = ctk.CTkImage(pil_image, size=(image_display_size, image_display_size)) 
                image_label.configure(text="", image=ctk_image) 
                image_label.image = ctk_image
            except Exception as e:
                print(f"Error loading image from path {image_path}: {e}")
                image_label.configure(text=f"Error loading image.")
        else:
             print(f"No image path found for resident {res_id}")

        # --- 6. POPULATE INFO FRAME (Left-aligned, centered) ---
        label_font = ctk.CTkFont(size=16, weight="bold")
        data_font = ctk.CTkFont(size=16) 
        
        info_to_display = {
            "Name:": f"{user_data['firstname']} {user_data['lastname']}",
            "Date of Birth:": user_data['dob'] or 'N/A',
            "Place of Birth:": user_data['place_of_birth'] or 'N/A',
            "Age:": user_data['age'] or 'N/A',
            "Civil Status:": user_data['civil_status'] or 'N/A',
            "Gender:": user_data['gender'] or 'N/A'
        }
        
        for i, (label_text, data_text) in enumerate(info_to_display.items(), start=1):
            ctk.CTkLabel(
                info_frame, 
                text=label_text, 
                font=label_font, 
                text_color="black", 
                anchor="w" 
            ).grid(row=i, column=0, padx=(0, 10), pady=8, sticky="w")
            
            ctk.CTkLabel(
                info_frame, 
                text=data_text, 
                font=data_font, 
                text_color="black", 
                anchor="w", 
                wraplength=300
            ).grid(row=i, column=1, padx=(0, 10), pady=8, sticky="w")
            
        info_frame.grid_rowconfigure(len(info_to_display) + 1, weight=1) 


        # --- 7. POPULATE BUTTON FRAME (No changes here) ---
        button_frame.grid_columnconfigure((0, 1, 2), weight=1) 

        ctk.CTkButton(
            button_frame, 
            text="Approve", 
            command=lambda id=res_id, email=user_data.get('email', ''): [approve_action(id, email), popup.destroy()],
            fg_color=APPROVE_COLOR,
            hover_color="darkgreen"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            button_frame, 
            text="Reject", 
            command=lambda id=res_id, email=user_data.get('email', ''): [reject_action(id, email), popup.destroy()],
            fg_color=REJECT_COLOR,
            hover_color="#B71C1C"
        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            button_frame, 
            text="Close", 
            command=popup.destroy,
            fg_color=VIEW_COLOR, 
            hover_color=SIDEBAR_BTN_HOVER
        ).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def approve_action(res_id, email):
        if approve_verification_request(res_id):
            if send_approval_email(email):  # Send verification approval email
                print(f"Approved verification for {res_id} and emailed {email}")
            else:
                print(f"Approved verification for {res_id} but failed to send email")
            refresh_content()
        else:
            print(f"Failed to approve verification for {res_id}")

    def reject_action(res_id, email):
        # Create rejection popup for reason
        popup = ctk.CTkToplevel(parent_frame)
        popup.title("Reject Verification")
        popup.geometry("400x300")
        popup.transient(parent_frame)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Reason for Rejection:", font=ctk.CTkFont(size=14)).pack(pady=(20, 10))
        reason_text = ctk.CTkTextbox(popup, height=100)
        reason_text.pack(pady=(0, 20), padx=20, fill="x")

        def send_reject():
            reason = reason_text.get("1.0", "end").strip()
            if not reason:
                ctk.CTkLabel(popup, text="Please enter a reason.", text_color="red").pack(pady=10)
                return
            if reject_verification_request(res_id):
                if send_rejection_email(email, reason):  # Send rejection email with reason
                    print(f"Rejected verification for {res_id} and emailed {email}")
                else:
                    print(f"Rejected verification for {res_id} but failed to send email")
                refresh_content()
            else:
                print(f"Failed to reject verification for {res_id}")
            popup.destroy()

        ctk.CTkButton(popup, text="Send Rejection", command=send_reject).pack(pady=10)
        
    # --- END OF HELPER FUNCTION DEFINITIONS ---

    pending_residents = get_pending_verification_residents()
    approved_residents = get_approved_residents()

    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True)

    pending_title_text = f"Pending Verification Requests ({len(pending_residents)})"
    pending_title = ctk.CTkLabel(scrollable_frame, text=pending_title_text, font=ctk.CTkFont(size=18, weight="bold"),
                                 anchor="w")
    pending_title.pack(fill="x", pady=(10, 5), padx=10)

    pending_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    pending_container.pack(fill="x", pady=(0, 20), padx=10)

    if not pending_residents:
        ctk.CTkLabel(pending_container, text="No pending verification requests.", text_color="gray",
                     font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_pending = ctk.CTkFrame(pending_container, fg_color="transparent")
        header_frame_pending.pack(fill="x", padx=10, pady=(10, 5))
        header_frame_pending.grid_columnconfigure((1, 2), weight=1)
        header_frame_pending.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(header_frame_pending, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="EMAIL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="ACTION", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="e", padx=5)

        for resident in pending_residents:
            row_frame = ctk.CTkFrame(pending_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure((1, 2), weight=1)
            row_frame.grid_columnconfigure(3, weight=0)

            ctk.CTkLabel(row_frame, text=f"#{resident['id']}").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['name']).grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['email']).grid(row=0, column=2, sticky="w", padx=5)

            action_buttons_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_buttons_frame.grid(row=0, column=3, sticky="e")
            
            # ---!!! ALL BUTTONS MOVED HERE, INSIDE THE LOOP !!!---
            
            # *** BUG FIX HERE: ***
            # Added 'parent_frame' to the view_action call
            ctk.CTkButton(action_buttons_frame, text="View", width=60, height=25, fg_color=VIEW_COLOR, font=ctk.CTkFont(size=10), 
                          command=lambda id=resident['id']: view_action(id, parent_frame)).pack(side="left", padx=2)
                          
            ctk.CTkButton(action_buttons_frame, text="Approve", width=60, height=25, fg_color=APPROVE_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=resident['id'], email=resident['email']: approve_action(id, email)).pack(
                side="left", padx=2)
                
            ctk.CTkButton(action_buttons_frame, text="Reject", width=60, height=25, fg_color=REJECT_COLOR, font=ctk.CTkFont(size=10),
                          command=lambda id=resident['id'], email=resident['email']: reject_action(id, email)).pack(
                side="left", padx=2)

    # --- "Verified Residents" Section (no changes needed here) ---
    approved_title_text = f"Verified Residents ({len(approved_residents)})"
    approved_title = ctk.CTkLabel(scrollable_frame, text=approved_title_text, font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    approved_title.pack(fill="x", pady=(20, 5), padx=10)

    approved_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    approved_container.pack(fill="x", pady=(0, 20), padx=10)

    if not approved_residents:
        ctk.CTkLabel(approved_container, text="No verified residents found.", text_color="gray",
                     font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_approved = ctk.CTkFrame(approved_container, fg_color="transparent")
        header_frame_approved.pack(fill="x", padx=10, pady=(10, 5))
        header_frame_approved.grid_columnconfigure((1, 2), weight=1)

        ctk.CTkLabel(header_frame_approved, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_approved, text="NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(header_frame_approved, text="EMAIL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=5)

        for resident in approved_residents:
            row_frame = ctk.CTkFrame(approved_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure((1, 2), weight=1)

            ctk.CTkLabel(row_frame, text=f"#{resident['id']}").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['name']).grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['email']).grid(row=0, column=2, sticky="w", padx=5)

def get_full_user_data_by_id(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # --- MODIFICATION: Added 'profile_picture' to the query ---
        cur.execute("""
            SELECT firstname, lastname, dob, place_of_birth, age, civil_status, gender, profile_picture_path
            FROM resident WHERE id = %s
        """, (resident_id,))
        row = cur.fetchone()
        
        if row:
            return {
                "firstname": row[0], "lastname": row[1], "dob": row[2], 
                "place_of_birth": row[3], "age": row[4], "civil_status": row[5], 
                "gender": row[6], "profile_picture": row[7] # --- MODIFICATION: Added new data ---
            }
        return None
    except Exception as error:
        print(f"Error fetching user data by ID: {error}")
        return None
    finally:
        cur.close()
        conn.close()


def show_staff_accounts_content(parent_frame):
    existing_staff = get_existing_staff()
    staff_roles = ["Admin", "Staff", "Treasurer"]
    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    create_frame = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    create_frame.pack(fill="x", pady=(0, 20), padx=0)
    ctk.CTkLabel(create_frame, text="Create New Staff Account", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(fill="x", padx=20, pady=(15, 10))

    form_grid = ctk.CTkFrame(create_frame, fg_color="transparent")
    form_grid.pack(fill="x", padx=20, pady=(0, 20))
    form_grid.columnconfigure(0, weight=1)

    def create_form_row(parent, label_text, widget_type="entry", options=None, show_char=None):
        ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", pady=(5, 2))
        if widget_type == "entry":
            entry = ctk.CTkEntry(parent, height=35, corner_radius=5, show=show_char)
            entry.pack(fill="x")
            return entry
        elif widget_type == "combobox":
            combobox = ctk.CTkComboBox(parent, height=35, corner_radius=5, values=options, state="readonly")
            combobox.pack(fill="x")
            combobox.set("-Select Role-")
            return combobox

    full_name_entry = create_form_row(form_grid, "Full Name")
    username_entry = create_form_row(form_grid, "Username")
    password_entry = create_form_row(form_grid, "Password (Temporary)", show_char="*")
    position_entry = create_form_row(form_grid, "Position (Optional)")
    role_combobox = create_form_row(form_grid, "Staff Role", widget_type="combobox", options=staff_roles)

    status_label = ctk.CTkLabel(form_grid, text="", font=ctk.CTkFont(size=12))
    status_label.pack(pady=(5, 0))

    def create_account_action():
        full_name = full_name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        position = position_entry.get().strip() or None
        role = role_combobox.get()

        if not full_name or not username or not password or role == "-Select Role-":
            status_label.configure(text="Please fill in all required fields.", text_color="red")
            return

        success, message = create_staff_account(full_name, username, password, position, role)
        if success:
            status_label.configure(text=message, text_color="green")
            # Clear fields
            full_name_entry.delete(0, 'end')
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            position_entry.delete(0, 'end')
            role_combobox.set("-Select Role-")
            # Refresh the list (optional: reload the page or update existing_staff)
        else:
            status_label.configure(text=message, text_color="red")

    create_button = ctk.CTkButton(form_grid, text="+ Create Account", height=40, font=ctk.CTkFont(weight="bold"), command=create_account_action)
    create_button.pack(fill="x", pady=(20, 5))

    existing_title_text = f"Existing Staff Accounts ({len(existing_staff)})"
    existing_title = ctk.CTkLabel(scrollable_frame, text=existing_title_text, font=ctk.CTkFont(size=18, weight="bold"),anchor="w")
    existing_title.pack(fill="x", pady=(10, 5), padx=0)

    existing_container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
    existing_container.pack(fill="x", pady=(0, 20), padx=0)

    if not existing_staff:
        ctk.CTkLabel(existing_container, text="No existing staff accounts found.", text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=20)
    else:
        header_frame_existing = ctk.CTkFrame(existing_container, fg_color="transparent", height=30)
        header_frame_existing.pack(fill="x", padx=10, pady=(10, 5))
        header_frame_existing.grid_columnconfigure((1, 2, 3), weight=1)
        header_frame_existing.grid_columnconfigure((0, 4, 5, 6), weight=0)

        headers = ["ID", "NAME", "USERNAME", "POSITION", "ROLE", "STATUS", "ACTION"]
        for i, header in enumerate(headers):
            sticky_val = "w" if i < len(headers) - 1 else "e"
            ctk.CTkLabel(header_frame_existing, text=header, font=ctk.CTkFont(weight="bold", size=11)).grid(row=0,column=i,sticky=sticky_val,padx=5)

        for staff in existing_staff:
            row_frame = ctk.CTkFrame(existing_container, fg_color="transparent", height=30)
            row_frame.pack(fill="x", padx=10, pady=2)
            row_frame.grid_columnconfigure((1, 2, 3), weight=1)
            row_frame.grid_columnconfigure((0, 4, 5, 6), weight=0)

            ctk.CTkLabel(row_frame, text=f"#{staff['id']}", font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w",padx=5)
            ctk.CTkLabel(row_frame, text=staff['name'], font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=1,sticky="ew", padx=5)
            ctk.CTkLabel(row_frame, text=staff['username'], font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=2,sticky="ew",padx=5)
            ctk.CTkLabel(row_frame, text=staff['position'] or "-", font=ctk.CTkFont(size=11), anchor="w").grid(row=0,column=3,sticky="ew",padx=5)

            role_label = ctk.CTkLabel(row_frame, text=staff['role'], font=ctk.CTkFont(size=10, weight="bold"), corner_radius=5, width=50)
            role_label.grid(row=0, column=4, sticky="w", padx=5)
            role_color = REJECT_COLOR if staff['role'].lower() == 'admin' else VIEW_COLOR
            role_label.configure(fg_color=role_color, text_color="white")

            status_label = ctk.CTkLabel(row_frame, text=staff['status'], font=ctk.CTkFont(size=10, weight="bold"), corner_radius=5, width=50)
            status_label.grid(row=0, column=5, sticky="w", padx=5)
            status_color = APPROVE_COLOR if staff['status'].lower() == 'active' else DEACTIVATE_COLOR
            status_label.configure(fg_color=status_color, text_color="white")

            action_buttons_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_buttons_frame.grid(row=0, column=6, sticky="e")

            def view_staff_action(staff_id):
                print(f"View staff {staff_id}")

            ctk.CTkButton(action_buttons_frame, text="View", width=50, height=25, fg_color=VIEW_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=staff['id']: view_staff_action(id)).pack(
                side="left", padx=2)

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

    global barangay_logo_pil, barangay_logo_ctk_image, barangay_logo_icon
    
    print("Creating Tkinter images from PIL image...")
    if barangay_logo_pil:
        try:
            # NOW it's safe to create these because 'root' exists
            barangay_logo_ctk_image = ctk.CTkImage(barangay_logo_pil.copy(), size=(40, 40))
            barangay_logo_icon = ImageTk.PhotoImage(barangay_logo_pil.copy())
            print("Barangay logo and icon created successfully.")
            
            # Set the main window icon right away
            root.iconphoto(True, barangay_logo_icon)
        except Exception as e:
            print(f"Error creating Tkinter images: {e}")
    else:
        print("Skipping Tkinter image creation, PIL image not loaded.")
    # --- END OF IMAGE CONVERSION ---

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

        if page_key == "dashboard": show_dashboard_content(dynamic_content_frame, navigate_to)
        elif page_key == "requests": show_request_management_content(dynamic_content_frame)
        elif page_key == "residents": show_resident_accounts_content(dynamic_content_frame)
        elif page_key == "staff": show_staff_accounts_content(dynamic_content_frame)
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