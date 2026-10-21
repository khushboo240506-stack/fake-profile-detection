from dotenv import load_dotenv
from pathlib import Path
import os

import joblib
import pandas as pd
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

MODEL_PATH = BASE_DIR / "model" / "fake_profile_model.joblib"

# Load trained machine-learning model
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH}. Run backend/train_model.py first."
    )

model = joblib.load(MODEL_PATH)


# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Fake Profile Detection API is running"
    })


# Predict whether a profile appears fake or genuine
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}

    bio = str(data.get("bio", "")).strip()
    username = str(data.get("username", "")).strip()

    if not bio:
        return jsonify({
            "error": "Please enter the profile bio."
        }), 400

    try:
        followers = int(data.get("followers", 0))
        following = int(data.get("following", 0))
        posts = int(data.get("posts", 0))
        account_age_days = int(data.get("account_age_days", 0))
    except (ValueError, TypeError):
        return jsonify({
            "error": "Profile numbers must be valid integers."
        }), 400

    numbers = [followers, following, posts, account_age_days]

    if any(number < 0 for number in numbers):
        return jsonify({
            "error": "Profile numbers cannot be negative."
        }), 400

    if any(number > 1000000000 for number in numbers):
        return jsonify({
            "error": "Profile numbers are too large."
        }), 400

    # Prepare input for the ML model
    profile = pd.DataFrame([{
        "bio": bio,
        "followers": followers,
        "following": following,
        "posts": posts,
        "account_age_days": account_age_days
    }])

    # Generate prediction
    try:
        prediction = str(model.predict(profile)[0])

        confidence = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(profile)[0]
            confidence = round(float(max(probabilities)) * 100, 2)

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "The model could not analyze this profile."
        }), 500

    # Save prediction in MySQL
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO predictions
            (username, bio, followers, following, posts,
             account_age_days, prediction, confidence)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            username,
            bio,
            followers,
            following,
            posts,
            account_age_days,
            prediction,
            confidence
        ))

        connection.commit()

    except Error:
        app.logger.exception("Failed to save prediction in MySQL")

        return jsonify({
            "error": (
                "Prediction was generated, but saving to MySQL failed. "
                "Check your database credentials and predictions table columns."
            ),
            "prediction": prediction,
            "confidence": confidence
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

    # Send result to frontend
    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "notice": (
            "Experimental estimate based on the supplied information; "
            "not proof that a profile is fake or genuine."
        )
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)