import hashlib
import secrets
from database import DBManager
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key
Bootstrap(app)

database = DBManager("localhost", "root", None, "adet")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/sign_in", methods=["POST"])
def sign_in():
    pass


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    table_name = "adet_user"
    schema = """
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        first_name VARCHAR(255),
        middle_name VARCHAR(255),
        last_name VARCHAR(255),
        contact_number VARCHAR(50),
        email VARCHAR(255) UNIQUE,
        address VARCHAR(255),
        password VARCHAR(255)
    """

    database.create_table(table_name, schema)

    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        address = request.form.get("address")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("sign_up"))

        database.cursor.execute(
            f"SELECT * FROM {table_name} WHERE username = %s OR email = %s",
            (username, email),
        )
        existing_user_or_email = database.cursor.fetchone()

        if existing_user_or_email:
            flash(
                "Username or email is already taken. Please choose a different one.",
                "error",
            )
        else:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            columns = [
                "username",
                "first_name",
                "middle_name",
                "last_name",
                "contact_number",
                "email",
                "address",
                "password",
            ]
            values = (
                username,
                first_name,
                middle_name,
                last_name,
                contact_number,
                email,
                address,
                hashed_password,
            )
            database.insert_data(table_name, columns, values)
            flash("Account created successfully!", "success")

        return redirect(url_for("index"))

    return render_template("sign_up.html")


if __name__ == "__main__":
    app.run(debug=True)
