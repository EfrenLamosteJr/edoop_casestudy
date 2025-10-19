import bcrypt
from database_connector import get_connection  # <-- your DB connection file

# -------------------- SIGN UP --------------------
def signup(firstname, lastname, username, co_number, email, barangay_address, password):
    conn = get_connection()
    cur = conn.cursor()

    # Hash the password for security
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("""
            INSERT INTO resident (firstname, lastname, username, co_number, email, barangay_address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (firstname, lastname, username, co_number, email, barangay_address, hashed.decode('utf-8')))

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

    # Check if user exists by username OR email
    cur.execute("""
        SELECT password FROM resident 
        WHERE username = %s
    """, (username,))

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
            cur.execute("UPDATE resident SET password = %s WHERE email = %s",(newhashed.decode('utf-8'), register_email))
            conn.commit()
            return True, "Password reset successfully."
        else:
            return False, "Email not found."

    except Exception as error:
        return False, f"Error: {error}"

    finally:
        cur.close()
        conn.close()

# -------------------- UPDATE USER PROFILE --------------------
def update_user_profile_by_username(username, firstname, lastname, profile_picture_path):
    """Update user profile data by username."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE resident
            SET firstname = %s, lastname = %s, profile_picture_path = %s
            WHERE username = %s
        """, (firstname, lastname, profile_picture_path, username))
        conn.commit()
        return True, "Profile updated successfully."
    except Exception as error:
        return False, f"Error: {error}"
    finally:
        cur.close()
        conn.close()