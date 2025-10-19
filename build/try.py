# Main_page_GUI.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
from database_connector import get_connection
from PIL import Image, ImageTk
import requests
from io import BytesIO
from auth import get_user_id_by_username, insert_document_request  # Added imports

current_username = None


# --- DATABASE FUNCTIONS ---
def get_current_user_data(username):
    print(f"Fetching data for username: {username}")  # Debug print
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT firstname, lastname, profile_picture_path
            FROM resident
            WHERE username = %s
        """, (username,))
        row = cur.fetchone()
        print(f"Query result: {row}")  # Debug print
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


def save_user_profile_data(firstname, lastname, picture_path):
    """Saves the profile picture path to the database for the current user."""
    global current_username
    if not current_username:
        return False
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE resident
            SET profile_picture_path = %s
            WHERE username = %s
        """, (picture_path, current_username))
        conn.commit()
        print(f"Profile picture path saved for {current_username}: {picture_path}")  # Debug print
        return True
    except Exception as error:
        print(f"Error saving profile data: {error}")
        return False
    finally:
        cur.close()
        conn.close()


# =============================================================================
# --- PAGE CREATION FUNCTIONS ---

def create_home_page(parent_frame):
    """Creates the content for the Home page."""
    content_label = ctk.CTkLabel(parent_frame, text="Welcome to the Home Page Content Area.", font=ctk.CTkFont(size=20),
                                 text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")


def create_about_us_page(parent_frame):
    """Creates the content for the About Us page."""
    content_label = ctk.CTkLabel(parent_frame, text="This is the About Us page.", font=ctk.CTkFont(size=20),
                                 text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")


def create_contact_us_page(parent_frame):
    """Creates the content for the Contact Us page."""
    content_label = ctk.CTkLabel(parent_frame, text="Contact information goes here.", font=ctk.CTkFont(size=20),
                                 text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")


def create_services_page(parent_frame):
    """Creates the services page with document request functionality."""
    selected_info = {"widget": None, "document_name": None}
    uploaded_files = {}
    BTN_UNSELECTED_COLOR = "#3498db"
    BTN_SELECTED_COLOR = "#28A745"
    BTN_HOVER_COLOR = "#5dade2"

    # --- MODIFIED: Updated requirements data ---
    requirements_data = {
        "Barangay Clearance": {
            "title": "Barangay Clearance Requirements",
            "content": [
                ("Valid ID", "Must be addressed to Poblacion II. Please upload a clear picture."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),
            ]
        },
        "Barangay Building Clearance": {
            "title": "Barangay Building Clearance Requirements",
            "content": [
                ("Valid ID", "Must be addressed to Poblacion II. Please upload a clear picture."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),
            ]
        },
        "Barangay Business Clearance": {
            "title": "Barangay Business Clearance Requirements",
            "content": [
                ("Valid ID", "Please upload a clear picture of your ID."),
                ("DTI Registration", "Upload a clear picture or copy of your DTI certificate."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),  # Added
            ]
        },
        "Certificate of First Time Jobseeker": {
            "title": "Certificate of First Time Jobseeker Requirements",
            "content": [
                ("Valid ID", "Must be addressed to Poblacion II. Please upload a clear picture."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),
            ]
        },
        "Certificate of Indigency": {
            "title": "Certificate of Indigency Requirements",
            "content": [
                ("Valid ID", "Must be addressed to Poblacion II. Please upload a clear picture."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),
            ]
        },
        "Certificate of Residency": {
            "title": "Certificate of Residency Requirements",
            "content": [
                ("Valid ID", "Must be addressed to Poblacion II. Please upload a clear picture."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),
            ]
        },
        "Oath of Undertaking - First Time Jobseeker": {
            "title": "Oath of Undertaking Requirements",
            "content": [
                ("Valid ID", "Must be addressed to Poblacion II. Please upload a clear picture."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),
            ]
        },
        "Order of Payment for Barangay Business Clearance": {
            "title": "Order of Payment Requirements",
            "content": [
                ("Valid ID", "Please upload a clear picture of your ID."),
                ("DTI Registration", "Upload a clear picture or copy of your DTI certificate."),
                ("Proof of Payment", "Upload a screenshot of your payment confirmation."),  # Added
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

    def show_info_popup(title, message):
        popup = ctk.CTkToplevel(parent_frame)
        popup.title(title)
        popup.geometry("450x250")
        popup.transient(parent_frame.winfo_toplevel())
        popup.grab_set()
        ctk.CTkLabel(popup, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(popup, text=message, font=ctk.CTkFont(size=14), wraplength=400, justify="left").pack(pady=10,
                                                                                                          padx=20,
                                                                                                          fill="x")
        ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy).pack(pady=20)

    def submit_all_documents():
        doc_name = selected_info.get("document_name")
        if not doc_name: return
        expected_reqs = [req[0] for req in requirements_data[doc_name]["content"]]
        missing_reqs = [req for req in expected_reqs if req not in uploaded_files]
        if missing_reqs:
            show_info_popup("Incomplete Requirements", f"Please upload all required files. Missing:\n\n" + "\n".join(
                f"• {req}" for req in missing_reqs))
        else:
            # Get user ID from username
            global current_username
            user_id = get_user_id_by_username(current_username)
            if not user_id:
                show_info_popup("Error", "Unable to identify user. Please log in again.")
                return

            # Get file paths (if available)
            valid_id_path = uploaded_files.get("Valid ID")
            prof_of_payment_path = uploaded_files.get("Proof of Payment")

            # Insert the request into the database
            if insert_document_request(user_id, doc_name, valid_id_path, prof_of_payment_path):
                show_info_popup("Submission Successful",
                                f"Your request for '{doc_name}' has been submitted and is pending approval.")
            else:
                show_info_popup("Error", "Failed to submit request. Please try again.")

    # --- MODIFIED: handle_upload now shows a preview ---
    def handle_upload(status_label, preview_label, requirement_name):
        filetypes = (("Image Files", "*.png *.jpg *.jpeg"), ("PDF Files", "*.pdf"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title=f"Upload for {requirement_name}", filetypes=filetypes)

        if not filepath:
            return

        filename = os.path.basename(filepath)
        uploaded_files[requirement_name] = filepath

        # Check if the file is an image to show a preview
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(filepath)
                preview_img = ctk.CTkImage(light_image=img, size=(100, 100))
                preview_label.configure(image=preview_img, text="")
                preview_label.image = preview_img  # Keep reference
                status_label.configure(text=f"Uploaded: {filename}", text_color="green")
            except Exception as e:
                # Handle cases where the file is corrupted or not a valid image
                preview_label.configure(image=None, text="Invalid Image")
                status_label.configure(text=f"Error: {filename}", text_color="red")
        else:
            # For non-image files like PDF, just show text
            preview_label.configure(image=None, text="No Preview\n(PDF/File)")
            status_label.configure(text=f"Uploaded: {filename}", text_color="green")

    def display_requirements(document_name):
        uploaded_files.clear()
        for widget in requirements_frame.winfo_children(): widget.destroy()
        req_info = requirements_data.get(document_name)
        if not req_info: return

        ctk.CTkFrame(requirements_frame, height=2, fg_color="#E0E0E0").pack(fill="x", pady=(10, 20))
        ctk.CTkLabel(requirements_frame, text=req_info["title"], font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#333").pack(anchor="w", pady=(0, 15))

        for subtitle, text in req_info["content"]:
            ctk.CTkLabel(requirements_frame, text=subtitle, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
                fill="x", pady=(10, 2))
            ctk.CTkLabel(requirements_frame, text=text, wraplength=750, justify="left", anchor="w",
                         text_color="#555").pack(fill="x", padx=(15, 0), pady=(0, 5))

            # --- MODIFIED: Added image preview label ---
            preview_label = ctk.CTkLabel(requirements_frame, text="No Preview", fg_color="#EAEAEA", width=100,
                                         height=100, corner_radius=8, text_color="gray")
            preview_label.pack(pady=(5, 5), padx=(15, 0), anchor="w")

            upload_frame = ctk.CTkFrame(requirements_frame, fg_color="transparent")
            upload_frame.pack(fill="x", padx=(15, 0), pady=(5, 15))
            file_status_label = ctk.CTkLabel(upload_frame, text="No file selected.", font=ctk.CTkFont(size=12),
                                             text_color="gray")
            upload_button = ctk.CTkButton(upload_frame, text="Upload File", width=120)

            # Pass the new preview_label to the handler
            upload_button.configure(
                command=lambda s_lbl=file_status_label, p_lbl=preview_label, req_name=subtitle: handle_upload(s_lbl,
                                                                                                              p_lbl,
                                                                                                              req_name))

            upload_button.pack(side="left", anchor="w")
            file_status_label.pack(side="left", anchor="w", padx=10)

        ctk.CTkButton(requirements_frame, text="Submit All Documents", font=ctk.CTkFont(size=16, weight="bold"),
                      height=50, command=submit_all_documents).pack(fill="x", pady=(30, 10))
        scrollable_frame.update_idletasks()
        scrollable_frame._parent_canvas.yview_moveto(1.0)

    def select_document(document_name, clicked_button):
        if selected_info["widget"] is not None: selected_info["widget"].configure(fg_color=BTN_UNSELECTED_COLOR)
        clicked_button.configure(fg_color=BTN_SELECTED_COLOR)
        selected_info["widget"] = clicked_button
        selected_info["document_name"] = document_name
        display_requirements(document_name)

    documents = list(requirements_data.keys())
    for doc_name in documents:
        doc_button = ctk.CTkButton(button_container_frame, text=doc_name, fg_color=BTN_UNSELECTED_COLOR,
                                   hover_color=BTN_HOVER_COLOR, font=ctk.CTkFont(size=14), corner_radius=16, height=40,
                                   anchor="w")
        doc_button.configure(command=lambda name=doc_name, btn=doc_button: select_document(name, btn))
        doc_button.pack(fill="x", pady=4)


def create_profile_page(parent_frame):
    """Creates the profile page with data from the database."""
    global current_username
    if not current_username:
        ctk.CTkLabel(parent_frame, text="Please log in first.", text_color="red").pack(pady=20)
        return

    user = get_current_user_data(current_username)
    if not user:
        ctk.CTkLabel(parent_frame, text="Error loading profile data.", text_color="red").pack(pady=20)
        return

    new_picture_path = {"path": user.get("profile_picture_path")}
    profile_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    profile_frame.pack(fill="both", expand=True, padx=50, pady=30)
    title_label = ctk.CTkLabel(profile_frame, text="User Profile", font=ctk.CTkFont(size=24, weight="bold"))
    pfp_frame = ctk.CTkFrame(profile_frame, fg_color="#f0f0f0", width=200, height=200, corner_radius=10)
    pfp_label = ctk.CTkLabel(pfp_frame, text="", font=ctk.CTkFont(size=14), text_color="gray")
    upload_btn = ctk.CTkButton(profile_frame, text="Upload Picture")
    details_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
    save_btn = ctk.CTkButton(profile_frame, text="Save Profile")
    status_label = ctk.CTkLabel(profile_frame, text="")
    title_label.pack(anchor="w", pady=(0, 20))
    pfp_frame.pack(anchor="w", pady=(0, 20))
    pfp_frame.pack_propagate(False)
    pfp_label.pack(expand=True)
    upload_btn.pack(anchor="w", pady=(0, 30))
    details_frame.pack(fill="x", anchor="w")
    save_btn.pack(anchor="w", pady=(20, 10))
    status_label.pack(anchor="w")

    def display_image(image_path):
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                ctk_img = ctk.CTkImage(light_image=img, size=(200, 200))
                pfp_label.configure(image=ctk_img, text="")
                pfp_label.image = ctk_img
            except Exception as e:
                pfp_label.configure(image=None, text=f"Error:\n{e}")
        else:
            pfp_label.configure(image=None, text="No Image")

    def upload_picture():
        filepath = filedialog.askopenfilename(title="Select a Profile Picture",
                                              filetypes=(("Image Files", "*.png *.jpg *.jpeg"),))
        if filepath: new_picture_path["path"] = filepath; display_image(filepath)

    def save_profile():
        fname, lname = user.get("firstname", "N/A"), user.get("lastname", "N/A")
        if save_user_profile_data(fname, lname, new_picture_path["path"]):
            status_label.configure(text="Profile saved successfully!", text_color="green")
            status_label.after(3000, lambda: status_label.configure(text=""))
        else:
            status_label.configure(text="Error: Could not save profile.", text_color="red")
            status_label.after(3000, lambda: status_label.configure(text=""))

    upload_btn.configure(command=upload_picture)
    save_btn.configure(command=save_profile)
    display_image(new_picture_path["path"])
    ctk.CTkLabel(details_frame, text="First Name:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0,
                                                                                                   sticky="w",
                                                                                                   padx=(0, 10))
    ctk.CTkLabel(details_frame, text=user.get("firstname", "N/A"), font=ctk.CTkFont(size=14)).grid(row=0, column=1,
                                                                                                   sticky="w")
    ctk.CTkLabel(details_frame, text="Last Name:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=1, column=0,
                                                                                                  sticky="w",
                                                                                                  padx=(0, 10), pady=10)
    ctk.CTkLabel(details_frame, text=user.get("lastname", "N/A"), font=ctk.CTkFont(size=14)).grid(row=1, column=1,
                                                                                                  sticky="w")