# Fake Profile Detection on Social Media Using NLP

## Project Overview
A web application that uses Natural Language Processing and Machine Learning to estimate whether a social media profile appears fake or genuine.

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

## How to Run
1. Activate the virtual environment.
2. Install dependencies using: python -m pip install -r requirements.txt
3. Start the backend using: python backend\app.py
4. Start the frontend using: python -m http.server 8000 --directory frontend
5. Open http://localhost:8000 in your browser.

## Database
Database: fake_profile_detection
Table: predictions

Configure database credentials using a local .env file. Never upload .env to GitHub.

## Limitations
The dataset currently contains only 10 demonstration profiles. Predictions are experimental and cannot reliably establish whether a real account is fake or genuine.

## Conclusion
This project demonstrates a basic integration of NLP, Machine Learning, Flask, frontend web technologies, and MySQL.
