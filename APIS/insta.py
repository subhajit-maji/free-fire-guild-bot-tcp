# ------------------------------------------------------------
# Instagram Info API — Credit: SM (@SubhajitMajiRobot)
# JOIN    : @SubhajitMajiRobot  FOR MORE SRC | API | BOT CODE | METHOD | 🛐
# Purpose : Fetch profile & recent media (public + optional session-based)
# Note    : THIS CODE MADE BY SM @SubhajitMajiRobot (GIVE CREDIT OTHERWISE EVERYONE **** YOU AT 300 KM SPEED)
# Usage   : /api/insta/<username>?
# License : Personal / internal use only — retain credit when sharing
# ------------------------------------------------------------

from flask import Flask, jsonify, request
import requests
import time
import socket
from functools import lru_cache

app = Flask(__name__)

# DONT REMOVE THIS BRUH
@lru_cache(maxsize=1024)
def fetch_instagram_profile(username, proxy=None):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "x-ig-app-id": "936619743392459",
        "Referer": f"https://www.instagram.com/{username}/",
    }
    session = requests.Session()
    proxies = {"http": proxy, "https": proxy} if proxy else None

    backoff = 1
    for attempt in range(4):
        try:
            resp = session.get(url, headers=headers, timeout=10, proxies=proxies)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code in (429, 403):
                # rate limited or blocked
                time.sleep(backoff)
                backoff *= 2
            elif resp.status_code == 404:
                return {"error": "not_found", "status_code": 404}
            else:
                return {
                    "error": "http_error",
                    "status_code": resp.status_code,
                    "body": resp.text[:500],
                }
        except requests.RequestException:
            time.sleep(backoff)
            backoff *= 2
    return {"error": "request_failed"}


@app.route("/api/insta/<username>", methods=["GET"])
def insta_info(username):
    proxy = request.args.get("proxy")  # optional proxy
    data = fetch_instagram_profile(username, proxy=proxy)
    if data is None:
        return jsonify({"error": "no_response"}), 502

    if "error" in data:
        return jsonify(data), (data.get("status_code") or 400)

    try:
        user = data.get("data", {}).get("user") or data.get("user") or data.get("data")
        if not user:
            return jsonify({"raw": data})

        out = {
            "id": user.get("id"),
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "biography": user.get("biography"),
            "is_private": user.get("is_private"),
            "is_verified": user.get("is_verified"),
            "profile_pic_url": user.get("profile_pic_url_hd")
                              or user.get("profile_pic_url"),
            "followers_count": (
                user.get("edge_followed_by", {}).get("count")
                or user.get("followers_count")
            ),
            "following_count": (
                user.get("edge_follow", {}).get("count")
                or user.get("following_count")
            ),
            "media_count": (
                user.get("media_count")
                or user.get("edge_owner_to_timeline_media", {}).get("count")
            ),
            "recent_media": [],
        }

        media = (
            user.get("edge_owner_to_timeline_media")
            or user.get("media")
            or {}
        )
        edges = media.get("edges") or media.get("items") or []
        for e in edges[:8]:
            node = e.get("node") if isinstance(e, dict) and e.get("node") else e
            if not node:
                continue
            caption = None
            if node.get("edge_media_to_caption"):
                edges_caption = node["edge_media_to_caption"].get("edges") or []
                if edges_caption and "node" in edges_caption[0]:
                    caption = edges_caption[0]["node"].get("text")
            else:
                caption = node.get("caption")

            out["recent_media"].append({
                "id": node.get("id"),
                "shortcode": node.get("shortcode"),
                "display_url": node.get("display_url")
                               or node.get("display_src"),
                "taken_at": node.get("taken_at_timestamp")
                             or node.get("taken_at"),
                "caption": caption,
            })
        return jsonify(out)
    except Exception as exc:
        return jsonify({
            "error": "parse_error",
            "details": str(exc),
            "raw": data
        }), 500
        
def find_free_port(start=8080, end=65535):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('0.0.0.0', port)) != 0:
                return port
    raise RuntimeError("No free port available")

if __name__ == "__main__":
    port = find_free_port()
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
