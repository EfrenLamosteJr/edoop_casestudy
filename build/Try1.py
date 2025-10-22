def get_full_user_data(username):
    """Fetch full user data including verification fields."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, firstname, lastname, email, profile_picture_path, dob, place_of_birth, age, civil_status, gender, verification_status
            FROM resident WHERE username = %s
        """, (username,))
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

def submit_verification_request(username, dob, place_of_birth, age, civil_status, gender):
    """Submit verification request and update status to 'pending'."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE resident 
            SET dob = %s, place_of_birth = %s, age = %s, civil_status = %s, gender = %s, verification_status = 'pending'
            WHERE username = %s
        """, (dob, place_of_birth, age, civil_status, gender, username))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error submitting verification: {error}")
        return False
    finally:
        cur.close()
        conn.close()

def reject_verification_request(resident_id):
    """Reject verification: Clear data and set status to 'not_verified'."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE resident 
            SET dob = NULL, place_of_birth = NULL, age = NULL, civil_status = NULL, gender = NULL, verification_status = 'not_verified'
            WHERE id = %s
        """, (resident_id,))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error rejecting verification: {error}")
        return False
    finally:
        cur.close()
        conn.close()

def approve_verification_request(resident_id):
    """Approve verification: Set status to 'approved'."""
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