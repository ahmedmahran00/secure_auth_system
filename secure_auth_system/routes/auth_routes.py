from flask import Blueprint, request, jsonify
from database import mongo
import bcrypt
import pyotp
import qrcode
import io
import base64
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

auth_routes = Blueprint("auth_routes", __name__)


########################
# REGISTER PAGE RESULT
########################

@auth_routes.route("/register", methods=["POST"])
def register():

    data = request.form if request.form else request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "User")

    existing_user = mongo.db.users.find_one({"email": email})

    if existing_user:
        return """
        <h2>User already exists ❌</h2>
        <a href="/test-register">Try again</a>
        """

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    secret = pyotp.random_base32()

    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name="SecureAuthSystem"
    )

    qr = qrcode.make(totp_uri)

    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")

    qr_code = base64.b64encode(buffer.getvalue()).decode()

    mongo.db.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password.decode(),
        "role": role,
        "secret": secret
    })

    return f"""
    <h2>✅ User Registered Successfully</h2>

    <h3>Scan this QR Code:</h3>

    <img src="data:image/png;base64,{qr_code}" width="250"/>

    <br><br>

    <a href="/test-login">
        <button>➡️ Go to Login</button>
    </a>
    """


########################
# LOGIN PAGE RESULT
########################

@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.form if request.form else request.json

    email = data.get("email")
    password = data.get("password")
    otp = data.get("otp")

    user = mongo.db.users.find_one({"email": email})

    if not user:
        return "<h2>User not found ❌</h2>"

    if not bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):
        return "<h2>Wrong password ❌</h2>"

    totp = pyotp.TOTP(user["secret"])

    if not totp.verify(otp):
        return "<h2>Invalid OTP ❌</h2>"

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    },
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )

    return f"""
    <h2>✅ Login Successful</h2>

    <p>Your token:</p>

    <textarea rows="4" cols="80">{token}</textarea>

    <br><br>

    <a href="/api/auth/profile?token={token}">
        <button>➡️ Open Profile</button>
    </a>

    <br><br>

    <a href="/api/auth/admin?token={token}">
        <button> Open Admin Page</button>
    </a>
    """


########################
# PROFILE ROUTE
########################

@auth_routes.route("/profile", methods=["GET"])
def profile():

    token = request.args.get("token")

    if not token:
        return "<h2>Token missing ❌</h2>"

    try:
        data = jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )

        return f"""
        <h2>✅ Profile Access Granted</h2>

        <p>User ID: {data['user_id']}</p>
        <p>Role: {data['role']}</p>

        <br>

        <a href="/test-login">
            <button>🔁 Login Again</button>
        </a>
        """

    except:
        return "<h2>Invalid Token ❌</h2>"


########################
# ADMIN ROUTE
########################

@auth_routes.route("/admin", methods=["GET"])
def admin():

    token = request.args.get("token")

    if not token:
        return "<h2>Token missing ❌</h2>"

    try:
        data = jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )

        if data["role"] != "Admin":
            return "<h2>Admins only ❌</h2>"

        return """
        <h2>👑 Welcome Admin</h2>

        <a href="/test-register">
            <button>🔁 Register New User</button>
        </a>
        """

    except:
        return "<h2>Invalid Token ❌</h2>"