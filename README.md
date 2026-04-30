# 🔐 Secure Authentication System with 2FA (Flask + MongoDB)

This project implements a secure authentication system using **Flask**, **MongoDB Atlas**, and **TOTP-based Two-Factor Authentication (2FA)**.

It demonstrates how modern secure login systems work using password hashing, QR code authentication, OTP verification, and JWT tokens.

---

# 🚀 Features

* User Registration System
* Secure Password Hashing (bcrypt)
* Two-Factor Authentication (TOTP)
* QR Code Generation
* Google Authenticator Integration
* OTP Verification
* JWT Token Authentication
* Protected Profile Route
* MongoDB Atlas Database Integration

---

# 🛠 Technologies Used

* Python
* Flask
* MongoDB Atlas
* PyMongo
* PyJWT
* pyotp
* bcrypt
* qrcode
* python-dotenv

---

# 📂 Project Structure

secure_auth_system/

app.py
config.py

database/
└── db.py

routes/
└── auth_routes.py

utils/
└── generate_qr.py

.env
requirements.txt
README.md

---

# ⚙️ Installation Steps

Clone the repository:

git clone https://github.com/YOUR_USERNAME/secure-auth-system-2fa.git

Navigate into the project folder:

cd secure-auth-system-2fa

Install dependencies:

pip install -r requirements.txt

---

# 🔑 Environment Variables Setup

Create a file named:

.env

Inside it write:

MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key

---

# ▶️ Run the Application

Start the server:

python app.py

Then open in your browser:

http://127.0.0.1:5000/test-register

---

# 🧪 API Endpoints

Register User

POST /api/auth/register

Creates a new user account and generates QR code for 2FA setup.

---

Login User

POST /api/auth/login

Requires:

email
password
OTP code from authenticator app

Returns JWT token after successful authentication.

---

Protected Profile Route

GET /api/auth/profile?token=YOUR_TOKEN

Returns user profile data if token is valid.

---

# 🔐 How Two-Factor Authentication Works

Step 1: User registers account
Step 2: Server generates secret key
Step 3: QR code is generated
Step 4: User scans QR code using authenticator app
Step 5: App generates OTP every 30 seconds
Step 6: User enters OTP during login
Step 7: Server verifies OTP
Step 8: JWT token is issued

---

# 📊 Example Authentication Flow

Register → Scan QR Code → Enter OTP → Login → Access Protected Profile

---

# 🌟 Future Improvements

Add token expiration handling
Add role-based authorization (Admin / User)
Add email verification
Add password reset functionality
Add frontend interface

---

# 👨‍💻 Author

Ahmed Mehran

Secure Authentication System using Flask + MongoDB + TOTP 2FA
