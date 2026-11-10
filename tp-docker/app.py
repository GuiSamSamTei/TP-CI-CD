from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

@app.route("/")
def hello_world():
    try:
        dbmongo.cx.admin.command("ping")
        status = "Healthy"
        response_code = 200
    except Exception:
        status = "Unhealthy"
        response_code = 503
        app.logger.exception("MongoDB health check failed")
    return f"<p>Hello, World!</p><p>Database status: {status}</p>", response_code

app.config["MONGO_URI"] = "mongodb://mongo:27017/tp-docker"

dbmongo = PyMongo(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)