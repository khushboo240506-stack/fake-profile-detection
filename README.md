# Fake Profile Detection on Social Media Using NLP

## Live Demo

- **Website:** https://fake-profile-detection-website.onrender.com
- **Backend API:** https://fake-profile-detection-td2r.onrender.com

## Project Overview

A web application that uses Natural Language Processing (NLP) and Machine Learning to estimate whether a social media profile appears fake or genuine.

## Technologies Used

- Python
- Flask
- Pandas
- Scikit-learn
- TF-IDF Vectorization
- Random Forest Classifier
- HTML, CSS, JavaScript
- MySQL

## Features

- Profile information input form
- Experimental fake/genuine profile prediction
- Model confidence display
- MySQL prediction history
- Input validation

## How to Run Locally

1. Open the project folder in VS Code.
2. Activate the virtual environment:

   `.\venv\Scripts\Activate.ps1`

3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Start the backend:

   `python backend\app.py`

5. Open a second terminal and start the frontend:

   `python -m http.server 8000 --directory frontend`

6. Open http://localhost:8000 in your browser.

## Database

- **Database:** `fake_profile_detection`
- **Table:** `predictions`

Configure database credentials using a local `.env` file. Never upload `.env` or expose database passwords on GitHub.

## Limitations

The dataset currently contains only 10 demonstration profiles. Predictions are experimental and cannot reliably establish whether a real account is fake or genuine.

## Conclusion

This project demonstrates the integration of NLP, Machine Learning, Flask, frontend web technologies, and MySQL in a web-based application.
