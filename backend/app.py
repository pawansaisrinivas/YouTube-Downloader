from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS

# Folder to save downloaded files
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/formats", methods=["POST"])
def get_video_formats():
    """Fetch available formats for a given YouTube video URL."""
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = []
            seen_resolutions = set()  # ✅ Store unique resolutions
            
            # Extract available formats (MP4 only)
            for f in info.get("formats", []):
                if f.get("height") and f.get("ext") == "mp4":
                    resolution = f"{f['height']}p"
                    if resolution not in seen_resolutions:
                        seen_resolutions.add(resolution)
                        formats.append({"format_id": f["format_id"], "resolution": resolution})
            
            return jsonify({"formats": formats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["POST"])
def download_video():
    """Download a YouTube video with user-selected quality."""
    data = request.json
    video_url = data.get("url")
    format_id = data.get("format_id")  # User-selected format ID

    if not video_url or not format_id:
        return jsonify({"error": "Invalid input data"}), 400

    ydl_opts = {
        'format': format_id,  # Use selected format ID
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({"download_link": f"http://localhost:5000/downloads/{os.path.basename(filename)}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/convert", methods=["POST"])
def convert_to_mp3():
    """Convert a YouTube video to MP3."""
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return jsonify({"mp3_download_link": f"http://localhost:5000/downloads/{os.path.basename(filename)}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/downloads/<path:filename>')
def serve_file(filename):
    """Serve the downloaded file."""
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
