from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import json
import os

app = Flask(__name__)
Bootstrap(app)


def append_to_json(filepath, data):
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            json.dump([], file, indent=4)

    with open(filepath, "r+") as file:
        old_data = json.load(file)
        old_data.append(data)
        file.seek(0)
        json.dump(old_data, file, indent=4)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/greetings", methods=["POST"])
def greetings():
    dict = {}
    data = request.form.to_dict()
    filepath = "data.json"
    append_to_json(filepath, data)
    return render_template("greetings.html")


if __name__ == "__main__":
    app.run(debug=True)
