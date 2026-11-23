# P2SERVE — Desktop Barangay E-Service Management System

A desktop-based **Barangay E-Service Management System** developed for **Barangay Poblacion II, Marilao, Bulacan** as part of the **Event-Driven and Object-Oriented Programming (EDOOP) Case Study**.

Built using **Python (CustomTkinter)** and **MySQL**, the system digitizes resident registration, identity verification, document requests, and administrative processing through separate Resident and Admin/Staff portals.

---

### 🎯 Business Problem

Barangay Poblacion II relied on manual logbooks, in-person queues, and disconnected spreadsheets to process resident clearances and certificates.

These manual processes made it difficult to manage resident information, monitor document requests, track payment submissions, and handle large volumes of transactions efficiently.

P2SERVE was developed to centralize these processes through a desktop-based system, allowing residents to submit requests online while providing barangay personnel with tools to verify information and manage document processing.

---

### ✨ Key System Features

#### 1. Resident Portal

Provides residents with an interface for account registration, verification, and document requests.

- **Secure Registration & Email OTP Verification:** Implements 6-digit email verification through Gmail SMTP before account creation. Includes input validation for 11-digit mobile numbers, alphanumeric usernames, and password strength.
- **Account Verification:** Allows residents to submit personal information and upload profile photos for administrative review before accessing document request services.
- **Online Document Requests:** Supports eight barangay documents:
  - Barangay Clearance
  - Building Clearance
  - Business Clearance
  - First-Time Jobseeker Certificate
  - Certificate of Indigency
  - Certificate of Residency
  - Oath of Undertaking
  - Order of Payment
- **Digital Payment Submission:** Allows residents to upload valid identification, DTI documents when applicable, and GCash payment receipts through the portal.
- **Request Status Tracking:** Displays document request progress through four statuses: Pending, Processing, Finished, and Rejected.

#### 2. Admin & Staff Portal

Provides barangay personnel with tools for resident verification, document processing, and administrative monitoring.

- **Administrative KPI Dashboard:** Displays summary cards for pending resident verifications, pending document requests, and total verified residents.
- **Resident Verification:** Allows administrators to review submitted resident information and uploaded profile photos before approving or rejecting accounts.
- **Document Request Management:** Enables staff to inspect submitted requirements and GCash receipts, process requests, and provide reasons for rejected submissions.
- **Staff Account Management:** Supports multiple user roles, including Admin, Staff, and Treasurer.
- **Automated Email Notifications:** Sends HTML-formatted email notifications for registration OTPs, password resets, account approvals and rejections, and document-ready-for-pickup updates.

---

### 🗄️ Database & Backend Implementation

The system uses a **MySQL relational database (`barangay_eservice`)** to organize and manage resident information, staff accounts, authentication records, and document requests.

Key backend implementations include:

- **SQL CRUD Operations:** Handles creating, retrieving, updating, and deleting database records.
- **Data Validation:** Implements input validation to maintain the consistency and accuracy of submitted information.
- **Authentication & Security:** Uses `bcrypt` for salted password hashing and Gmail SMTP for email-based OTP verification.
- **Dashboard Queries:** Uses SQL count queries to retrieve administrative figures for the KPI dashboard.
- **Database Connectivity:** Connects the Python application to MySQL through `mysql-connector-python`.

---

### 🛠️ Technologies Used

| Category | Technologies |
| :--- | :--- |
| Programming Language | Python 3 |
| Desktop GUI Framework | CustomTkinter, Tkinter, ttk |
| Database Management | MySQL, XAMPP |
| Database Connectivity | mysql-connector-python |
| Security & Authentication | bcrypt, Gmail SMTP, smtplib |
| Image Processing | Pillow (PIL) |
| HTTP Requests & Data Handling | requests, io, BytesIO |
| Email Templates | HTML5, Inline CSS |

---

### 👨‍💻 Project Contribution

**Role: Back-End & Database Developer**

Responsible for developing the backend components and database integration of the application.

- Designed and connected the MySQL relational database (`barangay_eservice`) for resident profiles, staff accounts, and document request records.
- Implemented authentication workflows using `bcrypt` password hashing and 6-digit email OTP verification through SMTP.
- Developed data validation rules and SQL CRUD operations for managing application records.
- Implemented SQL queries that supply administrative KPI figures to the dashboard.
- Integrated database operations with the application's resident and administrative interfaces.
