import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os  # Needed to get the base name of the file path
from PIL import Image  # Import Pillow for image processing
from database_connector import get_connection

# Global variable for the current username
current_username = None

# =============================================================================
# --- DATABASE FUNCTIONS ---
# =============================================================================

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
# =============================================================================

# ... (create_home_page, create_about_us_page, create_contact_us_page, create_services_page remain unchanged)

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

# =============================================================================
# --- MAIN APPLICATION ---
# =============================================================================

# ... (start_mainhomepage function remains unchanged)

# --- To run the application ---
if __name__ == "__main__":
    start_mainhomepage()
