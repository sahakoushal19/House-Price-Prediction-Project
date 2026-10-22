# House Price Prediction Project

## Project Overview

This project is a web-based House Price Prediction System developed using Python, Django, and Machine Learning. It predicts house prices based on user-provided property details and location.

## Technologies Used

* Python
* Django
* Scikit-learn
* Pandas and NumPy
* HTML and CSS
* Machine Learning

## Features

* Predict house prices using a trained machine learning model.
* Select property locations and view location-based pricing.
* User registration and login functionality.
* Store and view prediction history.
* Responsive web interface.

## Project Structure

* predictor/ – Django application containing views, models, forms, and templates.
* ml_model/ – Machine learning model training code.
* static/ – CSS and other static files.
* templates/ – HTML templates.
* house_price_model.pkl – Trained machine learning model.
* house_prices_city_dataset.csv – Dataset used for price prediction.
* manage.py – Django management utility.

## How to Run the Project

1. Clone this repository:
   git clone https://github.com/sahakoushal19/House-Price-Prediction-Project.git

2. Open the project folder and navigate to the Django project directory.

3. Install the required dependencies:
   pip install django pandas numpy scikit-learn

4. Apply database migrations:
   python manage.py migrate

5. Start the development server:
   python manage.py runserver

6. Open http://127.0.0.1:8000/ in your browser.

## Author
Rohan Saha

## Note
This project is intended for educational purposes. Prediction accuracy depends on the dataset and the trained machine learning model.
