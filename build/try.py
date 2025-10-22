def show_resident_accounts_content(parent_frame):
    """Creates and displays the UI for managing resident accounts, including verification requests."""

    def refresh_content():
        # Clear and reload the content
        for widget in parent_frame.winfo_children():
            widget.destroy()
        show_resident_accounts_content(parent_frame)

    # Fetch residents with pending verification (not initial approval)
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

    # Fetch approved residents (for display)
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

        ctk.CTkLabel(header_frame_pending, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w",
                                                                                            padx=5)
        ctk.CTkLabel(header_frame_pending, text="NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1,
                                                                                              sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="EMAIL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2,
                                                                                               sticky="w", padx=5)
        ctk.CTkLabel(header_frame_pending, text="ACTION", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3,
                                                                                                sticky="e", padx=5)

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

            def view_action(res_id):
                # Fetch and display verification info in a popup
                user_data = get_full_user_data_by_id(res_id)  # Need a helper function
                if user_data:
                    info = f"Name: {user_data['firstname']} {user_data['lastname']}\nDOB: {user_data['dob'] or 'N/A'}\nPlace of Birth: {user_data['place_of_birth'] or 'N/A'}\nAge: {user_data['age'] or 'N/A'}\nCivil Status: {user_data['civil_status'] or 'N/A'}\nGender: {user_data['gender'] or 'N/A'}"
                    popup = ctk.CTkToplevel(parent_frame)
                    popup.title("Verification Info")
                    popup.geometry("400x300")
                    ctk.CTkLabel(popup, text=info, font=ctk.CTkFont(size=12)).pack(pady=20, padx=20)
                    ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=10)
                else:
                    print("No verification data found")

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

            ctk.CTkButton(action_buttons_frame, text="View", width=60, height=25, fg_color=VIEW_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=resident['id']: view_action(id)).pack(
                side="left", padx=2)
            ctk.CTkButton(action_buttons_frame, text="Approve", width=60, height=25, fg_color=APPROVE_COLOR,
                          font=ctk.CTkFont(size=10), command=lambda id=resident['id'], email=resident['email']: approve_action(id, email)).pack(
                side="left", padx=2)
            ctk.CTkButton(action_buttons_frame, text="Reject", width=60, height=25, fg_color=REJECT_COLOR,
                          font=ctk.CTkFont(size=10),
                          command=lambda id=resident['id'], email=resident['email']: reject_action(id, email)).pack(
                side="left", padx=2)

    approved_title_text = f"Verified Residents ({len(approved_residents)})"
    approved_title = ctk.CTkLabel(scrollable_frame, text=approved_title_text, font=ctk.CTkFont(size=18, weight="bold"),
                                  anchor="w")
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

        ctk.CTkLabel(header_frame_approved, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0,
                                                                                             sticky="w", padx=5)
        ctk.CTkLabel(header_frame_approved, text="NAME", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1,
                                                                                               sticky="w", padx=5)
        ctk.CTkLabel(header_frame_approved, text="EMAIL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2,
                                                                                                sticky="w", padx=5)

        for resident in approved_residents:
            row_frame = ctk.CTkFrame(approved_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            row_frame.grid_columnconfigure((1, 2), weight=1)

            ctk.CTkLabel(row_frame, text=f"#{resident['id']}").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['name']).grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(row_frame, text=resident['email']).grid(row=0, column=2, sticky="w", padx=5)

# Helper function to get user data by ID (add this inside the function or globally)
def get_full_user_data_by_id(resident_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT firstname, lastname, dob, place_of_birth, age, civil_status, gender
            FROM resident WHERE id = %s
        """, (resident_id,))
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