from flask import Blueprint, request, jsonify
from ..db import session
import uuid
import bcrypt

auth_bp = Blueprint("auth", __name__)

def hash_password(password):
    # Hash a password for the first time
    # (Using bcrypt, the salt is included in the hash)
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    # Check hashed password. Using .encode() on the stored hash because bcrypt expects bytes.
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        if not data.get("email") or not data.get("password") or not data.get("username"):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        existing = session.execute("SELECT * FROM users WHERE email=%s ALLOW FILTERING", (data["email"],)).one()
        if existing:
            return jsonify({"error": "Email already registered"}), 409

        user_id = uuid.uuid4()
        password_hash = hash_password(data["password"])

        session.execute("""
            INSERT INTO users (id, username, email, password_hash)
            VALUES (%s, %s, %s, %s)
        """, (user_id, data["username"], data["email"], password_hash))

        return jsonify({"message": "User registered successfully 🔐"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        rows = session.execute("SELECT * FROM users WHERE email=%s ALLOW FILTERING", (data["email"],))
        user = rows.one()

        if not user or not check_password(data["password"], user['password_hash']):
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({
            "message": "Login successful 🔥",
            "user_id": str(user['id']),
            "email": user['email']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

