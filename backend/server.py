from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # allow React frontend to call the backend

@app.route("/run-passwords")
def run_passwords():
    try:
        # Build absolute path to GeneratePasswords.py
        base_dir = os.path.abspath(os.path.dirname(__file__))  # /backend
        frontend_public = os.path.abspath(os.path.join(base_dir, "..", "gen-pass-demo-frontend", "public"))
        script_path = os.path.join(frontend_public, "GeneratePasswords.py")

        print("Running:", script_path)

        # Execute the Python script
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)

        # Optional: print script output to backend console
        print(result.stdout)
        print(result.stderr)

        if result.returncode != 0:
            return jsonify({"status": "error", "message": result.stderr}), 500

        return jsonify({"status": "ok", "message": "Passwords generated."})

    except Exception as e:
        return jsonify({"status": "exception", "message": str(e)}), 500


@app.route("/")
def home():
    return "Flask backend is running!"


if __name__ == "__main__":
    app.run(port=5001)
