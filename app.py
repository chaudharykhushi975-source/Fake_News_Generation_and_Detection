from flask import Flask, render_template, request, jsonify
import joblib
import os
from utils.preprocess import preprocess_text
from utils.generator import FakeNewsGenerator
import nltk

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load model
try:
    model = joblib.load('model/fake_news_model.pkl')
    vectorizer = joblib.load('model/vectorizer.pkl')
    model_loaded = True
except:
    model_loaded = False
    print("Model not found. Please train the model first.")

# Initialize generator
generator = FakeNewsGenerator()

def predict_news(text):
    """Predict if news is fake or real"""
    if not model_loaded:
        return {'prediction': 'Model not loaded', 'confidence': 0}
    
    processed = preprocess_text(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)
    probability = model.predict_proba(vectorized)
    
    return {
        'prediction': 'Fake News' if prediction[0] == 1 else 'Real News',
        'confidence': round(max(probability[0]) * 100, 2),
        'is_fake': bool(prediction[0])
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Endpoint for news detection"""
    news_text = request.form.get('news_text', '')
    if not news_text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = predict_news(news_text)
    return jsonify(result)

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint for generating fake news"""
    topic = request.form.get('topic', None)
    generated = generator.generate_fake_news(topic)
    return jsonify(generated)

@app.route('/modify', methods=['POST'])
def modify():
    """Endpoint for modifying real news to fake"""
    real_text = request.form.get('real_text', '')
    if not real_text:
        return jsonify({'error': 'No text provided'}), 400
    
    modified = generator.modify_real_news(real_text)
    return jsonify({'modified_text': modified})

@app.route('/batch_detect', methods=['POST'])
def batch_detect():
    """Endpoint for batch detection"""
    texts = request.json.get('texts', [])
    if not texts:
        return jsonify({'error': 'No texts provided'}), 400
    
    results = []
    for text in texts:
        result = predict_news(text)
        results.append({
            'text': text[:100] + '...' if len(text) > 100 else text,
            'prediction': result['prediction'],
            'confidence': result['confidence']
        })
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)