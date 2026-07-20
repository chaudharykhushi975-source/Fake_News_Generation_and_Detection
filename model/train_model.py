import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import nltk
from nltk.corpus import stopwords
import re

# Download stopwords
nltk.download('stopwords')

class FakeNewsDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words=stopwords.words('english'),
            ngram_range=(1, 2)
        )
        self.model = LogisticRegression(max_iter=1000)
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def train(self, data_path):
        """Train the model on dataset"""
        # Load dataset (assuming CSV with 'text' and 'label' columns)
        df = pd.read_csv(data_path)
        
        # Preprocess texts
        df['processed_text'] = df['text'].apply(self.preprocess_text)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            df['processed_text'], 
            df['label'], 
            test_size=0.2, 
            random_state=42
        )
        
        # Vectorize text
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)
        
        # Train model
        self.model.fit(X_train_vectorized, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_vectorized)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model and vectorizer
        joblib.dump(self.model, 'model/fake_news_model.pkl')
        joblib.dump(self.vectorizer, 'model/vectorizer.pkl')
        
        return accuracy
    
    def predict(self, text):
        """Predict if news is fake or real"""
        processed_text = self.preprocess_text(text)
        vectorized_text = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(vectorized_text)
        probability = self.model.predict_proba(vectorized_text)
        
        return {
            'prediction': 'Fake News' if prediction[0] == 1 else 'Real News',
            'confidence': max(probability[0]) * 100
        }

if __name__ == "__main__":
    # Create sample dataset if not exists
    import os
    if not os.path.exists('dataset/fake_news_data.csv'):
        print("Please add your dataset to dataset/fake_news_data.csv")
        print("Expected format: text,label (0 for real, 1 for fake)")
    else:
        detector = FakeNewsDetector()
        detector.train('dataset/fake_news_data.csv')