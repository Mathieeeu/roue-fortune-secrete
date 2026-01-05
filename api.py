from flask import Flask, Response

app = Flask(__name__)

@app.route("/logger")
def get_logs():
    try:
        with open("script.log", "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype="text/plain")
    except FileNotFoundError:
        return Response("Aucun log trouvé.", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200)
