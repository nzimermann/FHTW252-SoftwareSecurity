import random
import string
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/generate", methods=["GET"])
def generate_passwords():
    quantity = int(request.args.get("quantity", 1))
    length = int(request.args.get("length", 15))
    alphabet = request.args.get("alphabet", "3")

    letters = string.ascii_letters
    numbers = string.digits
    punctuation = string.punctuation.replace(
        "\\", ""
    )  # remove the backslash to avoid JSON escape sequences

    characters = {
        "1": letters,
        "2": letters + numbers,
        "3": letters + numbers + punctuation,
    }.get(alphabet, "3")

    passwords = []

    for _ in range(quantity):
        pwd = "".join(random.choice(characters) for i in range(length))
        passwords.append(pwd)

    return jsonify({"passwords": passwords})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
