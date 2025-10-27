import os, requests
from flask import Flask, request, jsonify

app = Flask(__name__)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise SystemExit("Set RAPIDAPI_KEY environment variable")

HEADERS = {"x-rapidapi-key": RAPIDAPI_KEY}

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json() or {}
    url = data.get("url")
    if not url:
        return jsonify({"error":"missing url"}), 400

    # Example: TikTok API (RapidAPI)
    if "tiktok.com" in url:
        try:
            HOST = "tiktok-downloader-download-videos-without-watermark.p.rapidapi.com"
            r = requests.get(f"https://{HOST}/index", headers=HEADERS, params={"url": url}, timeout=30)
            r.raise_for_status()
            js = r.json()
            media_url = js.get("video") or js.get("url") or js.get("data", {}).get("play")
            return jsonify({"media_url": media_url})
        except Exception as e:
            return jsonify({"error": f"TikTok API error: {e}"}), 502

    # Example: Instagram API (RapidAPI)
    if "instagram.com" in url:
        try:
            HOST = "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
            r = requests.get(f"https://{HOST}/index", headers=HEADERS, params={"url": url}, timeout=30)
            r.raise_for_status()
            js = r.json()
            media_url = js.get("media") or js.get("url") or js.get("data", {}).get("video")
            return jsonify({"media_url": media_url})
        except Exception as e:
            return jsonify({"error": f"Instagram API error: {e}"}), 502

    return jsonify({"error": "unsupported link"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
