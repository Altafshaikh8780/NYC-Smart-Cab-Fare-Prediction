# 🚕 NYC Smart Cab Fare System

A Machine Learning based dynamic cab fare prediction system with an interactive and responsive web interface built using Streamlit.

🔗 **Live Application:**  
https://nyc-cab-fare-system.streamlit.app

---

## 📌 Project Overview

NYC Smart Cab Fare System predicts taxi fares using a trained Machine Learning model combined with real-world business logic rules such as:

- Night surcharge
- Rush hour surge pricing
- Weather-based multiplier
- Booking fee
- Passenger-based pricing

The system also includes interactive route visualization using PyDeck.

---

## ✨ Key Features

- 📍 Pickup & Dropoff location selection
- 🗺️ Route visualization on interactive map
- 📏 Distance calculation using Haversine formula
- 👥 Passenger-based pricing adjustment
- 🌙 Night surcharge (8 PM – 6 AM)
- 🔥 Rush hour surge pricing (4 PM – 7 PM)
- 🌦 Weather-based fare multiplier
- 💳 Minimum fare rule
- 📊 Professional fare breakdown display
- 🎨 Responsive modern UI
- 🌍 Deployed on Streamlit Cloud

---

## 🧠 How It Works

### 1️⃣ Base Fare Prediction

The trained ML model predicts base fare using:

- Pickup latitude
- Pickup longitude
- Dropoff latitude
- Dropoff longitude
- Passenger count
- Distance (calculated using Haversine formula)
- Hour of the day

---

### 2️⃣ Dynamic Pricing Layer

After ML prediction, additional business rules are applied:

- Minimum fare enforcement
- Night surcharge
- Rush hour surge multiplier
- Weather multiplier
- Booking fee
- Per-passenger additional charge

Final Fare Formula:

Final Fare =  
(Base Fare + Night Charge + Booking Fee + Passenger Charge)  
× Surge Multiplier × Weather Multiplier

---

## 🛠 Tech Stack

- Python
- Streamlit
- Scikit-Learn
- NumPy
- Pandas
- PyDeck
- Joblib

---

## 📂 Project Structure
-NYC-Smart-Cab-Fare-Prediction/
-|
-├── CFP.py
-├── cab_fare_model.pkl
-├── requirements.txt
-└── README.md

---


## ▶️ How To Run Locally


### 1️⃣ Clone the repository

- git clone https://github.com/Altafshaikh8780/NYC-Smart-Cab-Fare-Prediction.git



### 2️⃣ Navigate to the project folder
- cd NYC-Smart-Cab-Fare-Prediction


### 3️⃣ Install dependencies
- pip install -r requirements.txt


### 4️⃣ Run the Streamlit app
- streamlit run CFP.py


---

## 🌍 Deployment

The application is deployed using **Streamlit Cloud** and connected directly to the GitHub repository.

Every push to the `main` branch automatically updates the live app.

---

## 🎓 Academic Context

This project was developed as a Final Year BCA project demonstrating:

- Machine Learning model deployment
- Real-world pricing simulation
- UI/UX integration
- Cloud deployment using Streamlit
- GitHub version control workflow

---

## 👨‍💻 Developed By

**Altaf Shaikh**  
Bachelor of Computer Applications (BCA)  
Final Year Minor Project

---

## 📈 Future Improvements

- Real-time traffic-based pricing
- Google Maps API integration
- Trip history logging
- Admin dashboard with analytics
- Invoice PDF generation
- User authentication system

---

## 📜 License

This project is developed for Academic and Educational purposes.
