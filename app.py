from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
HISTORY_FILE = "chat_history.txt"


def save_message(role, message):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{role}:{message}\n")


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return ""
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return "".join([
            f"<p><strong>{'Você' if line.startswith('user:') else 'Bot'}:</strong> {line.split(':', 1)[1]}</p>"
            for line in lines
        ])


@app.route("/")
def index():
    chat_history = load_history()
    return render_template("index.html", history=chat_history)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    save_message("user", message)

    # Simula uma resposta do bot
    response = f"Você disse: {message}"
    save_message("bot", response)
    return jsonify({"response": response})


@app.route("/tweet", methods=["POST"])
def tweet():
    data = request.json
    message = data.get("message")
    save_message("user", f"[Tweet] {message}")

    response = "Tweet simulado com sucesso!"
    save_message("bot", response)
    return jsonify({"message": response})


@app.route("/clear", methods=["POST"])
def clear():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
