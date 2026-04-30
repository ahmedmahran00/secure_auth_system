from flask import Flask
from dotenv import load_dotenv
from database import mongo
from routes.auth_routes import auth_routes
import os

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo.init_app(app)

# تسجيل auth routes
app.register_blueprint(auth_routes, url_prefix="/api/auth")


@app.route("/")
def home():
    return "Database Connected Successfully 🚀"


@app.route("/test-register")
def test_register():
    return """
    <form action="/api/auth/register" method="post">
        Name: <input name="name"><br>
        Email: <input name="email"><br>
        Password: <input name="password"><br>
        Role: <input name="role"><br>
        <button type="submit">Register</button>
    </form>
    """


@app.route("/test-login")
def test_login():
    return """
    <form action="/api/auth/login" method="post">
        Email: <input name="email"><br>
        Password: <input name="password"><br>
        OTP Code: <input name="otp"><br>
        <button type="submit">Login</button>
    </form>
    """


app.run(debug=True)