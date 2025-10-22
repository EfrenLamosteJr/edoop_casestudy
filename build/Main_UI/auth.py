import bcrypt
from database_connector import get_connection
import smtplib
from email.message import EmailMessage

# -------------------- SIGN UP --------------------
def signup(firstname, lastname, username, co_number, email, barangay_address, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cur.execute(""" INSERT INTO resident (firstname, lastname, username, co_number, email, barangay_address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s) """,
            (firstname, lastname, username, co_number, email, barangay_address, hashed.decode('utf-8')))
        conn.commit()
        return True, "User registered successfully."
    except Exception as error:
        return False, f"Error: {error}"
    finally:
        cur.close()
        conn.close()

# -------------------- LOGIN --------------------
def login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    # Check if user exists by username
    cur.execute(""" SELECT password FROM resident WHERE username = %s """,
                (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
        return True, "Login successful."
    return False, "Invalid username/email or password."

# -------------------- FORGOT PASSWORD --------------------
def forgotpassword(register_email, new_password):
    conn = get_connection()
    cur = conn.cursor()
    newhashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("SELECT email FROM resident WHERE email = %s", (register_email,))
        c_email = cur.fetchone()
        if c_email:
            cur.execute("UPDATE resident SET password = %s WHERE email = %s",(newhashed.decode('utf-8'),
            register_email))
            conn.commit()
            return True, "Password reset successfully."
        else:
            return False, "Email not found."

    except Exception as error:
        return False, f"Error: {error}"
    finally:
        cur.close()
        conn.close()

# -------------------- INSERT DOCUMENT REQUEST --------------------
def insert_document_request(user_id, document_name, valid_id_path=None, prof_of_payment_path=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO document_requests (user_id, document_name, valid_id, prof_of_payment)
            VALUES (%s, %s, %s, %s)
        """, (user_id, document_name, valid_id_path, prof_of_payment_path))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error inserting document request: {error}")
        return False
    finally:
        cur.close()
        conn.close()

# -------------------- GET FULL USER DATA --------------------
def get_full_user_data(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT id, firstname, lastname, email, profile_picture_path, dob, place_of_birth, age, civil_status, gender, verification_status
            FROM resident WHERE username = %s""",
            (username,))
        row = cur.fetchone()
        if row:
            return {
                "id": row[0], "firstname": row[1], "lastname": row[2], "email": row[3], "profile_picture_path": row[4],
                "dob": row[5], "place_of_birth": row[6], "age": row[7], "civil_status": row[8], "gender": row[9], "verification_status": row[10]
            }
        return None
    except Exception as error:
        print(f"Error fetching full user data: {error}")
        return None
    finally:
        cur.close()
        conn.close()

# -------------------- CREATE STAFF ACCOUNT --------------------
def create_staff_account(full_name, username, password, position, role):
    conn = get_connection()
    cur = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cur.execute("""INSERT INTO staff (full_name, username, password, position, role)
            VALUES (%s, %s, %s, %s, %s)""",
            (full_name, username, hashed.decode('utf-8'), position or None, role))
        conn.commit()
        return True, "Staff account created successfully."
    except Exception as error:
        return False, f"Error: {error}"
    finally:
        cur.close()
        conn.close()

# -------------------- SEND REJECTION EMAIL --------------------
def send_rejection_email(to_email, reason):
    try:
        with open("rejection_email.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        html_content = html_content.replace("{{ reason }}", reason)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        from_email = "barangaypoblacion2eservice@gmail.com"
        server.login(from_email, 'veorjdapcuglikhu')

        msg = EmailMessage()
        msg['Subject'] = "Account Registration Rejected"
        msg['From'] = from_email
        msg['To'] = to_email
        msg.set_content(
            f"Your account registration has been rejected.\n\nReason: {reason}\n\nPlease contact support for more information.")
        msg.add_alternative(html_content, subtype='html')

        server.send_message(msg)
        server.quit()
        print(f"Rejection email sent to {to_email}")
        return True
    except Exception as error:
        print(f"Error sending email: {error}")
        return False

# -------------------- SEND APPROVAL EMAIL --------------------
def send_approval_email(to_email):
    try:
        with open("approval_email.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        from_email = "barangaypoblacion2eservice@gmail.com"
        server.login(from_email, 'veorjdapcuglikhu')

        msg = EmailMessage()
        msg['Subject'] = "Account Registration Approved"
        msg['From'] = from_email
        msg['To'] = to_email
        msg.set_content(
            "Congratulations! Your account registration has been approved. You can now log in to your account and access all resident services.")
        msg.add_alternative(html_content, subtype='html')

        server.send_message(msg)
        server.quit()
        print(f"Approval email sent to {to_email}")
        return True
    except Exception as error:
        print(f"Error sending approval email: {error}")
        return False

# -------------------- SUBMIT VERIFICATION REQUEST --------------------
def submit_verification_request(username, dob, place_of_birth, age, civil_status, gender):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" UPDATE resident SET dob = %s, place_of_birth = %s, age = %s, civil_status = %s, gender = %s, verification_status = 'pending'
            WHERE username = %s """,
            (dob, place_of_birth, age, civil_status, gender, username))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error submitting verification: {error}")
        return False
    finally:
        cur.close()
        conn.close()

# -------------------- REJECT VERIFICATION REQUEST --------------------
def reject_verification_request(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""UPDATE resident 
            SET dob = NULL, place_of_birth = NULL, age = NULL, civil_status = NULL, gender = NULL, verification_status = 'not_verified'
            WHERE id = %s""",
            (resident_id,))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error rejecting verification: {error}")
        return False
    finally:
        cur.close()
        conn.close()

# -------------------- APPROVE VERIFICATION REQUEST --------------------
def approve_verification_request(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE resident SET verification_status = 'approved' WHERE id = %s", (resident_id,))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error approving verification: {error}")
        return False
    finally:
        cur.close()
        conn.close()

# -------------------- GET USER ID BY USERNAME --------------------
def get_user_id_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM resident WHERE username = %s", (username,))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as error:
        print(f"Error fetching user ID: {error}")
        return None
    finally:
        cur.close()
        conn.close()

# -------------------- UPDATE USER PROFILE --------------------
def update_user_profile_by_username(username, firstname, lastname, profile_picture_path):
    """Update user profile data by username."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" UPDATE resident
            SET firstname = %s, lastname = %s, profile_picture_path = %s
            WHERE username = %s """,
            (firstname, lastname, profile_picture_path, username))
        conn.commit()
        return True, "Profile updated successfully."
    except Exception as error:
        return False, f"Error: {error}"
    finally:
        cur.close()
        conn.close()

# -------------------- GET USER STATUS BY USERNAME --------------------
def get_user_status_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT verification_status FROM resident WHERE username = %s", (username,))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as error:
        print(f"Error fetching user verification status: {error}")
        return None
    finally:
        cur.close()
        conn.close()

# -------------------- GET FULL USER DATA BY ID --------------------
def get_full_user_data_by_id(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(""" SELECT firstname, lastname, dob, place_of_birth, age, civil_status, gender
            FROM resident WHERE id = %s """,
            (resident_id,))
        row = cur.fetchone()
        if row:
            return {
                "firstname": row[0], "lastname": row[1], "dob": row[2], "place_of_birth": row[3],
                "age": row[4], "civil_status": row[5], "gender": row[6]
            }
        return None
    except Exception as error:
        print(f"Error fetching user data by ID: {error}")
        return None
    finally:
        cur.close()
        conn.close()
