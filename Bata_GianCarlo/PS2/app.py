import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)


def append_to_json(filename, new_data):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_data)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


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
