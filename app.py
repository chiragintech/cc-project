from flask import Flask, request, jsonify, redirect
import redis
import hashlib

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.route("/shorten", methods=["POST"])
def shorten_url():
    """Generate a short URL from a long URL."""
    data = request.get_json()
    long_url = data.get("long_url")

    if not long_url:
        return jsonify({"error": "Missing URL"}), 400

    url_hash = hashlib.md5(long_url.encode()).hexdigest()[:6]
    redis_client.set(url_hash, long_url)
    
    short_url = f"http://localhost:5000/{url_hash}"
    return jsonify({"short_url": short_url})

@app.route("/<short_url>")
def redirect_url(short_url):
    """Redirect to the original URL."""
    long_url = redis_client.get(short_url)
    
    if long_url:
        return redirect(long_url, code=302)
    
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)