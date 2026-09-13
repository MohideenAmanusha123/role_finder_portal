"""
app.py
------
Flask web portal: upload a resume, get back ranked role matches.

Run with:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
import tempfile

from flask import Flask, render_template, request, jsonify

from resume_matcher import analyze_resume, UnsupportedFileType
from roles_data import ROLES

app = Flask(__name__)
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


@app.route("/")
def index():
    return render_template("index.html", roles=list(ROLES.keys()))


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No file was uploaded."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file was selected."}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Please upload a .pdf, .docx, or .txt file."}), 400

    target_role = request.form.get("target_role", "").strip()
    if target_role not in ROLES:
        target_role = None

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = analyze_resume(tmp_path, target_role=target_role)
        result["filename"] = file.filename
        return jsonify(result)
    except UnsupportedFileType as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Could not process this file: {e}"}), 500
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


if __name__ == "__main__":
    # PORT is set automatically by most free hosting platforms (Render, etc.);
    # locally it falls back to 5000. debug=True is safe for local dev only —
    # hosting platforms run this file via gunicorn instead (see Procfile),
    # which never triggers this block.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
