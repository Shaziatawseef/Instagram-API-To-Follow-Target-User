from flask import Flask, request, jsonify
from instagrapi import Client
import os

app = Flask(__name__)


def get_client(sessionid: str) -> Client:
    """Initialize and return an Instagrapi client with sessionid."""
    cl = Client()
    try:
        cl.login_by_sessionid(sessionid)
    except Exception as e:
        raise ValueError(f"Invalid sessionid or login failed: {str(e)}")
    return cl


@app.route("/instagram", methods=["GET"])
def follow_user():
    sessionid = request.args.get("sessionid")
    user_id = request.args.get("id")

    if not sessionid or not user_id:
        return jsonify({
            "success": False,
            "error": "Missing required query parameters: sessionid and id"
        }), 400

    try:
        cl = get_client(sessionid)
        result = cl.user_follow(int(user_id))

        return jsonify({
            "success": True,
            "followed_user_id": user_id,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Instagram Follow API is running. Use /follow?sessionid=...&id=..."
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
