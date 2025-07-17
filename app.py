from flask import Flask, jsonify
import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import traceback

app = Flask(__name__)
load_dotenv()

HA_TOKEN = os.getenv("HA_TOKEN", "").strip()
HA_URL = os.getenv("HA_URL", "").strip()
ENTITY_ID = os.getenv("ENTITY_ID", "").strip()
CHANNEL_ID = "UCCxF55adGXOscJ3L8qdKnrQ"

@app.route("/update_bryson", methods=["POST"])
def update_bryson_video():
    try:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(rss_url, headers=headers)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        video_id = root.find(".//{http://www.youtube.com/xml/schemas/2015}videoId").text
        latest_video_url = f"https://www.youtube.com/watch?v={video_id}"

        ha_api_url = f"{HA_URL}/api/states/{ENTITY_ID}"
        ha_headers = {
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"state": latest_video_url}
    
        res = requests.post(ha_api_url, headers=ha_headers, json=payload)
        res.raise_for_status()

        return jsonify({"success": True, "url": latest_video_url})
    except Exception as e:
        traceback.print_exc()  # Logs full stack trace to console or Docker logs
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
