from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "amoura_luxe_secret"

DATABASE = "amoura_luxe.db"

def init_db():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, category TEXT, age_group TEXT, image TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, address TEXT, status TEXT)")

@app.route("/")
def index():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template("index.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                con.commit()
                return redirect(url_for("login"))
            except:
                return "Username already exists"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            if user:
                session["user_id"] = user[0]
                session["username"] = user[1]
                return redirect(url_for("index"))
            else:
                return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session or session["username"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        category = request.form["category"]
        age_group = request.form["age_group"]
        image = request.form["image"]
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, price, category, age_group, image) VALUES (?, ?, ?, ?, ?)", 
                        (name, price, category, age_group, image))
            con.commit()
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template("admin.html", products=products)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
