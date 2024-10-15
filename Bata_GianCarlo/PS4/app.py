import hashlib
from flask import Flask, render_template, request, redirect, session, flash
from database import DBManager

app = Flask(__name__)
app.secret_key = (
    "my super duper secret key that only I know of... except if you read it here"
)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': None,
    'database': 'adet',
}

db_manager = DBManager(db_config)

db_manager.create_database()
db_manager.create_users_table()


def sha256_hash(password):
    password_bytes = password.encode("utf-8")
    sha256 = hashlib.sha256()
    sha256.update(password_bytes)
    return sha256.hexdigest()

def check_password(stored_hash, provided_password):
    hashed_provided_password = sha256_hash(provided_password)
    return stored_hash == hashed_provided_password


@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        username = session['username']
        user = db_manager.get_user_by_username(username)
        print(user)
        return render_template('dashboard.html', user=user)
    
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")
        contact_number = request.form.get("contact_number")
        email = request.form["email"]
        address = request.form.get("address")
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect("/signup")

        hashed_password = sha256_hash(password)

        existing_user = db_manager.get_user_by_username(username)
        if existing_user:
            flash("Username already taken!", "error")
            return redirect("/signup")

        db_manager.create_user(
            username,
            first_name,
            middle_name,
            last_name,
            contact_number,
            email,
            address,
            hashed_password,
        )
        flash("Signup successful! You can now log in.", "success")
        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db_manager.get_user_by_username(username)
        if user and check_password(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)