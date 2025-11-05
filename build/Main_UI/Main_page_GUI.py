# Main_page_GUI.py
import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
import os
from database_connector import get_connection
from PIL import Image, ImageTk, ImageDraw
import requests
import io
from io import BytesIO
from auth import get_user_id_by_username, insert_document_request, get_full_user_data, submit_verification_request

current_username = None

# --- validation sa age sa profile page
def validate_age_input(P):
    """
    Checks if the proposed new string 'P' is either empty or a valid non-negative integer.
    """
    if P == "":
        return True # Allows the user to delete everything
        
    
    try:
        age_int = int(P)
            
        # Reject negative numbers
        if age_int < 0:
            return False
                
        # Reject single digits if they are less than 1 
        if len(P) == 1 and age_int < 1: 
            return False 
            
        # dapat 12 to 100 lang ung input
        if len(P) >= 2:
            if age_int < 12 or age_int > 100:
                # Reject if the number is fully typed and outside the 12-100 range.
                return False 
            
        # Limit to 3 digits (e.g., 100)
        if len(P) > 3:
            return False
                
        return True 
    except ValueError:
        return False # Reject the input


# --- DATABASE FUNCTIONS --- DAPAT SA AUTH TO KASO NAHIHILO NA AKO E
# ----- KUNIN DITO YUNG DATA GALING SA PROFILE ----- PAG WALA NON PA TO
def get_current_user_data(username):
    print(f"Fetching data for username: {username}")  # para sa debugging
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" SELECT firstname, lastname, profile_picture_path FROM resident WHERE username = %s """, (username,))
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

#------ ITO LALAGAY NG PICTURE SA PROFILE
def save_user_profile_data(picture_path):
    global current_username
    if not current_username:
        return False
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" UPDATE resident SET profile_picture_path = %s WHERE username = %s""", (picture_path, current_username))
        conn.commit()
        print(f"Profile picture path saved for {current_username}: {picture_path}")  # para sa debugging
        return True
    except Exception as error:
        print(f"Error saving profile data: {error}")
        return False
    finally:
        cur.close()
        conn.close()

#----- AALAMIN KUNG APPROVE NA ACCOUNT NILA KASI PAG HINDI DI MAOOPEN MGA FOLDER SA SERVICE
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
    """Creates the content for the Home page using a scrollable Canvas."""
    print("--- Entering create_home_page (Reverted Scaling, Content Below) ---") # Changed log

    parent_frame.configure(fg_color="transparent") # Keep parent transparent
    image_path = r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/refs/heads/main/build/Image_Resources/barangay_background.jpg"
    original_pil_image = None
    canvas = None
    bg_photo_image_ref = None # Stored on canvas later


    # placeholders ng picture ng mga officials
    officials_placeholders = {}
    # --- Officials Data ---
    officials = [
        {"type": "captain", "name": "BOSS Irineo M4p4GmAhALZ", "title": "BARANGAY CAPTAIN", "committee": "Health and Sanitation", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/refs/heads/main/build/Image_Resources/captain1.jpg"},
        {"type": "kagawad", "name": "Aaron Peña", "title": "Position", "committee": "Social Services, Management and Information Systems", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},
        {"type": "kagawad", "name": "Benedicto Gamba", "title": "Position", "committee": "Beautification and Cleanliness Committee, Barangay Disaster Risk Reduction Management", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},
        {"type": "kagawad", "name": "Cristal San Juan", "title": "Position", "committee": "Peace and Order Committee", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},
        {"type": "kagawad", "name": "Gizelle Reyes Tuazon", "title": "Position", "committee": "Peace and Order Committee", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},
        {"type": "kagawad", "name": "Larry Pasco", "title": "Position", "committee": "Peace and Order Committee", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},
        {"type": "kagawad", "name": "Michael Sumala", "title": "Position", "committee": "Peace and Order Committee", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},
        {"type": "kagawad", "name": "Topher Garcia", "title": "Position", "committee": "Peace and Order Committee", "image_path": r"https://raw.githubusercontent.com/EfrenLamosteJr/edoop_casestudy/88332146a003b7ee56069c5760400904cfdc21f1/build/Image_Resources/maykol2.png"},

    ]

    def update_canvas_content(event=None):
        nonlocal original_pil_image, canvas, bg_photo_image_ref, officials_placeholders
        
        # --- NEW: Dictionary to hold image references ---
        canvas.official_images = {} 
        
        try:
            if not canvas or not canvas.winfo_exists():
                if "<Configure>" in parent_frame.bind():
                    parent_frame.unbind("<Configure>")
                return
        except tk.TclError: return

        # --- Load Original Image ONCE ---
        if not original_pil_image:
            try: 
                response = requests.get(image_path)
                response.raise_for_status() # Checks for download errors
                image_data = io.BytesIO(response.content)
                original_pil_image = Image.open(image_data)
                
            except Exception as e:
                print(f"ERROR loading background image from URL: {e}")
                return

        # --- Get Frame/Canvas Dimensions ---
        try:
            frame_width = parent_frame.winfo_width()
            frame_height = parent_frame.winfo_height()
            if frame_width <= 1 or frame_height <= 1:
                parent_frame.after(100, update_canvas_content)
                return
        except tk.TclError: return

        # --- Clear Canvas ---
        canvas.delete("all")

        # --- Reverted to your ORIGINAL scaling and cropping ---
        img_width, img_height = original_pil_image.size
        scale = max(frame_width / img_width, frame_height / img_height)
        scaled_img_width = int(img_width * scale); scaled_img_height = int(img_height * scale)
        resized_image = original_pil_image.resize((scaled_img_width, scaled_img_height), Image.Resampling.LANCZOS)
        x_offset = (scaled_img_width - frame_width) // 2; y_offset = (scaled_img_height - frame_height) // 2
        cropped_image = resized_image.crop((x_offset, y_offset, x_offset + frame_width, y_offset + frame_height))
        translucent_bg_image = cropped_image.copy().convert("RGBA")
        alpha = translucent_bg_image.split()[3]; alpha = alpha.point(lambda p: int(p * 0.7)); translucent_bg_image.putalpha(alpha)
        canvas.bg_photo_image_ref = ImageTk.PhotoImage(translucent_bg_image)

        # 1. Draw Background Image
        canvas.create_image(0, 0, anchor='nw', image=canvas.bg_photo_image_ref, tags="background_image")

        # --- Welcome Text ---
        welcome_line1 = "Welcome to Barangay Poblacion II!"
        welcome_line2 = "Your digital gateway for barangay services."
        font_name = "Segoe UI"; color_white = "white"; color_outline = "black"; outline_offset = 2
        font_size_line1 = 30; font_size_line2 = 18; font_weight = "bold"
        font_obj1 = tkFont.Font(family=font_name, size=font_size_line1, weight=font_weight)
        font_obj2 = tkFont.Font(family=font_name, size=font_size_line2, weight=font_weight)
        line1_height = font_obj1.metrics('linespace'); line2_height = font_obj2.metrics('linespace')
        wrap_width_ratio = 0.7; actual_wrap_width = int(frame_width * wrap_width_ratio)
        if actual_wrap_width < 1: actual_wrap_width = 1
        center_y_block = frame_height * 0.25 
        center_x = frame_width / 2
        total_text_height = line1_height + line2_height + 10
        y_pos_line1 = center_y_block - (total_text_height / 2) + (line1_height / 2)
        y_pos_line2 = y_pos_line1 + (line1_height / 2) + 10 + (line2_height / 2)
        o = outline_offset 
        offsets = [
            (-o, -o), (0, -o), (o, -o),
            (-o, 0),          (o, 0),
            (-o, o), (0, o), (o, o)
        ]
        # Line 1
        for dx, dy in offsets: canvas.create_text(center_x + dx, y_pos_line1 + dy, text=welcome_line1, fill=color_outline, font=font_obj1, tags="welcome_text", justify="center", width=actual_wrap_width)
        canvas.create_text(center_x, y_pos_line1, text=welcome_line1, fill=color_white, font=font_obj1, tags="welcome_text", justify="center", width=actual_wrap_width)
        # Line 2
        for dx, dy in offsets: canvas.create_text(center_x + dx, y_pos_line2 + dy, text=welcome_line2, fill=color_outline, font=font_obj2, tags="welcome_text", justify="center", width=actual_wrap_width)
        canvas.create_text(center_x, y_pos_line2, text=welcome_line2, fill=color_white, font=font_obj2, tags="welcome_text", justify="center", width=actual_wrap_width)

        # --- Elected Officials Section ---
        content_start_y = frame_height 
        section_padding = 50
        current_y = content_start_y + section_padding
        
        title_font = tkFont.Font(family=font_name, size=24, weight="bold")
        name_font = tkFont.Font(family=font_name, size=18, weight="bold")
        position_font = tkFont.Font(family=font_name, size=12, weight="normal")
        committee_font = tkFont.Font(family=font_name, size=12, weight="normal")
        placeholder_bg = "#E0E0E0"; text_color_dark = "#FFFFFF"

        canvas.create_text(center_x, current_y, text="Elected Officials", font=title_font, fill=text_color_dark, tags="officials")
        current_y += title_font.metrics('linespace') + 30

        captain = officials[0]
        placeholder_size_captain = 200
        placeholder_x_captain = center_x - (placeholder_size_captain / 2); placeholder_y_captain = current_y
        
        # --- pag load ng image ni boss ---
        try:
            response = requests.get(captain["image_path"]) 
            response.raise_for_status()
            image_data = io.BytesIO(response.content)
            pil_img = Image.open(image_data)

            pil_img = pil_img.resize((placeholder_size_captain, placeholder_size_captain), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(pil_img)
            
            # Store the reference and draw the image
            canvas.official_images['captain'] = tk_img 
            canvas.create_image(center_x, placeholder_y_captain, anchor="n", image=tk_img, tags="officials")
        
        except Exception as e:
            print(f"Error loading captain image: {e}")
            # Fallback: Draw the grey placeholder
            canvas.create_rectangle(placeholder_x_captain, placeholder_y_captain, placeholder_x_captain + placeholder_size_captain, placeholder_y_captain + placeholder_size_captain, fill=placeholder_bg, outline="", tags="officials")
            canvas.create_text(center_x, placeholder_y_captain + (placeholder_size_captain/2), text="Placeholder", fill="gray", font=("Arial", 10), anchor="center", tags="officials")
        
        # This text starts BELOW the placeholder/image
        current_y += placeholder_size_captain + 25 
        canvas.create_text(center_x, current_y, text=captain["title"], font=position_font, fill="orange", tags="officials", anchor="n")
        current_y += position_font.metrics('linespace')
        canvas.create_text(center_x, current_y, text=captain["name"], font=name_font, fill=text_color_dark, tags="officials", anchor="n")
        current_y += name_font.metrics('linespace') + 5
        committee_text_id_capt = canvas.create_text(center_x, current_y, text=captain["committee"], font=committee_font, fill=text_color_dark, tags="officials", anchor="n", width=frame_width*0.8)
        bbox_capt = canvas.bbox(committee_text_id_capt) 
        current_y += (bbox_capt[3] - bbox_capt[1] if bbox_capt else committee_font.metrics('linespace')) + section_padding

    
        kagawads = officials[1:]
        num_columns = 3
        
        # Avoid division by zero if frame_width is tiny
        if frame_width < 1: frame_width = 1 
        column_width = frame_width / num_columns
        
        placeholder_size_kagawad = 150; kagawad_start_y = current_y
        max_row_height = 0 

        # --- logic for centering the last row ---
        num_kagawads = len(kagawads)
        
        num_in_last_row = num_kagawads % num_columns
        if num_in_last_row == 0:
            num_in_last_row = num_columns # Last row is full, treat normally
            
        # Get the index of the last row (e.g., row 0, 1, 2...)
        last_row_index = (num_kagawads - 1) // num_columns
        
        # Calculate the padding needed to center the last row's items
        last_row_total_width = num_in_last_row * column_width
        left_padding = (frame_width - last_row_total_width) / 2

        for i, kagawad in enumerate(kagawads):
            col = i % num_columns
            row = i // num_columns

            if col == 0 and i > 0:
                kagawad_start_y += max_row_height + section_padding 
                max_row_height = 0 

            # Check if we are on the last row AND it's not a full row
            if row == last_row_index and num_in_last_row != num_columns:
                # We are in the non-full last row, use padding
                # Get the column *within* the last row (0, 1...)
                col_in_last_row = i - (last_row_index * num_columns) 
                base_x = left_padding + (col_in_last_row * column_width) + (column_width / 2)
            else:
                # This is a full row, calculate normally
                base_x = (col * column_width) + (column_width / 2)
           
            
            base_y = kagawad_start_y
            ph_y = base_y
            
            # --- pag load ng mga image nila kagawad---
            try:
                response = requests.get(kagawad["image_path"]) # 'image_path' is now a URL
                response.raise_for_status()
                image_data = io.BytesIO(response.content)
                pil_img = Image.open(image_data)

                pil_img = pil_img.resize((placeholder_size_kagawad, placeholder_size_kagawad), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)
                
                # Store the reference (using a unique key) and draw the image
                image_key = f'kagawad_{i}'
                canvas.official_images[image_key] = tk_img
                canvas.create_image(base_x, ph_y, anchor="n", image=tk_img, tags="officials")

            except Exception as e:
                if kagawad["image_path"]: # Only print error if a path was provided
                     print(f"Error loading image for {kagawad['name']}: {e}")
                # Fallback: Draw the grey placeholder
                ph_x = base_x - (placeholder_size_kagawad / 2)
                canvas.create_rectangle(ph_x, ph_y, ph_x + placeholder_size_kagawad, ph_y + placeholder_size_kagawad, fill=placeholder_bg, outline="", tags="officials")
                canvas.create_text(base_x, ph_y + (placeholder_size_kagawad/2), text="Placeholder", fill="gray", font=("Arial", 9), anchor="center", tags="officials")
            # --- END NEW ---
            
            text_y = ph_y + placeholder_size_kagawad + 20 # Text starts below the image/placeholder
            canvas.create_text(base_x, text_y, text=kagawad["title"], font=position_font, fill="orange", tags="officials", anchor="n")
            text_y += position_font.metrics('linespace')
            canvas.create_text(base_x, text_y, text=kagawad["name"], font=name_font, fill=text_color_dark, tags="officials", anchor="n")
            text_y += name_font.metrics('linespace') + 5
            committee_text_id = canvas.create_text( base_x, text_y, text=kagawad["committee"], font=committee_font, fill=text_color_dark, tags="officials", anchor="n", width=column_width * 0.8)
            text_bbox = canvas.bbox(committee_text_id)
            committee_height = (text_bbox[3] - text_bbox[1]) if text_bbox else committee_font.metrics('linespace') * (1 + kagawad["committee"].count('\n'))
            text_y += committee_height
            max_row_height = max(max_row_height, text_y - base_y)

        current_y = kagawad_start_y + max_row_height + section_padding

        # Background of Elected Officials #
        try:

            color_start_hex = "#87CEFA"  # Bright blue 
            color_end_hex   = "#012A4A"  # Dark navy blue

            # pag convert ng hex to rgb
            r_s, g_s, b_s = (int(color_start_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            r_e, g_e, b_e = (int(color_end_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

            # Get the dimensions for the gradient
            gradient_width = frame_width
            gradient_height = current_y - content_start_y # This is the height of the whole content section
            
            # Make sure width/height are at least 1
            if gradient_width < 1: gradient_width = 1
            if gradient_height < 1: gradient_height = 1

            # Create a new PIL Image in memory
            pil_gradient = Image.new("RGB", (gradient_width, gradient_height))
            draw = ImageDraw.Draw(pil_gradient)

            # Draw the gradient one line at a time
            for y in range(gradient_height):
                ratio = y / gradient_height
                
                # "Interpolate" the color for this line
                r = int(r_s * (1 - ratio) + r_e * ratio)
                g = int(g_s * (1 - ratio) + g_e * ratio)
                b = int(b_s * (1 - ratio) + b_e * ratio)
                
                # Draw the 1-pixel-high line
                draw.line([(0, y), (gradient_width, y)], fill=(r, g, b))

            # Convert the PIL image to a Tkinter PhotoImage
            canvas.gradient_bg_ref = ImageTk.PhotoImage(pil_gradient)

            # Draw the new gradient image onto the canvas
            canvas.create_image(0, content_start_y, anchor='nw', image=canvas.gradient_bg_ref, tags="content_bg")

        except Exception as e:
            print(f"ERROR creating gradient: {e}")
            canvas.create_rectangle(0, content_start_y, frame_width, current_y, 
                                     fill="#012A4A", # Fallback solid color
                                     outline="", 
                                     tags="content_bg")
        
        canvas.tag_lower("content_bg", "officials")

        # --- Update Scroll Region ---
        try:
            scroll_region = (0, 0, frame_width, current_y + 50) 
            canvas.configure(scrollregion=scroll_region)
        except tk.TclError as e:
            print(f"Error setting scrollregion: {e}")
            canvas.configure(scrollregion=(0, 0, frame_width, frame_height))

    # --- Create Canvas and Scrollbar ---
    canvas = tk.Canvas(parent_frame, highlightthickness=0, bd=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ctk.CTkScrollbar(parent_frame, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    def _on_mousewheel(event):
        # Platform-independent scroll direction
        delta = 0
        if event.num == 5 or event.delta < 0: delta = 1  # Scroll down
        elif event.num == 4 or event.delta > 0: delta = -1 # Scroll up
        if delta != 0: canvas.yview_scroll(delta, "units")

    # Bind across platforms
    root = parent_frame.winfo_toplevel() # Get the root window to bind globally if needed
    root.bind_all("<MouseWheel>", _on_mousewheel, add='+') # Windows/macOS
    root.bind_all("<Button-4>", _on_mousewheel, add='+')   # Linux scroll up
    root.bind_all("<Button-5>", _on_mousewheel, add='+')   # Linux scroll down


    # --- Initial call & Binding for resizing ---
    parent_frame.after_idle(update_canvas_content) # Use after_idle
    parent_frame.bind("<Configure>", update_canvas_content)

    print("--- Exiting create_home_page (Reverted Scaling, Content Below) ---")
    # --- END OF FUNCTION ---

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

    # --- requirements sa documents ---
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

    def show_info_popup(title, message):
        popup = ctk.CTkToplevel(parent_frame)
        popup.title(title)
        popup.geometry("450x250")
        popup.transient(parent_frame.winfo_toplevel())
        popup.grab_set()
        ctk.CTkLabel(popup, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(popup, text=message, font=ctk.CTkFont(size=14), wraplength=400, justify="left").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy).pack(pady=20)


    # --- PLACEHOLDER HELPER FUNCTIONS ---
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


    # --- submit_all_documents now checks for placeholder text ---
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


    # --- display_requirements now adds border and placeholder ---
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
                #
                textbox = ctk.CTkTextbox(
                    requirements_frame,
                    height=80,
                    corner_radius=8,
                    font=ctk.CTkFont(size=13),
                    border_width=1, 
                    border_color="#9A9A9A"  
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

    #---- DITO LALAGAY YUNG KUNG APPROVED NA YUNG ACCOUNT O HINDI PA MAG OOPEN MGA TEXTBOX PAG OK NA DI NA MABABAGO NA INPUT
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
        # --- Define the Validation Command ---
        # The register method makes the validation function available to Tkinter/CustomTkinter
        vcmd = details_frame.register(validate_age_input) 
        
        # --- Create the CTkEntry with Validation Options ---
        age_entry = ctk.CTkEntry(
            details_frame, 
            font=ctk.CTkFont(size=14), 
            corner_radius=5,
            validate="key", # 'key' means validate on every key press
            # The validation function is called with %P (new value)
            validatecommand=(vcmd, '%P') 
        )
        
        # Set the current value if it exists
        current_value = str(user.get("age")) if user.get("age") is not None else ""
        if current_value:
            age_entry.insert(0, current_value)

        age_entry.grid(row=current_row, column=1, sticky="ew", pady=5)
        fields["age"] = age_entry

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

    # --- Submit Button (KUNG NONE PA YUNG STATUS KASI YUNG SINET KO NA DEFAULT) ---
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
        age_str = fields["age"].get().strip() # Get the string value from the entry
        civil_status = fields["civil_status"].get()
        gender = fields["gender"].get()

        # Check 1: Ensure all fields are filled
        if not dob or not pob or civil_status == "-Select-" or gender == "-Select-" or not age_str:
            status_label.configure(text="Error: Please fill all additional information fields.", text_color="red")
            return
            
        # --- CHECK 2: AGE VALIDATION (Minimum 12, Maximum 100) ---
        try:
            age = int(age_str)
            
            # Reject if less than 12
            if age < 12:
                 status_label.configure(text="Error: Minimum age required is 12 years old.", text_color="red")
                 return
            
            # Reject if greater than 100
            if age > 100:
                 status_label.configure(text="Error: Age is unreasonably high.", text_color="red")
                 return
                 
        except ValueError:
            
            status_label.configure(text="Error: Age must be a valid whole number.", text_color="red")
            return
        # --- END AGE SUBMISSION VALIDATION ---

        # Proceed with submission, using the validated 'age' integer
        success = submit_verification_request(current_username, dob, pob, age, civil_status, gender)
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

def create_my_requests_page(parent_frame):
    """Creates the content for the My Requests page, showing user's document request history."""
    from auth import get_user_document_requests, get_user_id_by_username  # Import here to avoid circular imports

    global current_username
    if not current_username:
        ctk.CTkLabel(parent_frame, text="Please log in first.", text_color="red").pack(pady=20)
        return

    user_id = get_user_id_by_username(current_username)
    if not user_id:
        ctk.CTkLabel(parent_frame, text="Error: Unable to identify user.", text_color="red").pack(pady=20)
        return

    # Fetch user's requests
    user_requests = get_user_document_requests(user_id)

    # Clear any previous widgets
    for widget in parent_frame.winfo_children():
        widget.destroy()

    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    title_label = ctk.CTkLabel(scrollable_frame, text="My Document Requests", font=ctk.CTkFont(size=24, weight="bold"), anchor="w")
    title_label.pack(fill="x", pady=(0, 20))

    if not user_requests:
        # No requests message
        no_requests_frame = ctk.CTkFrame(scrollable_frame, fg_color="#F8F9FA", border_color="#DEE2E6", border_width=1, corner_radius=10)
        no_requests_frame.pack(fill="x", pady=(20, 0))
        ctk.CTkLabel(no_requests_frame, text="📄 You have no document requests yet.", font=ctk.CTkFont(size=16), text_color="#6C757D").pack(pady=20, padx=20)
    else:
        # Requests list
        container = ctk.CTkFrame(scrollable_frame, fg_color="white", corner_radius=5)
        container.pack(fill="x", pady=(0, 20))

        # Header
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(header_frame, text="DOCUMENT REQUESTED", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="DATE REQUESTED", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(header_frame, text="STATUS", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="e", padx=5)

        # Status color mapping
        status_colors = {
            "Pending": "#F1C40F",  # Yellow
            "Processing": "#3498DB",  # Blue
            "Finished": "#2ECC71",  # Green
            "Rejected": "#E74C3C"  # Red
        }

        # Rows
        for request in user_requests:
            row_frame = ctk.CTkFrame(container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(2, weight=0)

            ctk.CTkLabel(row_frame, text=request['document_name']).grid(row=0, column=0, sticky="w", padx=5)
            # Format date (assuming created_at is datetime)
            date_str = request['request_date'].strftime("%Y-%m-%d %H:%M") if request['request_date'] else "N/A"
            ctk.CTkLabel(row_frame, text=date_str).grid(row=0, column=1, sticky="w", padx=5)

            # Status label with color
            status = request['status']
            status_label = ctk.CTkLabel(row_frame, text=status, font=ctk.CTkFont(size=12, weight="bold"),
                                        fg_color=status_colors.get(status, "#95A5A6"), text_color="white",
                                        corner_radius=5, width=80, height=25)
            status_label.grid(row=0, column=2, sticky="e", padx=5)


    content_label = ctk.CTkLabel(parent_frame,
                                 text="",
                                 font=ctk.CTkFont(size=20),
                                 text_color="gray")
    content_label.place(relx=0.5, rely=0.5, anchor="center")
    
        
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
        print(f"\n--- Navigating to: {page_name} ---") # DEBUG

        # --- Unbind configure ONLY from content_frame ---
        bound_events = content_frame.bind() # Get bound events first
        # Check if bound_events is not None *before* using 'in'
        if bound_events and "<Configure>" in bound_events:
             print("Unbinding <Configure> from content_frame") # DEBUG
             content_frame.unbind("<Configure>")
        else:
             # This will now correctly handle the case where bind() returns None or an empty tuple
             print("No <Configure> binding found on content_frame to unbind.") # DEBUG
        # --- End Unbind ---

        # Now destroy widgets
        print("Destroying old widgets...") # DEBUG
        widgets_to_destroy = content_frame.winfo_children()
        for widget in widgets_to_destroy:
            widget.destroy()
        print(f"Destroyed {len(widgets_to_destroy)} old widgets.") # DEBUG

        # --- Recreate page content ---
        if page_name == "Home":
            print("Calling create_home_page...") # DEBUG
            create_home_page(content_frame)
        elif page_name == "Services":
            print("Calling create_services_page...") # DEBUG
            create_services_page(content_frame)
        elif page_name == "My Requests":
            print("Calling create_my_requests_page...") # DEBUG
            create_my_requests_page(content_frame)
        elif page_name == "Profile":
            print("Calling create_profile_page...") # DEBUG
            create_profile_page(content_frame)
        print("Page creation function called.") # DEBUG


        # --- Update Button States ---
        buttons = {"Home": home_btn, "Services": services_btn, "My Requests": my_requests_btn} # Exclude profile btn

        for name, btn in buttons.items():
            if name == page_name:
                btn.configure(fg_color=NAV_ACTIVE_COLOR, text_color="white", hover_color=NAV_ACTIVE_COLOR)
            else:
                btn.configure(fg_color=NAV_INACTIVE_COLOR, text_color=TEXT_COLOR, hover_color="#F39C12")

        # Handle profile button state separately
        if page_name == "Profile":
             profile_btn.configure(text_color="white")
             print("Set Profile button to active state.") # DEBUG
        else:
            profile_btn.configure(text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"])
            print("Set Profile button to inactive/default state.") # DEBUG
        print("Button states updated.") # DEBUG


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

    # --- Button creation ---
    home_btn = create_nav_button("Home")
    services_btn = create_nav_button("Services")
    my_requests_btn = create_nav_button("My Requests")  # <-- ADDED

    content_frame = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0) # Make frame transparent
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