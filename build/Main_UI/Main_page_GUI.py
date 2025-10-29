# Main_page_GUI.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
from database_connector import get_connection
from PIL import Image, ImageTk
import requests
from io import BytesIO
from auth import get_user_id_by_username, insert_document_request, get_full_user_data, submit_verification_request

current_username = None


# --- DATABASE FUNCTIONS ---
def get_current_user_data(username):
    print(f"Fetching data for username: {username}")  # para sa debugging
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT firstname, lastname, profile_picture_path
            FROM resident
            WHERE username = %s
        """, (username,))
        row = cur.fetchone()
        print(f"Query result: {row}")  # para sa debugging
        if row:
            return {
                "firstname": row[0],
                "lastname": row[1],
                "profile_picture_path": row[2]
            }
        return None
    except Exception as error:
        print(f"Error fetching user data: {error}")
        return None
    finally:
        cur.close()
        conn.close()


def save_user_profile_data(picture_path):
    global current_username
    if not current_username:
        return False
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" UPDATE resident
            SET profile_picture_path = %s
            WHERE username = %s""",
            (picture_path, current_username))
        conn.commit()
        print(f"Profile picture path saved for {current_username}: {picture_path}")  # para sa debugging
        return True
    except Exception as error:
        print(f"Error saving profile data: {error}")
        return False
    finally:
        cur.close()
        conn.close()


def get_user_status_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT verification_status FROM resident WHERE username = %s", (username,))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as error:
        print(f"Error fetching user status: {error}")
        return None
    finally:
        cur.close()
        conn.close()


# --- PAGE CREATION FUNCTIONS ---

def create_home_page(parent_frame):
    """Creates the content for the Home page."""
    content_label = ctk.CTkLabel(parent_frame, text="Welcome to the Home Page Content Area.", font=ctk.CTkFont(size=20), text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")


def create_about_us_page(parent_frame):
    """Creates the content for the About Us page."""
    content_label = ctk.CTkLabel(parent_frame, text="This is the About Us page.", font=ctk.CTkFont(size=20), text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")


def create_contact_us_page(parent_frame):
    """Creates the content for the Contact Us page."""
    content_label = ctk.CTkLabel(parent_frame, text="Contact information goes here.", font=ctk.CTkFont(size=20), text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")


def create_services_page(parent_frame):
    """Creates the services page with document request functionality."""
    selected_info = {"widget": None, "document_name": None}
    uploaded_files = {}
    text_inputs = {}
    BTN_UNSELECTED_COLOR = "#3498db"
    BTN_SELECTED_COLOR = "#28A745"
    BTN_HOVER_COLOR = "#5dade2"

    # This stores the default text color, which we'll need for the placeholder
    placeholder_color = "gray"
    # Try to get the system's default text color
    try:
        default_text_color = ctk.ThemeManager.theme["CTkTextbox"]["text_color"]
    except:
        default_text_color = ("#000", "#FFF") # Fallback color

    # --- (requirements_data remains the same as last time) ---
    requirements_data = {
        "Barangay Clearance": {
            "title": "Barangay Clearance Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., For employment, for travel, etc.", "text"),
            ]
        },
            "Barangay Building Clearance": {
                "title": "Barangay Building Clearance Requirements",
                "content": [
            ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
            ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
            ("DTI Registration", "Upload a clear picture or copy of your DTI certificate.", "file"),
            ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
            ("Purpose of Request", "e.g., For building construction permit.", "text"),
        ]
        },
        "Barangay Business Clearance": {
            "title": "Barangay Business Clearance Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("DTI Registration", "Upload a clear picture or copy of your DTI certificate.", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., For new business, or renewal.", "text"),
            ]
        },
        "Certificate of First Time Jobseeker": {
            "title": "Certificate of First Time Jobseeker Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., For local employment application.", "text"),
            ]
        },
        "Certificate of Indigency": {
            "title": "Certificate of Indigency Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., For medical assistance, financial aid.", "text"),
            ]
        },
        "Certificate of Residency": {
            "title": "Certificate of Residency Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., For proof of address, school enrollment.", "text"),
            ]
        },
        "Oath of Undertaking - First Time Jobseeker": {
            "title": "Oath of Undertaking Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., To avail of RA 11261 benefits.", "text"),

            ]
        },
        "Order of Payment for Barangay Business Clearance": {
            "title": "Order of Payment Requirements",
            "content": [
                ("Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("2nd Valid ID", "Upload a clear image of any Government Issued ID addressed to Poblacion 2 (e.g., Driver's License, Voter's ID, Postal ID)", "file"),
                ("DTI Registration", "Upload a clear picture or copy of your DTI certificate.", "file"),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation.", "file"),
                ("Purpose of Request", "e.g., To get order of payment for business.", "text"),
            ]
        },
    }

    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=40, pady=20)
    button_container_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    button_container_frame.pack(fill="x", expand=True)
    requirements_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    requirements_frame.pack(fill="x", expand=True, pady=(20, 0))
    title_label = ctk.CTkLabel(button_container_frame, text="Request a Document (Click to Select)",
                               font=ctk.CTkFont(size=24, weight="bold"), text_color="black")
    title_label.pack(anchor="w", pady=(0, 20))


    # --- TOOLTIP WIDGET AND FUNCTIONS ---
    root_window = parent_frame.winfo_toplevel()
    tooltip_label = ctk.CTkLabel(
        root_window,
        text="",
        fg_color=("#333", "#CCC"),
        text_color=("white", "black"),
        corner_radius=6,
        font=ctk.CTkFont(size=12),
        wraplength=300,
        justify="left"
    )

    def show_tooltip(widget_to_follow, text):
        tooltip_label.configure(text=text)
        widget_screen_x = widget_to_follow.winfo_rootx()
        widget_screen_y = widget_to_follow.winfo_rooty()
        widget_width = widget_to_follow.winfo_width()
        root_screen_x = root_window.winfo_rootx()
        root_screen_y = root_window.winfo_rooty()
        window_rel_x = widget_screen_x - root_screen_x
        window_rel_y = widget_screen_y - root_screen_y
        final_x = window_rel_x + widget_width + 5
        final_y = window_rel_y - 2
        tooltip_label.update_idletasks()
        if final_x + tooltip_label.winfo_width() > root_window.winfo_width():
            final_x = window_rel_x - tooltip_label.winfo_width() - 5
        tooltip_label.place(x=final_x, y=final_y)

    def hide_tooltip(event=None):
        tooltip_label.place_forget()
    # --- END OF TOOLTIP CODE ---


    def show_info_popup(title, message):
        popup = ctk.CTkToplevel(parent_frame)
        popup.title(title)
        popup.geometry("450x250")
        popup.transient(parent_frame.winfo_toplevel())
        popup.grab_set()
        ctk.CTkLabel(popup, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(popup, text=message, font=ctk.CTkFont(size=14), wraplength=400, justify="left").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy).pack(pady=20)


    # --- NEW: PLACEHOLDER HELPER FUNCTIONS ---
    def on_textbox_focus_in(event, textbox, placeholder_text):
        """Removes placeholder text on focus."""
        if textbox.get("1.0", "end-1c").strip() == placeholder_text:
            textbox.delete("1.0", "end")
            textbox.configure(text_color=default_text_color)

    def on_textbox_focus_out(event, textbox, placeholder_text):
        """Adds placeholder text if field is empty on focus out."""
        if not textbox.get("1.0", "end-1c").strip():
            textbox.insert("1.0", placeholder_text)
            textbox.configure(text_color=placeholder_color)
    # --- END OF NEW FUNCTIONS ---


    # --- MODIFIED: submit_all_documents now checks for placeholder text ---
    def submit_all_documents():
        doc_name = selected_info.get("document_name")
        if not doc_name: return

        expected_files = []
        expected_texts = {}  # Store as dict to hold placeholder

        for item in requirements_data[doc_name]["content"]:
            if len(item) == 3:
                subtitle, text, req_type = item
            else:
                subtitle, text = item
                req_type = "file"

            if req_type == "file":
                expected_files.append(subtitle)
            elif req_type == "text":
                expected_texts[subtitle] = text  # Key = name, Value = placeholder

        # Check for missing files
        missing_files = [req for req in expected_files if req not in uploaded_files]
        if missing_files:
            show_info_popup("Incomplete Requirements", "Please upload all required files. Missing:\n\n" + "\n".join(
                f"• {req}" for req in missing_files))
            return

        # Get text inputs and check for missing ones
        purpose_text = ""
        missing_texts = []

        for req_name, placeholder in expected_texts.items():
            textbox_widget = text_inputs.get(req_name)
            if textbox_widget:
                text_content = textbox_widget.get("1.0", "end-1c").strip()

                # Check if empty OR still has placeholder
                if not text_content or text_content == placeholder:
                    missing_texts.append(req_name)
                else:
                    if req_name == "Purpose of Request":
                        purpose_text = text_content
            else:
                missing_texts.append(req_name)

        if missing_texts:
            show_info_popup("Incomplete Requirements", "Please fill in all required fields. Missing:\n\n" + "\n".join(
                f"• {req}" for req in missing_texts))
            return

        # Proceed with submission
        global current_username
        user_id = get_user_id_by_username(current_username)
        if not user_id:
            show_info_popup("Error", "Unable to identify user. Please log in again.")
            return

        # Collect both ID paths
        valid_id_path = uploaded_files.get("Valid ID")
        second_valid_id_path = uploaded_files.get("2nd Valid ID")
        prof_of_payment_path = uploaded_files.get("Proof of Payment")
        dti_path = uploaded_files.get("DTI Registration")

        # Insert with both IDs and purpose
        if insert_document_request(user_id, doc_name, valid_id_path, second_valid_id_path, dti_path, prof_of_payment_path, purpose_text):
            show_info_popup("Submission Successful",
                            f"Your request for '{doc_name}' has been submitted and is pending approval.")
            # Reset form after submission
            display_requirements(doc_name)
        else:
            show_info_popup("Error", "Failed to submit request. Please try again.")


    def handle_upload(status_label, preview_label, requirement_name):
        filetypes = (("Image Files", "*.png *.jpg *.jpeg"), ("PDF Files", "*.pdf"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title=f"Upload for {requirement_name}", filetypes=filetypes)

        if not filepath:
            return

        filename = os.path.basename(filepath)
        uploaded_files[requirement_name] = filepath

        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(filepath)
                img.thumbnail((100, 100), Image.Resampling.LANCZOS)
                preview_img = ctk.CTkImage(light_image=img, size=(img.width, img.height))
                preview_label.configure(image=preview_img, text="")
                preview_label.image = preview_img
                status_label.configure(text=f"Uploaded: {filename}", text_color="green")
            except Exception as e:
                preview_label.configure(image=None, text="Invalid Image")
                status_label.configure(text=f"Error: {filename}", text_color="red")
        else:
            preview_label.configure(image=None, text="No Preview\n(PDF/File)")
            status_label.configure(text=f"Uploaded: {filename}", text_color="green")


    # --- MODIFIED: display_requirements now adds border and placeholder ---
    def display_requirements(document_name):
        uploaded_files.clear()
        text_inputs.clear()
        hide_tooltip()
        for widget in requirements_frame.winfo_children(): widget.destroy()

        req_info = requirements_data.get(document_name)
        if not req_info: return

        ctk.CTkFrame(requirements_frame, height=2, fg_color="#E0E0E0").pack(fill="x", pady=(10, 20))
        ctk.CTkLabel(requirements_frame, text=req_info["title"], font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#333").pack(anchor="w", pady=(0, 15))

        for item in req_info["content"]:
            if len(item) == 3:
                subtitle, text, req_type = item
            else:
                subtitle, text = item
                req_type = "file"

            title_frame = ctk.CTkFrame(requirements_frame, fg_color="transparent")
            title_frame.pack(fill="x", pady=(10, 2), anchor="w")

            ctk.CTkLabel(title_frame, text=subtitle, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
                side="left", anchor="w")

            info_icon = ctk.CTkLabel(
                title_frame,
                text=" ⓘ",
                font=ctk.CTkFont(size=14),
                text_color="#007BFF"
            )
            info_icon.pack(side="left", padx=5, anchor="w")
            info_icon.bind("<Enter>", lambda event, icon=info_icon, t=text: show_tooltip(icon, t))
            info_icon.bind("<Leave>", hide_tooltip)

            if req_type == "file":
                # --- FILE UPLOAD block ---
                preview_label = ctk.CTkLabel(requirements_frame, text="No Preview", fg_color="#EAEAEA", width=100,
                                             height=100, corner_radius=8, text_color="gray")
                preview_label.pack(pady=(5, 5), padx=(15, 0), anchor="w")

                upload_frame = ctk.CTkFrame(requirements_frame, fg_color="transparent")
                upload_frame.pack(fill="x", padx=(15, 0), pady=(5, 15))
                file_status_label = ctk.CTkLabel(upload_frame, text="No file selected.", font=ctk.CTkFont(size=12),
                                                 text_color="gray")
                upload_button = ctk.CTkButton(upload_frame, text="Upload File", width=120)

                upload_button.configure(
                    command=lambda s_lbl=file_status_label, p_lbl=preview_label, req_name=subtitle: handle_upload(s_lbl,
                                                                                                                  p_lbl,
                                                                                                                  req_name))

                upload_button.pack(side="left", anchor="w")
                file_status_label.pack(side="left", anchor="w", padx=10)

            elif req_type == "text":
                # --- MODIFIED TEXT BOX block ---
                textbox = ctk.CTkTextbox(
                    requirements_frame,
                    height=80,
                    corner_radius=8,
                    font=ctk.CTkFont(size=13),
                    border_width=1,          # <-- ADDED BORDER
                    border_color="#9A9A9A"   # <-- ADDED BORDER COLOR
                )
                textbox.pack(fill="x", pady=(5, 15), padx=(15, 0))

                # Add placeholder text and color
                textbox.insert("1.0", text)
                textbox.configure(text_color=placeholder_color)

                # Bind focus events for placeholder logic
                textbox.bind("<FocusIn>", lambda event, tb=textbox, ph=text: on_textbox_focus_in(event, tb, ph))
                textbox.bind("<FocusOut>", lambda event, tb=textbox, ph=text: on_textbox_focus_out(event, tb, ph))

                text_inputs[subtitle] = textbox

        ctk.CTkButton(requirements_frame, text="Submit All Documents", font=ctk.CTkFont(size=16, weight="bold"),
                      height=50, command=submit_all_documents).pack(fill="x", pady=(30, 10))
        scrollable_frame.update_idletasks()
        scrollable_frame._parent_canvas.yview_moveto(1.0)
    # --- END OF MODIFIED FUNCTION ---


    def select_document(document_name, clicked_button):
        global current_username
        user_status = get_user_status_by_username(current_username)
        if user_status != 'approved':
            show_info_popup("Access Denied", "Please verify your account first before requesting documents.")
            return

        if selected_info["widget"] is not None: selected_info["widget"].configure(fg_color=BTN_UNSELECTED_COLOR)
        clicked_button.configure(fg_color=BTN_SELECTED_COLOR)
        selected_info["widget"] = clicked_button
        selected_info["document_name"] = document_name
        display_requirements(document_name)

    documents = list(requirements_data.keys())
    for doc_name in documents:
        doc_button = ctk.CTkButton(button_container_frame, text=doc_name, fg_color=BTN_UNSELECTED_COLOR,
                                   hover_color=BTN_HOVER_COLOR, font=ctk.CTkFont(size=14), corner_radius=16,
                                   height=40, anchor="w")
        doc_button.configure(command=lambda name=doc_name, btn=doc_button: select_document(name, btn))
        doc_button.pack(fill="x", pady=4)

def create_profile_page(parent_frame):
    """Creates the profile page with data display and additional info inputs for verification."""
    global current_username
    if not current_username:
        ctk.CTkLabel(parent_frame, text="Please log in first.", text_color="red").pack(pady=20)
        return

    # Fetch full user data including new verification fields
    user = get_full_user_data(current_username)
    if not user:
        ctk.CTkLabel(parent_frame, text="Error loading profile data.", text_color="red").pack(pady=20)
        return

    new_picture_path = {"path": user.get("profile_picture_path")}

    # --- Main container frame ---
    profile_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    profile_scrollable = ctk.CTkScrollableFrame(profile_frame, fg_color="transparent")
    profile_scrollable.pack(fill="both", expand=True)
    profile_frame.pack(fill="both", expand=True, padx=50, pady=30)

    # Configure grid layout within the scrollable frame
    profile_scrollable.grid_columnconfigure(1, weight=1)

    # --- Title ---
    title_label = ctk.CTkLabel(profile_scrollable, text="User Profile", font=ctk.CTkFont(size=24, weight="bold"))
    title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

    # --- Left Column: Profile Picture ---
    pfp_container = ctk.CTkFrame(profile_scrollable, fg_color="transparent")
    pfp_container.grid(row=1, column=0, sticky="nw", padx=(0, 30))
    pfp_frame = ctk.CTkFrame(pfp_container, fg_color="#f0f0f0", width=200, height=200, corner_radius=10)
    pfp_frame.pack(pady=(0, 10));
    pfp_frame.pack_propagate(False)
    pfp_label = ctk.CTkLabel(pfp_frame, text="", font=ctk.CTkFont(size=14), text_color="gray");
    pfp_label.pack(expand=True)
    upload_btn = ctk.CTkButton(pfp_container, text="Upload Picture");
    upload_btn.pack(fill="x")

    # --- Right Column: User Details ---
    details_frame = ctk.CTkFrame(profile_scrollable, fg_color="transparent")
    details_frame.grid(row=1, column=1, sticky="nsew");
    details_frame.grid_columnconfigure(1, weight=1)

    current_row = 0

    # --- Display Existing Info (Labels) ---
    ctk.CTkLabel(details_frame, text="First Name:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=current_row, column=0, sticky="w", padx=(0, 10), pady=5)
    ctk.CTkLabel(details_frame, text=user.get("firstname", "N/A"), font=ctk.CTkFont(size=14)).grid(row=current_row, column=1, sticky="w", pady=5)
    current_row += 1

    ctk.CTkLabel(details_frame, text="Last Name:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=current_row, column=0, sticky="w", padx=(0, 10), pady=10)
    ctk.CTkLabel(details_frame, text=user.get("lastname", "N/A"), font=ctk.CTkFont(size=14)).grid(row=current_row, column=1, sticky="w", pady=10)
    current_row += 1

    # --- Separator ---
    separator = ctk.CTkFrame(details_frame, height=2, fg_color="#E0E0E0")
    separator.grid(row=current_row, column=0, columnspan=2, sticky="ew", pady=(20, 10));
    current_row += 1

    # --- Additional Information Section ---
    add_info_label = ctk.CTkLabel(details_frame, text="Additional Information (Required for Verification)",
                                  font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
    add_info_label.grid(row=current_row, column=0, columnspan=2, sticky="ew", pady=(0, 15));
    current_row += 1

    # Check verification status
    verification_status = user.get("verification_status", "not_verified")
    is_approved = verification_status == "approved"
    is_pending = verification_status == "pending"

    # --- Input Fields or Labels Based on Status ---
    fields = {}

    # DOB
    ctk.CTkLabel(details_frame, text="Date of Birth (YYYY-MM-DD):", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").grid(row=current_row, column=0, sticky="w", padx=(0, 10), pady=5)
    if is_approved:
        ctk.CTkLabel(details_frame, text=user.get("dob", "N/A"), font=ctk.CTkFont(size=14)).grid(row=current_row, column=1, sticky="w", pady=5)
    else:
        dob_entry = ctk.CTkEntry(details_frame, placeholder_text="YYYY-MM-DD", font=ctk.CTkFont(size=14), corner_radius=5)
        dob_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        if user.get("dob"): dob_entry.insert(0, user["dob"])
        fields["dob"] = dob_entry
    current_row += 1

    # Place of Birth
    ctk.CTkLabel(details_frame, text="Place of Birth:", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").grid(row=current_row, column=0, sticky="w", padx=(0, 10), pady=5)
    if is_approved:
        ctk.CTkLabel(details_frame, text=user.get("place_of_birth", "N/A"), font=ctk.CTkFont(size=14)).grid(
            row=current_row, column=1, sticky="w", pady=5)
    else:
        pob_entry = ctk.CTkEntry(details_frame, font=ctk.CTkFont(size=14), corner_radius=5)
        pob_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        if user.get("place_of_birth"): pob_entry.insert(0, user["place_of_birth"])
        fields["place_of_birth"] = pob_entry
    current_row += 1

    # Age
    age_options = ["-Select Age-"] + [str(i) for i in range(18, 101)]
    ctk.CTkLabel(details_frame, text="Age:", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").grid(row=current_row, column=0, sticky="w", padx=(0, 10), pady=5)
    if is_approved:
        ctk.CTkLabel(details_frame, text=str(user.get("age", "N/A")), font=ctk.CTkFont(size=14)).grid(row=current_row, column=1, sticky="w", pady=5)
    else:
        age_combobox = ctk.CTkComboBox(details_frame, font=ctk.CTkFont(size=14), corner_radius=5, values=age_options, state="readonly")
        current_value = str(user.get("age")) if user.get("age") is not None else None
        if current_value in age_options:
            age_combobox.set(current_value)
        else:
            age_combobox.set("-Select Age-")
        age_combobox.grid(row=current_row, column=1, sticky="ew", pady=5)
        fields["age"] = age_combobox
    current_row += 1

    # Civil Status
    civil_status_options = ["-Select-", "Single", "Married", "Widowed", "Separated"]
    ctk.CTkLabel(details_frame, text="Civil Status:", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").grid(
        row=current_row, column=0, sticky="w", padx=(0, 10), pady=5)
    if is_approved:
        ctk.CTkLabel(details_frame, text=user.get("civil_status", "N/A"), font=ctk.CTkFont(size=14)).grid(
            row=current_row, column=1, sticky="w", pady=5)
    else:
        civil_status_combobox = ctk.CTkComboBox(details_frame, font=ctk.CTkFont(size=14), corner_radius=5, values=civil_status_options, state="readonly")
        current_value = user.get("civil_status")
        if current_value in civil_status_options:
            civil_status_combobox.set(current_value)
        else:
            civil_status_combobox.set("-Select-")
        civil_status_combobox.grid(row=current_row, column=1, sticky="ew", pady=5)
        fields["civil_status"] = civil_status_combobox
    current_row += 1

    # Gender
    gender_options = ["-Select-", "Male", "Female", "Other", "Prefer not to say"]
    ctk.CTkLabel(details_frame, text="Gender:", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").grid( row=current_row, column=0, sticky="w", padx=(0, 10), pady=5)
    if is_approved:
        ctk.CTkLabel(details_frame, text=user.get("gender", "N/A"), font=ctk.CTkFont(size=14)).grid(row=current_row, column=1, sticky="w", pady=5)
    else:
        gender_combobox = ctk.CTkComboBox(details_frame, font=ctk.CTkFont(size=14), corner_radius=5, values=gender_options, state="readonly")
        current_value = user.get("gender")
        if current_value in gender_options:
            gender_combobox.set(current_value)
        else:
            gender_combobox.set("-Select-")
        gender_combobox.grid(row=current_row, column=1, sticky="ew", pady=5)
        fields["gender"] = gender_combobox
    current_row += 1

    # --- Status Label ---
    status_label = ctk.CTkLabel(details_frame, text="", font=ctk.CTkFont(size=12));
    status_label.grid(row=current_row, column=0, columnspan=2, sticky="w", pady=(10, 5));
    current_row += 1

    # --- Submit Button (Only if not approved and not pending) ---
    if not is_approved and not is_pending:
        submit_info_btn = ctk.CTkButton(details_frame, text="Verify Account",
                                        command=lambda: submit_verification(fields, status_label))
        submit_info_btn.grid(row=current_row, column=0, columnspan=2, sticky="w", pady=(20, 0));
        current_row += 1
    elif is_pending:
        ctk.CTkLabel(details_frame, text="Verification is in process. Please wait for admin approval.", font=ctk.CTkFont(size=12, weight="bold"), text_color="orange").grid(row=current_row, column=0, columnspan=2, sticky="w", pady=(20, 0));
        current_row += 1

    # --- Functions ---
    def submit_verification(fields, status_label):
        dob = fields["dob"].get().strip()
        pob = fields["place_of_birth"].get().strip()
        age = fields["age"].get()
        civil_status = fields["civil_status"].get()
        gender = fields["gender"].get()

        if not dob or not pob or age == "-Select Age-" or civil_status == "-Select-" or gender == "-Select-":
            status_label.configure(text="Error: Please fill all additional information fields.", text_color="red")
            return

        success = submit_verification_request(current_username, dob, pob, int(age), civil_status, gender)
        if success:
            status_label.configure(text="Verification submitted successfully!", text_color="green")
            # Refresh page to show pending status
            for widget in parent_frame.winfo_children(): widget.destroy()
            create_profile_page(parent_frame)
        else:
            status_label.configure(text="Error: Could not submit verification.", text_color="red")

    def display_image(image_path):
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path); ctk_img = ctk.CTkImage(light_image=img, size=(200, 200)); pfp_label.configure( image=ctk_img, text=""); pfp_label.image = ctk_img
            except Exception as e:
                pfp_label.configure(image=None, text=f"Error:\n{e}")
        else:
            pfp_label.configure(image=None, text="No Image")

    def upload_picture():
        filepath = filedialog.askopenfilename(title="Select Profile Picture", filetypes=(("Image Files", "*.png *.jpg *.jpeg"),))
        if filepath:
            new_picture_path["path"] = filepath
            display_image(filepath)
            # Save picture path
            from auth import update_user_profile_by_username
            update_user_profile_by_username(current_username, user["firstname"], user["lastname"], filepath)

    upload_btn.configure(command=upload_picture)
    display_image(new_picture_path["path"])

# =============================================================================
# --- MAIN APPLICATION ---
# =============================================================================

def start_mainhomepage(username=None):
    """Starts the main homepage, accepting an optional username."""
    global current_username
    current_username = username
    print(f"Starting main page with username: {current_username}")  # Debug print

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("P2SERVE")
    width, height = 1000, 650
    root.geometry(f"{width}x{height}")
    HEADER_BG, NAV_INACTIVE_COLOR, NAV_ACTIVE_COLOR, TEXT_COLOR = "#3498db", "#FFD700", "#E74C3C", "black"

    def navigate_to(page_name):
        for widget in content_frame.winfo_children(): widget.destroy()
        if page_name == "Home":
            create_home_page(content_frame)
        elif page_name == "About Us":
            create_about_us_page(content_frame)
        elif page_name == "Contact Us":
            create_contact_us_page(content_frame)
        elif page_name == "Services":
            create_services_page(content_frame)
        elif page_name == "Profile":
            create_profile_page(content_frame)  # No username parameter needed now
        buttons = {"Home": home_btn, "About Us": about_btn, "Contact Us": contact_btn, "Services": services_btn,
                   "Profile": profile_btn}
        for name, btn in buttons.items():
            if name == page_name:
                if name in ["Home", "About Us", "Contact Us", "Services"]:
                    btn.configure(fg_color=NAV_ACTIVE_COLOR, text_color="white", hover_color=NAV_ACTIVE_COLOR)
                else:
                    btn.configure(text_color_disabled="white")
            else:
                if name in ["Home", "About Us", "Contact Us", "Services"]:
                    btn.configure(fg_color=NAV_INACTIVE_COLOR, text_color=TEXT_COLOR, hover_color="#F39C12")
                else:
                    btn.configure(text_color_disabled="#d0d0d0")

    header_frame = ctk.CTkFrame(root, height=80, fg_color=HEADER_BG, corner_radius=0)
    header_frame.pack(fill="x", side="top")
    try:
        def load_image_from_url(url, size=None):
            response = requests.get(url)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            pil_img = Image.open(img_data)
            return pil_img  # return PIL image

        logo_url = "https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/5ef8907a670294733dfb769d07195e84db937dd9/build/Image_Resources/P2SERVE_LOGO.png"
        pil_img = load_image_from_url(logo_url)

        # Use CTkImage with desired display size (e.g., 60x60 px)
        logo_img = ctk.CTkImage(light_image=pil_img, size=(60, 60))

        logo_lbl = ctk.CTkLabel(header_frame, image=logo_img, text="", fg_color=HEADER_BG)
        logo_lbl.image = logo_img  # keep reference
        logo_lbl.place(relx=0.01, rely=0.5, anchor="w")
        TITLE_PLACEMENT_X = 0.01 + 0.08
    except Exception as e:
        logo_lbl = ctk.CTkLabel(header_frame, text="[LOGO]", font=("Arial", 16), text_color="white")
        logo_lbl.place(relx=0.01, rely=0.5, anchor="w")
        TITLE_PLACEMENT_X = 0.01 + 0.05
    title_label = ctk.CTkLabel(header_frame, text="BARANGAY POBLACION II", font=ctk.CTkFont(size=24, weight="bold"),
                               text_color="white")
    title_label.place(relx=TITLE_PLACEMENT_X, rely=0.5, anchor="w")

    def logout_action():
        root.destroy(); from Log_In_GUI import start_login1; start_login1()

    logout_btn = ctk.CTkButton(header_frame, text="LOG OUT", fg_color="#E74C3C", text_color="white",
                               hover_color="#C0392B", font=ctk.CTkFont(size=14, weight="bold"), width=100, height=30,
                               corner_radius=10, command=logout_action)
    logout_btn.pack(side="right", padx=15, pady=25)
    profile_btn = ctk.CTkButton(header_frame, text="PROFILE", font=ctk.CTkFont(size=14, weight="bold"),
                                fg_color="transparent", hover=False, command=lambda: navigate_to("Profile"))
    profile_btn.pack(side="right", padx=(0, 10), pady=25)
    nav_frame = ctk.CTkFrame(root, height=50, fg_color=NAV_INACTIVE_COLOR, corner_radius=0)
    nav_frame.pack(fill="x", side="top")

    def create_nav_button(text):
        btn = ctk.CTkButton(nav_frame, text=text, fg_color=NAV_INACTIVE_COLOR, text_color=TEXT_COLOR,
                            hover_color="#F39C12", font=ctk.CTkFont(size=16, weight="bold"), height=50, corner_radius=0,
                            command=lambda: navigate_to(text))
        btn.pack(side="left", fill="both", expand=True)
        return btn

    home_btn = create_nav_button("Home");
    about_btn = create_nav_button("About Us");
    contact_btn = create_nav_button("Contact Us");
    services_btn = create_nav_button("Services")
    content_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
    content_frame.pack(fill="both", expand=True)
    navigate_to("Home")
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.mainloop()


# --- To run the application ---
if __name__ == "__main__":
    start_mainhomepage()