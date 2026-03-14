from flask import Flask, jsonify, render_template, request, session, redirect, url_for,flash
import random
import sqlite3
from datetime import datetime, timedelta
import io
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import razorpay

app = Flask(__name__)
app.secret_key = "secret123"

# Razorpay API Keys
RAZORPAY_KEY_ID = "rzp_test_SPoIpuOUhqlt8e"
RAZORPAY_KEY_SECRET = "1O5S9hbDeDQ77VBUbSFEHNHe"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Add Create Order API
@app.route("/create-order", methods=["POST"])
def create_order():

    data = request.json
    amount = int(data["amount"]) * 100   # Razorpay uses paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify(order)

# ================= VERIFY PAYMENT =================
@app.route("/verify-payment", methods=["POST"])
def verify_payment():

    data = request.json

    params_dict = {
        "razorpay_order_id": data["razorpay_order_id"],
        "razorpay_payment_id": data["razorpay_payment_id"],
        "razorpay_signature": data["razorpay_signature"]
    }

    try:
        client.utility.verify_payment_signature(params_dict)

        # Save successful payment
        conn = get_db()
        conn.execute(
            "INSERT INTO transactions (card_last4, bank_name, payment_method, amount, status, time) VALUES (?,?,?,?,?,?)",
            ("RZPY", "Razorpay", "Online", session.get("amount"), "Successful", datetime.now())
        )
        conn.commit()
        conn.close()

        return jsonify({"status": "success"})

    except:
        return jsonify({"status": "failed"})    

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("smartpay.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_last4 TEXT,
        bank_name TEXT,
        payment_method TEXT,
        amount REAL,
        status TEXT,
        time TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS chatbot_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_msg TEXT,
        bot_reply TEXT,
        time TEXT
    )
    """)

    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        rating INTEGER,
        comment TEXT,
        time TEXT
    )
    """)
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        mobile TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()





products = [
    # ========= AC SERIES =========
    {"id": 1, "name": "AC", "price": 92000, "image": "images/ac.jpg"},
    {"id": 2, "name": "Fridge", "price": 90000, "image": "images/fridge1.jpg"},
    {
        "id": 3,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine.jpg",
    },
    {"id": 4, "name": "TV", "price": 85000, "image": "images/tv1.jpg"},
    {"id": 5, "name": "Headphones", "price": 2500, "image": "images/headphone.jpg"},
    {"id": 6, "name": "Phone", "price": 125000, "image": "images/phone1.jpg"},
    {"id": 7, "name": "AC", "price": 60000, "image": "images/ac1.jpg"},
    {"id": 8, "name": "Oven", "price": 8000, "image": "images/oven.jpg"},
    {"id": 9, "name": "TV", "price": 30000, "image": "images/tv1.jpg"},
    {"id": 10, "name": "Fridge", "price": 80000, "image": "images/fridge2.jpg"},
    {"id": 11, "name": "Printer", "price": 6000, "image": "images/printer.jpg"},
    {"id": 12, "name": "Laptop", "price": 55000, "image": "images/laptop.jpg"},
    {"id": 13, "name": "Speaker", "price": 4500, "image": "images/speaker.jpg"},
    {"id": 14, "name": "Computer", "price": 50000, "image": "images/computer.jpg"},
    {"id": 15, "name": "Electric Kettle", "price": 1200, "image": "images/kettle.jpg"},
    {"id": 16, "name": "USB Drive", "price": 600, "image": "images/usb.jpg"},
    {"id": 17, "name": "Hard Drive", "price": 4000, "image": "images/hard drive.jpg"},
    {"id": 18, "name": "Keyboard", "price": 800, "image": "images/keyboard.jpg"},
    {"id": 19, "name": "Camera", "price": 25000, "image": "images/camera.jpg"},
    {"id": 20, "name": "Router", "price": 3000, "image": "images/router.jpg"},
    {"id": 21, "name": "Projector", "price": 40000, "image": "images/projector.jpg"},
    {
        "id": 22,
        "name": "Game Console",
        "price": 30000,
        "image": "images/gameconsole.jpg",
    },
    {"id": 23, "name": "Power Bank", "price": 1200, "image": "images/powerbank.jpg"},
    {"id": 24, "name": "Smart Watch", "price": 8000, "image": "images/watch.jpg"},
    {"id": 25, "name": "Tablet", "price": 20000, "image": "images/tablet.jpg"},
    {"id": 26, "name": "AC", "price": 92000, "image": "images/ac2.jpg"},
    {"id": 27, "name": "AC", "price": 92000, "image": "images/ac3.jpg"},
    {"id": 28, "name": "AC", "price": 92000, "image": "images/ac4.jpg"},
    {"id": 29, "name": "AC", "price": 92000, "image": "images/ac5.jpg"},
    {"id": 30, "name": "AC", "price": 92000, "image": "images/ac6.jpg"},
    {"id": 31, "name": "AC", "price": 92000, "image": "images/ac7.jpg"},
    {"id": 32, "name": "AC", "price": 92000, "image": "images/ac8.jpg"},
    {"id": 33, "name": "AC", "price": 92000, "image": "images/ac9.jpg"},
    {"id": 34, "name": "AC", "price": 92000, "image": "images/ac10.jpg"},
    {"id": 35, "name": "AC", "price": 92000, "image": "images/ac11.jpg"},
    {"id": 36, "name": "AC", "price": 92000, "image": "images/ac12.jpg"},
    {"id": 37, "name": "AC", "price": 92000, "image": "images/ac13.jpg"},
    {"id": 38, "name": "AC", "price": 92000, "image": "images/ac14.jpg"},
    {"id": 39, "name": "Fridge", "price": 35000, "image": "images/fridge3.jpg"},
    {"id": 40, "name": "Fridge", "price": 35000, "image": "images/fridge4.jpg"},
    {"id": 41, "name": "Fridge", "price": 35000, "image": "images/fridge5.jpg"},
    {"id": 42, "name": "Fridge", "price": 35000, "image": "images/fridge6.jpg"},
    {"id": 43, "name": "Fridge", "price": 35000, "image": "images/fridge7.jpg"},
    {"id": 44, "name": "Fridge", "price": 35000, "image": "images/fridge8.jpg"},
    {"id": 45, "name": "Fridge", "price": 35000, "image": "images/fridge9.jpg"},
    {"id": 46, "name": "Fridge", "price": 35000, "image": "images/fridge10.jpg"},
    {"id": 47, "name": "Fridge", "price": 35000, "image": "images/fridge11.jpg"},
    {"id": 48, "name": "Fridge", "price": 35000, "image": "images/fridge12.jpg"},
    {
        "id": 49,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine1.jpg",
    },
    {
        "id": 50,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine2.jpg",
    },
        
    
    {
        "id": 51,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine3.jpg",
    },
    {
        "id": 52,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine4.jpg",
    },
    {
        "id": 53,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine5.jpg",
    },
    {
        "id": 54,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine6.jpg",
    },
    {
        "id": 55,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine7.jpg",
    },
    {
        "id": 56,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine8.jpg",
    },
    
    {
        "id": 58,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine10.jpg",
    },
    {
        "id": 59,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine11.jpg",
    },
    {
        "id": 60,
        "name": "Washing Machine",
        "price": 25000,
        "image": "images/washingmachine12.jpg",
    },
    {"id": 61, "name": "TV", "price": 30000, "image": "images/tv1.jpg"},
    {"id": 62, "name": "TV", "price": 30000, "image": "images/tv2.jpg"},
    {"id": 63, "name": "TV", "price": 30000, "image": "images/tv3.jpg"},
    {"id": 64, "name": "TV", "price": 30000, "image": "images/tv4.jpg"},
    {"id": 65, "name": "TV", "price": 30000, "image": "images/tv5.jpg"},
    {"id": 66, "name": "TV", "price": 30000, "image": "images/tv6.jpg"},
    {"id": 67, "name": "TV", "price": 30000, "image": "images/tv7.jpg"},
    {"id": 68, "name": "TV", "price": 30000, "image": "images/tv8.jpg"},
    {"id": 69, "name": "TV", "price": 30000, "image": "images/tv9.jpg"},
    {"id": 70, "name": "Headphones", "price": 2500, "image": "images/headphone2.jpg"},
    {"id": 71, "name": "Headphones", "price": 2500, "image": "images/headphone3.jpg"},
    {"id": 72, "name": "Headphones", "price": 2500, "image": "images/headphone4.jpg"},
    {"id": 73, "name": "Headphones", "price": 2500, "image": "images/headphone5.jpg"},
    {"id": 74, "name": "Headphones", "price": 2500, "image": "images/headphone6.jpg"},
    {"id": 75, "name": "Headphones", "price": 2500, "image": "images/headphone7.jpg"},
    {"id": 76, "name": "Headphones", "price": 2500, "image": "images/headphone8.jpg"},
    {"id": 77, "name": "Headphones", "price": 2500, "image": "images/headphone9.jpg"},
    {"id": 78, "name": "Headphones", "price": 2500, "image": "images/headphone10.jpg"},
    {"id": 79, "name": "Phone", "price": 35000, "image": "images/phone2.jpg"},
    {"id": 80, "name": "Phone", "price": 35000, "image": "images/phone3.jpg"},
    {"id": 81, "name": "Phone", "price": 35000, "image": "images/phone4.jpg"},
    {"id": 82, "name": "Phone", "price": 35000, "image": "images/phone5.jpg"},
    {"id": 83, "name": "Phone", "price": 35000, "image": "images/phone6.jpg"},
    {"id": 84, "name": "Phone", "price": 35000, "image": "images/phone7.jpg"},
    {"id": 85, "name": "Phone", "price": 35000, "image": "images/phone8.jpg"},
    {"id": 86, "name": "Phone", "price": 35000, "image": "images/phone9.jpg"},
    {"id": 87, "name": "Phone", "price": 35000, "image": "images/phone10.jpg"},
    {"id": 88, "name": "Phone", "price": 35000, "image": "images/phone11.jpg"},
    {"id": 89, "name": "Phone", "price": 35000, "image": "images/phone12.jpg"},
]

# --- Registration Routes ---

# 1. Route to show the Signup Page
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

# 2. Route to handle the Form Data
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    mobile = request.form.get("mobile")
    password = request.form.get("password")

    try:
        conn = get_db()
        
        conn.execute("INSERT INTO users (username, email, mobile, password) VALUES (?, ?, ?, ?)",
                     (username, email, mobile, password))
        conn.commit()
        conn.close()
        
        session["user"] = username
        flash("Registration Successful!", "success") 
        return redirect(url_for('home'))

    except sqlite3.IntegrityError:
        
        flash("❌ Email or Username already exists! Please Login.", "error") 
        return redirect(url_for('signup_page')) 


@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db()
    
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password)).fetchone()
    conn.close()

    if user:
        
        session["user"] = user["username"]
        
        
        if session.get("pending_checkout"):
            return redirect(url_for('card'))
        
        
        return redirect(url_for('card'))
    else:
        
        flash("❌ Invalid Email or Password!", "error")
        return redirect(url_for('login_page'))
    

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_msg = data["message"].lower()

    if "otp" in user_msg:
        reply = "OTP has been sent to your registered mobile number. Please do not share it with anyone."
    elif "fraud" in user_msg:
        reply = "Our AI system monitors unusual transactions and blocks suspicious payments automatically."
    elif "amount" in user_msg:
        reply = "Your payment amount is displayed in the amount field on the screen."
    elif "card" in user_msg:
        reply = "We support Visa, MasterCard, RuPay and American Express cards."
    else:
        reply = random.choice(
            [
                "I'm here to help you with secure payments and fraud detection.",
                "Your transaction is protected with AI-based fraud monitoring.",
                "Feel free to ask about OTP, payments or card security.",
            ]
        )

    return jsonify({"reply": reply})

@app.route("/")
def index():
    return render_template("main.html")


@app.route("/shop")
def home():
    return render_template("products.html", products=products)

@app.route("/chatbot", methods=["POST"])

# ================= SEARCH API =================
@app.route("/search/<product>")
def search_product(product):
    results = []
    for p in products:
        if product.lower() in p["name"].lower():
            results.append(
                {
                    "id": p["id"],
                    "name": p["name"],
                    "price": p["price"],
                    "image": url_for("static", filename=p["image"]),
                }
            )
    return jsonify(results)

@app.route("/filter/<category>")  
def filter_products(category):
    cat = category.lower()
    
    if cat == "all":
        return jsonify(products)

    # Fuzzy logic: checks if category is in name OR name is in category
    # This solves the "Fridge" vs "Fridges" problem
    filtered = [
        p for p in products 
        if cat in p['name'].lower() or p['name'].lower() in cat
    ]
    
    return jsonify(filtered)


# ================= PAY NOW =================
@app.route("/pay/<int:product_id>")
def pay(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404

    
    session["item"] = product["name"]
    session["amount"] = product["price"]
    session["item_image"] = product["image"]
    session["pending_checkout"] = True 

    if "user" not in session:
        return redirect(url_for("signup_page"))

    return redirect(url_for("card"))

@app.route("/history")
def history():
    conn = get_db()
    rows = conn.execute("SELECT * FROM transactions ORDER BY id DESC").fetchall()
    total = len(rows)
    success = len([r for r in rows if "Successful" in r['status']])
    failed = total - success
    success_amount = sum(r['amount'] for r in rows if "Successful" in r['status'])
    
    conn.close()
    return render_template("history.html", 
                           history=rows, 
                           total=total, 
                           success=success, 
                           failed=failed, 
                           success_amount=success_amount)


# PDF DOWNLOAD ROUTE
@app.route("/download-statement")
def download_statement():
    conn = get_db()
    transactions = conn.execute("SELECT * FROM transactions ORDER BY time DESC").fetchall()
    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("SmartPay Bank Statement", styles["Title"]))
    elements.append(Spacer(1, 12))

    data = [["Date", "Card", "Amount", "Status"]]

    for tx in transactions:
        data.append([
            tx["time"],
            "**** " + tx["card_last4"],
            "₹" + str(tx["amount"]),
            tx["status"]
        ])

    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="SmartPay_Statement.pdf",
        mimetype="application/pdf"
    )
# ================= FEEDBACK =================
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

# ================= HELP =================
@app.route("/help")
def help_page():
    return render_template("help.html")

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404

    conn = get_db()

    reviews = conn.execute(
        "SELECT * FROM reviews WHERE product_id=? ORDER BY id DESC",
        (product_id,)
    ).fetchall()

    avg = conn.execute(
        "SELECT AVG(rating) FROM reviews WHERE product_id=?",
        (product_id,)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "product_detail.html",
        product=product,
        reviews=reviews,
        avg_rating=round(avg,1) if avg else 0
    )
@app.route("/add_review/<int:product_id>", methods=["POST"])
def add_review(product_id):
    rating = int(request.form.get("rating"))
    comment = request.form.get("comment")

    conn = get_db()
    conn.execute("""
        INSERT INTO reviews (product_id, rating, comment, time)
        VALUES (?, ?, ?, datetime('now'))
    """, (product_id, rating, comment))

    conn.commit()
    conn.close()

    return redirect(f"/product/{product_id}")

# ================= RUN =================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)