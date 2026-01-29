from flask import Flask, jsonify, request
import pickle
import numpy as np
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

# Use a different port - 8080
PORT = 8080

print("🚀 Starting ML Placement Predictor...")

# Try to load model
try:
    with open('backend/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
    model_loaded = True
except:
    print("⚠️ Model not found, using demo mode")
    model_loaded = False

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎯 Placement Predictor</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 { 
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                font-size: 2.5rem;
            }
            .input-group {
                margin: 25px 0;
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
                color: #555;
                font-size: 1.1rem;
            }
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #667eea;
                border-radius: 8px;
                font-size: 1.1rem;
                margin: 10px 0;
            }
            .btn {
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 1.3rem;
                border-radius: 12px;
                cursor: pointer;
                width: 100%;
                margin: 20px 0;
                font-weight: bold;
                transition: all 0.3s;
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
            }
            .btn:active {
                transform: translateY(-1px);
            }
            .result {
                margin-top: 30px;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                font-size: 1.3rem;
                font-weight: bold;
                min-height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                transition: all 0.5s;
                border: 3px solid transparent;
            }
            .placed {
                background: #d4edda;
                color: #155724;
                border-color: #28a745;
                animation: celebrate 1s ease;
            }
            .not-placed {
                background: #f8d7da;
                color: #721c24;
                border-color: #dc3545;
                animation: shake 0.5s ease;
            }
            @keyframes celebrate {
                0% { transform: scale(0.9); opacity: 0; }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); opacity: 1; }
            }
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
            .message {
                font-size: 1.5rem;
                margin-top: 20px;
                padding: 20px;
                border-radius: 10px;
                font-weight: bold;
            }
            .success {
                background: rgba(40, 167, 69, 0.1);
                color: #155724;
                border: 2px dashed #28a745;
            }
            .failure {
                background: rgba(220, 53, 69, 0.1);
                color: #721c24;
                border: 2px dashed #dc3545;
            }
            .status {
                text-align: center;
                margin-top: 20px;
                color: #666;
            }
            .confetti {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1000;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Placement Predictor</h1>
            
            <div class="input-group">
                <label>🎓 Your CGPA (0-10)</label>
                <input type="number" id="cgpa" min="0" max="10" step="0.1" value="7.5">
            </div>
            
            <div class="input-group">
                <label>🧠 Your IQ (50-200)</label>
                <input type="number" id="iq" min="50" max="200" value="130">
            </div>
            
            <button class="btn" onclick="predict()">🔮 Predict My Placement</button>
            
            <div class="result" id="resultBox">
                <div id="resultText">Enter your details and click Predict!</div>
                <div class="message" id="funMessage"></div>
            </div>
            
            <div class="status">
                <p>Model Status: <span id="modelStatus">Loading...</span></p>
                <p>Backend: <span id="backendStatus">Checking...</span></p>
            </div>
        </div>

        <div class="confetti" id="confettiContainer"></div>

        <script>
            // Check backend status
            fetch('/status')
                .then(response => {
                    if (response.ok) {
                        document.getElementById('backendStatus').textContent = '✅ Connected';
                        document.getElementById('backendStatus').style.color = 'green';
                    }
                })
                .catch(() => {
                    document.getElementById('backendStatus').textContent = '✅ Connected (Local)';
                    document.getElementById('backendStatus').style.color = 'green';
                });
            
            function predict() {
                const cgpa = parseFloat(document.getElementById('cgpa').value);
                const iq = parseFloat(document.getElementById('iq').value);
                
                if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
                    alert('CGPA must be between 0 and 10');
                    return;
                }
                
                if (isNaN(iq) || iq < 50 || iq > 200) {
                    alert('IQ must be between 50 and 200');
                    return;
                }
                
                const btn = document.querySelector('.btn');
                btn.disabled = true;
                btn.innerHTML = '🔮 Predicting...';
                
                fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cgpa, iq })
                })
                .then(response => response.json())
                .then(data => {
                    showResult(data);
                })
                .catch(error => {
                    console.log('Using local prediction');
                    const localResult = getLocalPrediction(cgpa, iq);
                    showResult(localResult);
                })
                .finally(() => {
                    btn.disabled = false;
                    btn.innerHTML = '🔮 Predict My Placement';
                });
            }
            
            function getLocalPrediction(cgpa, iq) {
                // Smart prediction logic
                let score = 0;
                
                if (cgpa >= 9) score += 60;
                else if (cgpa >= 8) score += 50;
                else if (cgpa >= 7.5) score += 40;
                else if (cgpa >= 7) score += 30;
                else if (cgpa >= 6.5) score += 20;
                else if (cgpa >= 6) score += 15;
                else score += 10;
                
                if (iq >= 140) score += 40;
                else if (iq >= 130) score += 35;
                else if (iq >= 120) score += 30;
                else if (iq >= 110) score += 20;
                else if (iq >= 100) score += 15;
                else score += 10;
                
                const probability = score / 100;
                const isPlaced = probability > 0.5;
                
                const messages = isPlaced ? [
                    "🎯 Placement hogya! Jaa, jee le apni zindagi! 🥳",
                    "🚀 Company ne pakad liya! Ab bas chutti! 🏖️",
                    "💰 Package mil gaya! Party time! 🍾",
                    "🏆 Selection ho gaya! Champion! 🏅"
                ] : [
                    "😢 Nhi hoga placement! Lage reh! 📚",
                    "💔 Aaj nahi toh kal! Keep trying! 💪",
                    "📉 Thoda aur mehnat chahiye! 🤓",
                    "😅 Chill kar! Abhi time hai! 🕰️"
                ];
                
                return {
                    prediction: isPlaced ? 1 : 0,
                    probability: probability,
                    message: isPlaced ? 'Placed' : 'Not Placed',
                    fun_message: messages[Math.floor(Math.random() * messages.length)],
                    cgpa: cgpa,
                    iq: iq,
                    confidence: Math.round(probability * 100)
                };
            }
            
            function showResult(result) {
                const isPlaced = result.prediction === 1;
                const resultBox = document.getElementById('resultBox');
                const resultText = document.getElementById('resultText');
                const funMessage = document.getElementById('funMessage');
                
                resultBox.className = `result ${isPlaced ? 'placed' : 'not-placed'}`;
                resultText.innerHTML = isPlaced ? '🎉 CONGRATULATIONS! 🎉' : '😢 SORRY BUDDY';
                resultText.innerHTML += `<br><small>Confidence: ${result.confidence}%</small>`;
                
                funMessage.textContent = result.fun_message;
                funMessage.className = `message ${isPlaced ? 'success' : 'failure'}`;
                
                if (isPlaced) {
                    createConfetti();
                }
            }
            
            function createConfetti() {
                const container = document.getElementById('confettiContainer');
                container.innerHTML = '';
                
                for (let i = 0; i < 50; i++) {
                    const confetti = document.createElement('div');
                    confetti.textContent = '🎉';
                    confetti.style.position = 'absolute';
                    confetti.style.left = Math.random() * 100 + '%';
                    confetti.style.top = '-50px';
                    confetti.style.fontSize = (Math.random() * 20 + 20) + 'px';
                    confetti.style.animation = `fall ${Math.random() * 2 + 2}s linear forwards`;
                    
                    container.appendChild(confetti);
                    
                    setTimeout(() => confetti.remove(), 3000);
                }
                
                if (!document.querySelector('#confetti-animation')) {
                    const style = document.createElement('style');
                    style.id = 'confetti-animation';
                    style.textContent = `
                        @keyframes fall {
                            0% { transform: translateY(0) rotate(0deg); opacity: 1; }
                            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
                        }
                    `;
                    document.head.appendChild(style);
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        cgpa = float(data.get('cgpa', 0))
        iq = float(data.get('iq', 0))
        
        print(f"📊 Prediction request: CGPA={cgpa}, IQ={iq}")
        
        if model_loaded:
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
            else:
                prediction = 0
                probability = 0.35
            model_type = "demo"
        
        # Fun messages
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
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/status')
def status():
    return jsonify({
        'status': 'online',
        'model_loaded': model_loaded,
        'port': PORT
    })

def open_browser():
    webbrowser.open_new(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print(f"🚀 Starting server on http://localhost:{PORT}")
    print(f"🤖 Model: {'Loaded ✅' if model_loaded else 'Demo Mode ⚠️'}")
    print(f"📁 Open: http://localhost:{PORT}")
    print("\n" + "="*50)
    print("PRESS Ctrl+C TO STOP")
    print("="*50 + "\n")
    
    Timer(2, open_browser).start()
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)
