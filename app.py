from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from openai import OpenAI
from flask import render_template
app = Flask(__name__)
CORS(app)


DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)




@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"success": False, "message": "No data received ❌"})

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Missing fields ❌"})

    users = load_users()

    for u in users:
        if u["email"] == email:
            return jsonify({"success": False, "message": "Email already exists ⚠️"})

    users.append({
        "name": name,
        "email": email,
        "password": password
    })

    save_users(users)

    return jsonify({
        "success": True,
        "message": "Account created 🚀",
        "redirect": "/f1"
    })


@app.route("/login", methods=["POST"])
def login_api():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Missing fields ❌"
        })

    try:
        with open(DATA_FILE, "r") as f:
            users = json.load(f)
    except:
        users = []

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "success": True,
                "message": "Login successful 🚀",
                "user": user,
                "redirect": "/f1"
            })

    return jsonify({
        "success": False,
        "message": "Invalid email or password ❌"
    })

with open("recipes.json", encoding="utf-8") as f:
    recipes = json.load(f)


@app.route("/get_recipe", methods=["POST"])
def get_recipe():
    data = request.get_json()

    if not data or "dish" not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid request"
        })

    user_input = data["dish"].lower().strip()

    best_match = None
    max_match = 0

    for dish in recipes:
        words = dish.lower().split()
        match_count = sum(word in user_input for word in words)

        if match_count > max_match:
            max_match = match_count
            best_match = dish

    if best_match and max_match > 0:
        return jsonify({
            "status": "success",
            "dish": best_match,
            "recipe": recipes[best_match]
        })

    return jsonify({
        "status": "error",
        "message": "Recipe not found 😢"
    })

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/f1")
def f1():
    return render_template("f1.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/signup_page")
def signup_page():
    return render_template("sign.html")

@app.route("/mymeal")
def mymeal():
    return render_template("mymeal.html")

@app.route("/order")
def order():
    return render_template("order.html")
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)