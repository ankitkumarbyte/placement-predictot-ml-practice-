from flask import Flask, jsonify, request, send_from_directory
import pickle
import numpy as np
import os
import webbrowser
from threading import Timer
import pandas as pd

app = Flask(__name__, static_folder='frontend')

# Use port 8080 to avoid conflicts
PORT = 8080

print("🚀 Starting ML Placement Predictor...")

# Try to load model
try:
    with open('backend/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully from backend/model.pkl")
except FileNotFoundError:
    print("⚠️ Model file not found, using demo mode")
    model = None
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None

# Try to load dataset
try:
    df = pd.read_csv('placement.csv')
    print(f"✅ Dataset loaded: {len(df)} records")
    dataset_loaded = True
except:
    print("⚠️ Dataset not found, using sample data")
    dataset_loaded = False

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('frontend', path)

# API Routes
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        cgpa = float(data.get('cgpa', 0))
        iq = float(data.get('iq', 0))
        
        print(f"📊 Prediction request: CGPA={cgpa}, IQ={iq}")
        
        if model:
            # Use actual model
            prediction = model.predict([[cgpa, iq]])[0]
            probability = float(model.predict_proba([[cgpa, iq]])[0][prediction])
            model_type = "real"
        else:
            # Smart demo logic
            if cgpa > 7.0 and iq > 120:
                prediction = 1
                probability = 0.85
            elif cgpa > 6.5 and iq > 110:
                prediction = 1
                probability = 0.65
            elif cgpa > 6.0 and iq > 100:
                prediction = 1
                probability = 0.45
            else:
                prediction = 0
                probability = 0.25
            model_type = "demo"
        
        # Determine fun message
        if prediction == 1:
            messages = [
                "🎯 Placement hogya! Jaa, jee le apni zindagi! 🥳",
                "🚀 Company ne pakad liya! Ab bas chutti! 🏖️",
                "💰 Package mil gaya! Party time! 🍾",
                "🏆 Selection ho gaya! Champion! 🏅",
                "🎊 Congratulations! Ab trip plan kar! ✈️"
            ]
            fun_message = messages[np.random.randint(0, len(messages))]
        else:
            messages = [
                "😢 Nhi hoga placement! Lage reh! 📚",
                "💔 Aaj nahi toh kal! Keep trying! 💪",
                "📉 Thoda aur mehnat chahiye! 🤓",
                "😅 Chill kar! Abhi time hai! 🕰️",
                "🤔 CGPA improve kar, IQ badha! Next time pakka! ✨"
            ]
            fun_message = messages[np.random.randint(0, len(messages))]
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'probability': probability,
            'message': 'Placed' if prediction == 1 else 'Not Placed',
            'fun_message': fun_message,
            'cgpa': cgpa,
            'iq': iq,
            'model_type': model_type,
            'confidence': round(probability * 100)
        })
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/stats', methods=['GET'])
def stats():
    try:
        if dataset_loaded:
            total = len(df)
            placed = df['placement'].sum()
            avg_cgpa = df['cgpa'].mean()
            avg_iq = df['iq'].mean()
            
            return jsonify({
                'success': True,
                'total_students': int(total),
                'placed_students': int(placed),
                'placement_rate': round((placed/total)*100, 2),
                'avg_cgpa': round(avg_cgpa, 2),
                'avg_iq': round(avg_iq, 2),
                'data_source': 'placement.csv'
            })
    except:
        pass
    
    # Default stats
    return jsonify({
        'success': True,
        'total_students': 100,
        'placed_students': 65,
        'placement_rate': 65.0,
        'avg_cgpa': 7.2,
        'avg_iq': 128.5,
        'data_source': 'demo'
    })

@app.route('/api/sample-data', methods=['GET'])
def sample_data():
    # Return sample data for frontend display
    data = [
        {'name': 'Rahul', 'cgpa': 6.8, 'iq': 123, 'placement': 1},
        {'name': 'Priya', 'cgpa': 5.9, 'iq': 106, 'placement': 0},
        {'name': 'Amit', 'cgpa': 5.3, 'iq': 121, 'placement': 0},
        {'name': 'Sneha', 'cgpa': 7.4, 'iq': 132, 'placement': 1},
        {'name': 'Vikram', 'cgpa': 5.8, 'iq': 142, 'placement': 0},
        {'name': 'Neha', 'cgpa': 8.1, 'iq': 135, 'placement': 1},
        {'name': 'Raj', 'cgpa': 7.2, 'iq': 128, 'placement': 1},
        {'name': 'Anjali', 'cgpa': 6.5, 'iq': 118, 'placement': 1},
        {'name': 'Karan', 'cgpa': 5.5, 'iq': 110, 'placement': 0},
        {'name': 'Pooja', 'cgpa': 7.8, 'iq': 140, 'placement': 1}
    ]
    return jsonify(data)

def open_browser():
    """Open browser automatically"""
    webbrowser.open_new(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print(f"🌐 Server will start on http://localhost:{PORT}")
    print(f"📁 Serving frontend from: frontend/")
    print(f"🤖 Model status: {'Loaded ✅' if model else 'Demo Mode ⚠️'}")
    print(f"📊 Dataset status: {'Loaded ✅' if dataset_loaded else 'Demo Mode ⚠️'}")
    print("\n" + "="*50)
    print("PRESS Ctrl+C TO STOP THE SERVER")
    print("="*50 + "\n")
    
    # Open browser after 2 seconds
    Timer(2, open_browser).start()
    
    # Run the app
    app.run(host='0.0.0.0', port=PORT, debug=False)
