from flask import Flask, jsonify, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load your model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
except:
    print("⚠️ Model not found, using demo mode")
    model = None

@app.route('/')
def home():
    return jsonify({"message": "Placement Predictor API", "status": "active"})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        cgpa = float(data['cgpa'])
        iq = float(data['iq'])
        
        if model:
            # Use your actual model
            prediction = model.predict([[cgpa, iq]])[0]
            probability = float(model.predict_proba([[cgpa, iq]])[0][prediction])
        else:
            # Demo logic
            score = (cgpa * 0.6) + (iq * 0.004)
            prediction = 1 if score > 5.0 else 0
            probability = min(score / 10, 0.99)
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'probability': probability,
            'message': 'Placed' if prediction == 1 else 'Not Placed',
            'cgpa': cgpa,
            'iq': iq
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify({
        'total_students': 100,
        'placed_students': 65,
        'placement_rate': 65.0,
        'avg_cgpa': 7.2,
        'avg_iq': 128.5
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
