class PlacementPredictor {
    constructor() {
        this.API_BASE = 'http://localhost:5001/api';
        this.predictionsHistory = [];
        this.init();
    }
    
    init() {
        this.cacheElements();
        this.setupEventListeners();
        this.checkBackend();
        this.loadSampleData();
        this.initChart();
        this.loadStats();
    }
    
    cacheElements() {
        // Input elements
        this.cgpaSlider = document.getElementById('cgpaSlider');
        this.cgpaInput = document.getElementById('cgpaInput');
        this.cgpaValue = document.getElementById('cgpaValue');
        this.iqSlider = document.getElementById('iqSlider');
        this.iqInput = document.getElementById('iqInput');
        this.iqValue = document.getElementById('iqValue');
        this.predictBtn = document.getElementById('predictBtn');
        
        // Result elements
        this.resultBox = document.getElementById('resultBox');
        this.resultIcon = document.getElementById('resultIcon');
        this.resultText = document.getElementById('resultText');
        this.resultDetails = document.getElementById('resultDetails');
        this.funMessage = document.getElementById('funMessage');
        
        // Status elements
        this.backendStatus = document.getElementById('backendStatus');
        this.historyList = document.getElementById('historyList');
        this.tableBody = document.getElementById('tableBody');
        this.confettiContainer = document.getElementById('confettiContainer');
        
        // Stats elements
        this.totalStudentsEl = document.getElementById('totalStudents');
        this.placedStudentsEl = document.getElementById('placedStudents');
        this.avgCgpaEl = document.getElementById('avgCgpa');
        this.avgIqEl = document.getElementById('avgIq');
    }
    
    setupEventListeners() {
        // CGPA sync
        this.cgpaSlider.addEventListener('input', () => {
            this.cgpaInput.value = this.cgpaSlider.value;
            this.cgpaValue.textContent = this.cgpaSlider.value;
        });
        
        this.cgpaInput.addEventListener('input', () => {
            this.cgpaSlider.value = this.cgpaInput.value;
            this.cgpaValue.textContent = this.cgpaInput.value;
        });
        
        // IQ sync
        this.iqSlider.addEventListener('input', () => {
            this.iqInput.value = this.iqSlider.value;
            this.iqValue.textContent = this.iqSlider.value;
        });
        
        this.iqInput.addEventListener('input', () => {
            this.iqSlider.value = this.iqInput.value;
            this.iqValue.textContent = this.iqInput.value;
        });
        
        // Predict button
        this.predictBtn.addEventListener('click', () => this.predict());
    }
    
    async checkBackend() {
        try {
            const response = await fetch(`${this.API_BASE}/stats`);
            if (response.ok) {
                this.backendStatus.textContent = '✅ Connected';
                this.backendStatus.style.color = 'green';
            } else {
                throw new Error('Backend not responding');
            }
        } catch (error) {
            this.backendStatus.textContent = '⚠️ Offline (Demo Mode)';
            this.backendStatus.style.color = 'orange';
        }
    }
    
    async loadStats() {
        try {
            const response = await fetch(`${this.API_BASE}/stats`);
            const data = await response.json();
            
            if (data.success) {
                this.totalStudentsEl.textContent = data.total_students;
                this.placedStudentsEl.textContent = data.placed_students;
                this.avgCgpaEl.textContent = data.avg_cgpa;
                this.avgIqEl.textContent = data.avg_iq;
            }
        } catch (error) {
            console.log('Using default stats');
        }
    }
    
    loadSampleData() {
        const sampleData = [
            { name: "Rahul", cgpa: 6.8, iq: 123, placement: 1 },
            { name: "Priya", cgpa: 5.9, iq: 106, placement: 0 },
            { name: "Amit", cgpa: 5.3, iq: 121, placement: 0 },
            { name: "Sneha", cgpa: 7.4, iq: 132, placement: 1 },
            { name: "Vikram", cgpa: 5.8, iq: 142, placement: 0 },
            { name: "Neha", cgpa: 8.1, iq: 135, placement: 1 },
            { name: "Raj", cgpa: 7.2, iq: 128, placement: 1 },
            { name: "Anjali", cgpa: 6.5, iq: 118, placement: 1 },
            { name: "Karan", cgpa: 5.5, iq: 110, placement: 0 },
            { name: "Pooja", cgpa: 7.8, iq: 140, placement: 1 }
        ];
        
        this.tableBody.innerHTML = '';
        sampleData.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.name}</td>
                <td>${student.cgpa.toFixed(1)}</td>
                <td>${student.iq}</td>
                <td>
                    <span style="
                        padding: 5px 10px;
                        border-radius: 15px;
                        font-weight: bold;
                        background: ${student.placement ? '#d4edda' : '#f8d7da'};
                        color: ${student.placement ? '#155724' : '#721c24'};
                    ">
                        ${student.placement ? '✅ Placed' : '❌ Not Placed'}
                    </span>
                </td>
            `;
            this.tableBody.appendChild(row);
        });
    }
    
    initChart() {
        const ctx = document.getElementById('placementChart').getContext('2d');
        const data = [
            { name: "Rahul", cgpa: 6.8, iq: 123, placement: 1 },
            { name: "Priya", cgpa: 5.9, iq: 106, placement: 0 },
            { name: "Amit", cgpa: 5.3, iq: 121, placement: 0 },
            { name: "Sneha", cgpa: 7.4, iq: 132, placement: 1 },
            { name: "Vikram", cgpa: 5.8, iq: 142, placement: 0 },
            { name: "Neha", cgpa: 8.1, iq: 135, placement: 1 },
            { name: "Raj", cgpa: 7.2, iq: 128, placement: 1 },
            { name: "Anjali", cgpa: 6.5, iq: 118, placement: 1 },
            { name: "Karan", cgpa: 5.5, iq: 110, placement: 0 },
            { name: "Pooja", cgpa: 7.8, iq: 140, placement: 1 }
        ];
        
        const placed = data.filter(s => s.placement === 1).length;
        const notPlaced = data.length - placed;
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Placed 🎉', 'Not Placed 😢'],
                datasets: [{
                    data: [placed, notPlaced],
                    backgroundColor: ['#28a745', '#dc3545'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    async predict() {
        const cgpa = parseFloat(this.cgpaInput.value);
        const iq = parseFloat(this.iqInput.value);
        
        // Validation
        if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
            this.showNotification('CGPA must be between 0 and 10', 'error');
            return;
        }
        
        if (isNaN(iq) || iq < 50 || iq > 200) {
            this.showNotification('IQ must be between 50 and 200', 'error');
            return;
        }
        
        // Show loading
        this.predictBtn.disabled = true;
        this.predictBtn.innerHTML = '<i class="emoji">⏳</i> Predicting...';
        
        try {
            const response = await fetch(`${this.API_BASE}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cgpa, iq })
            });
            
            let result;
            if (response.ok) {
                result = await response.json();
            } else {
                // Fallback to local prediction
                result = this.getLocalPrediction(cgpa, iq);
            }
            
            this.displayResult(result);
            this.addToHistory(result, cgpa, iq);
            
        } catch (error) {
            // Local fallback
            const result = this.getLocalPrediction(cgpa, iq);
            this.displayResult(result);
            this.addToHistory(result, cgpa, iq);
        } finally {
            this.predictBtn.disabled = false;
            this.predictBtn.innerHTML = '<i class="emoji">🔮</i> PREDICT MY PLACEMENT';
        }
    }
    
    getLocalPrediction(cgpa, iq) {
        // Smart prediction based on typical patterns
        let score = 0;
        
        // CGPA contributes 60%
        if (cgpa >= 9) score += 60;
        else if (cgpa >= 8) score += 50;
        else if (cgpa >= 7.5) score += 40;
        else if (cgpa >= 7) score += 30;
        else if (cgpa >= 6.5) score += 20;
        else if (cgpa >= 6) score += 10;
        else score += 5;
        
        // IQ contributes 40%
        if (iq >= 140) score += 40;
        else if (iq >= 130) score += 35;
        else if (iq >= 120) score += 30;
        else if (iq >= 110) score += 20;
        else if (iq >= 100) score += 10;
        else score += 5;
        
        const probability = score / 100;
        const isPlaced = probability > 0.5;
        
        return {
            prediction: isPlaced ? 1 : 0,
            probability: probability,
            message: isPlaced ? 'Placed' : 'Not Placed',
            cgpa: cgpa,
            iq: iq
        };
    }
    
    displayResult(result) {
        const isPlaced = result.prediction === 1;
        const confidence = Math.round(result.probability * 100);
        
        // Update UI
        this.resultBox.className = `result-box ${isPlaced ? 'placed' : 'not-placed'}`;
        this.resultIcon.textContent = isPlaced ? '🎉' : '😢';
        this.resultText.textContent = isPlaced ? 'CONGRATULATIONS! 🎊' : 'SORRY BUDDY 😔';
        this.resultDetails.textContent = `CGPA: ${result.cgpa.toFixed(1)} | IQ: ${result.iq} | Confidence: ${confidence}%`;
        
        // Fun messages
        if (isPlaced) {
            const messages = [
                "🎯 Placement hogya! Jaa, jee le apni zindagi! 🥳",
                "🚀 Company ne pakad liya! Ab bas chutti! 🏖️",
                "💰 Package mil gaya! Party time! 🍾",
                "🏆 Selection ho gaya! Champion! 🏅",
                "🎊 Congratulations! Ab trip plan kar! ✈️"
            ];
            const randomMsg = messages[Math.floor(Math.random() * messages.length)];
            this.funMessage.textContent = randomMsg;
            this.funMessage.className = 'fun-message placed';
            
            // Confetti
            this.createConfetti();
        } else {
            const messages = [
                "😢 Nhi hoga placement! Lage reh! 📚",
                "💔 Aaj nahi toh kal! Keep trying! 💪",
                "📉 Thoda aur mehnat chahiye! 🤓",
                "😅 Chill kar! Abhi time hai! 🕰️",
                "🤔 CGPA improve kar, IQ badha! Next time pakka! ✨"
            ];
            const randomMsg = messages[Math.floor(Math.random() * messages.length)];
            this.funMessage.textContent = randomMsg;
            this.funMessage.className = 'fun-message not-placed';
        }
    }
    
    addToHistory(result, cgpa, iq) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <div>
                <strong>CGPA: ${cgpa.toFixed(1)} | IQ: ${iq}</strong><br>
                <span style="color: ${result.prediction ? 'green' : 'red'};">
                    ${result.prediction ? '✅ Placed' : '❌ Not Placed'}
                </span>
            </div>
            <div style="color: #666;">
                ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </div>
        `;
        
        this.historyList.prepend(historyItem);
        
        // Keep only 5 items
        if (this.historyList.children.length > 5) {
            this.historyList.removeChild(this.historyList.lastChild);
        }
    }
    
    createConfetti() {
        this.confettiContainer.innerHTML = '';
        
        const colors = ['#ff6b6b', '#ffd166', '#06d6a0', '#118ab2', '#ef476f'];
        
        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti-piece';
            confetti.textContent = '🎉';
            
            // Random position
            confetti.style.left = `${Math.random() * 100}%`;
            
            // Random color
            confetti.style.color = colors[Math.floor(Math.random() * colors.length)];
            
            // Random animation
            const duration = Math.random() * 3 + 2;
            const delay = Math.random() * 1;
            
            confetti.style.animation = `
                confettiFall ${duration}s ease-in ${delay}s forwards
            `;
            
            this.confettiContainer.appendChild(confetti);
        }
        
        // Add animation styles
        if (!document.querySelector('#confetti-animation')) {
            const style = document.createElement('style');
            style.id = 'confetti-animation';
            style.textContent = `
                @keyframes confettiFall {
                    0% {
                        transform: translateY(-100px) rotate(0deg);
                        opacity: 1;
                    }
                    100% {
                        transform: translateY(100vh) rotate(360deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Clean up
        setTimeout(() => {
            this.confettiContainer.innerHTML = '';
        }, 5000);
    }
    
    showNotification(message, type) {
        // Create notification
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#dc3545' : '#28a745'};
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
        
        // Add animation styles
        if (!document.querySelector('#notification-animations')) {
            const style = document.createElement('style');
            style.id = 'notification-animations';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.predictor = new PlacementPredictor();
});