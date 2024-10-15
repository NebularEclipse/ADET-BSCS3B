import secrets
from database import DBManager
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key
Bootstrap(app)

database = DBManager("localhost", "root", None, "adet")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/greetings", methods=["POST"])
def greetings():
    table_name = "adet_user"
    schema = """
        id INT AUTO_INCREMENT PRIMARY KEY,
        f_name VARCHAR(255),
        m_name VARCHAR(255),
        l_name VARCHAR(255),
        contact VARCHAR(20),
        email VARCHAR(255),
        address VARCHAR(255)
    """
    database.create_table(table_name, schema)
    f_name = request.form.get("f_name")
    m_name = request.form.get("m_name")
    l_name = request.form.get("l_name")
    contact = request.form.get("contact_no")
    email = request.form.get("email")
    address = request.form.get("address")
    columns = ["f_name", "m_name", "l_name", "contact", "email", "address"]
    values = (f_name, m_name, l_name, contact, email, address)
    database.insert_data(table_name, columns, values)
    return render_template("greetings.html")


if __name__ == "__main__":
    app.run(debug=True)
