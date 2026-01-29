# 🎯 ML Placement Predictor

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

An **end-to-end Machine Learning project** that predicts **student placement** based on **CGPA** and **IQ scores**, wrapped in an interactive web application with **fun Hindi messages** 🇮🇳😄.

---

## ✨ Features

* 🤖 **ML Prediction** – Predicts student placement using a trained classification model
* 🎨 **Interactive UI** – Clean, responsive frontend with real-time feedback
* 😂 **Fun Hindi Messages** – Entertaining responses based on prediction results

  * ✅ Placed: *"🎯 Placement hogya! Jaa, jee le apni zindagi! 🥳"*
  * ❌ Not Placed: *"😢 Nhi hoga placement! Lage reh! 📚"*
* 📊 **Visualizations** – Charts showing placement statistics and data distribution
* ⚡ **Real-time Predictions** – Instant results with confidence scores
* 📱 **Responsive Design** – Works on desktop, tablet, and mobile

---

## 📸 Screenshots

<div align="center">
  <img src="https://via.placeholder.com/800x450/667eea/ffffff?text=Placement+Prediction+Interface" width="400" alt="Interface">
  <img src="https://via.placeholder.com/800x450/764ba2/ffffff?text=Results+with+Fun+Messages" width="400" alt="Results">
</div>

---

## 🚀 Quick Start

### Prerequisites

* Python **3.8+**
* `pip` package manager

### Installation

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/ankitkumarbyte/placement-predictot-ml-practice-
cd placement-predictot-ml-practice-
```

#### 2️⃣ Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

#### 3️⃣ Install dependencies

```bash
pip install -r backend/requirements.txt
```

#### 4️⃣ Run the application

```bash
python run.py
```

#### 5️⃣ Open in browser

```
http://localhost:8080
```

---

## 📁 Project Structure

```
ml-placement-predictor/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── model.pkl           # Trained ML model
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML interface
│   ├── styles.css          # CSS styling
│   └── script.js           # Frontend JavaScript
├── placement copy.csv      # Training dataset
├── run.py                  # Main application runner
├── end_to_end_ml.ipynb     # ML pipeline notebook
└── README.md               # Project documentation
```

---

## 🧠 Machine Learning Pipeline

1. **Data Collection** – Placement dataset with student records
2. **Data Preprocessing** – Cleaning, scaling, feature selection
3. **Model Training** – Scikit-learn classifiers
4. **Model Evaluation** – Accuracy, precision, recall
5. **Model Deployment** – Flask API serving predictions
6. **Web Interface** – Frontend consuming ML API

### Model Details

* **Algorithm**: Logistic Regression / Random Forest
* **Features**: CGPA (0–10), IQ Score (50–200)
* **Target**: Placement (1 = Placed, 0 = Not Placed)
* **Accuracy**: ~85% (demo mode supported)

---

## 💻 API Endpoints

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| GET    | `/`                | Serve frontend UI         |
| POST   | `/api/predict`     | Make placement prediction |
| GET    | `/api/stats`       | Dataset statistics        |
| GET    | `/api/sample-data` | Sample student data       |

### Prediction Request

```json
{
  "cgpa": 7.5,
  "iq": 130
}
```

### Prediction Response

```json
{
  "success": true,
  "prediction": 1,
  "probability": 0.85,
  "message": "Placed",
  "fun_message": "🎯 Placement hogya! Jaa, jee le apni zindagi! 🥳",
  "cgpa": 7.5,
  "iq": 130,
  "confidence": 85
}
```

---

## 🎮 How to Use

1. **Enter Details**

   * Set CGPA (0–10)
   * Set IQ score (50–200)

2. **Click Predict**

   * Press **🔮 Predict My Placement**

3. **View Results**

   * Placement status with confidence
   * Fun Hindi message
   * Placement statistics

---

## 🔧 Development

### Run in Debug Mode

```bash
python run.py --debug
```

### Custom Port

```bash
python run.py --port=9999
```

### Train Your Own Model

1. Open `end_to_end_ml.ipynb`
2. Train & evaluate models
3. Save best model as `model.pkl`
4. Place it in `backend/`

---

## 🌐 Deployment

### Heroku

```bash
echo "web: python run.py" > Procfile
git push heroku main
```

### Railway

```bash
npm i -g @railway/cli
railway up
```

---

## 🐛 Troubleshooting

| Issue             | Solution                    |
| ----------------- | --------------------------- |
| Port in use       | Change port or use `--port` |
| Model not loading | Ensure `model.pkl` exists   |
| Module not found  | Install requirements        |
| Frontend issues   | Check browser console       |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a branch (`feature/awesome-feature`)
3. Commit changes
4. Push and open PR

### Ideas

* More ML models
* Better UI animations
* Auth & prediction history
* Advanced analytics

---

## 📊 Dataset Information

* **Records**: 100+ students
* **Features**: `cgpa`, `iq`
* **Target**: `placement`

| CGPA | IQ  | Placement |
| ---- | --- | --------- |
| 6.8  | 123 | 1         |
| 5.9  | 106 | 0         |
| 7.4  | 132 | 1         |
| 5.8  | 142 | 0         |

---

## 📝 License

This project is licensed under the **MIT License**.

---

⭐ If you like this project, give it a star on GitHub!
