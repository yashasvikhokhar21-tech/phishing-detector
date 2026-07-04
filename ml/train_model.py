"""
Machine Learning Model Training Script
This script trains a Random Forest classifier for phishing detection
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import os

# Import feature extractor
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from features.url_features import URLFeatureExtractor


class PhishingModelTrainer:
    """Train and evaluate phishing detection model"""
    
    def __init__(self, test_size=0.2, random_state=42):
        """
        Initialize the trainer
        
        Args:
            test_size (float): Proportion of data for testing
            random_state (int): Random seed for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.extractor = URLFeatureExtractor()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_dataset(self, csv_path='datasets/phishing.csv', max_samples=None):
        """Load dataset from CSV file and extract features"""
        print(f"Loading dataset from {csv_path}...")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"Loaded {len(df)} URLs from dataset")
            print(df.head(10))
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset file not found: {csv_path}")
        except Exception as e:
            raise Exception(f"Error loading dataset: {e}")
        
        # Check required columns
        if 'url' not in df.columns or 'label' not in df.columns:
            raise ValueError("CSV must contain 'url' and 'label' columns")
        
        # Limit dataset size if specified
        if max_samples and len(df) > max_samples:
            df = df.sample(n=max_samples, random_state=42)
            print(f"Limited dataset to {max_samples} samples")
        
        X = []
        y = []
        invalid_urls = 0
        
        print("Extracting features from URLs...")
        for idx, row in df.iterrows():
            if (idx + 1) % 1000 == 0:
                print(f"Processed {idx + 1}/{len(df)} URLs...")
                
            url = str(row['url']).strip()
            label = 0 if int(row['label']) == 1 else 1
            
            try:
                # Extract features using URLFeatureExtractor
                features = self.extractor.extract_features(url)
                X.append(features)
                y.append(label)
            except Exception as e:
                # Handle invalid URLs safely
                invalid_urls += 1
                if invalid_urls <= 5:  # Only show first 5 errors
                    print(f"Warning: Skipping invalid URL at row {idx}: {url[:50]}... (Error: {e})")
                continue
        
        if invalid_urls > 5:
            print(f"... and {invalid_urls - 5} more invalid URLs skipped")
        elif invalid_urls > 0:
            print(f"Skipped {invalid_urls} invalid URLs")
        
        if len(X) == 0:
            raise ValueError("No valid URLs found in dataset")
        
        print(f"Successfully processed {len(X)} URLs")
        print(f"Legitimate URLs: {sum(1 for label in y if label == 0)}")
        print(f"Phishing URLs: {sum(1 for label in y if label == 1)}")
        
        return np.array(X), np.array(y)
    
    def train(self, csv_path='datasets/phishing.csv', max_samples=None):
        """Train the model using dataset from CSV"""
        print("Loading dataset and extracting features...")
        X, y = self.load_dataset(csv_path, max_samples)
        
        print(f"Dataset size: {len(X)} URLs")
        print(f"Legitimate URLs: {sum(y == 0)}")
        print(f"Phishing URLs: {sum(y == 1)}")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        # Train model
        print("\nTraining Random Forest model...")
        self.model.fit(self.X_train, self.y_train)
        print("Training completed!")
    
    def evaluate(self):
        """Evaluate the model"""
        print("\n" + "="*50)
        print("MODEL EVALUATION")
        print("="*50)
        
        # Predictions
        y_pred_train = self.model.predict(self.X_train)
        y_pred_test = self.model.predict(self.X_test)
        
        # Metrics
        print("\nTRAINING SET METRICS:")
        print(f"Accuracy:  {accuracy_score(self.y_train, y_pred_train):.4f}")
        print(f"Precision: {precision_score(self.y_train, y_pred_train, zero_division=0):.4f}")
        print(f"Recall:    {recall_score(self.y_train, y_pred_train, zero_division=0):.4f}")
        print(f"F1-Score:  {f1_score(self.y_train, y_pred_train, zero_division=0):.4f}")
        
        print("\nTEST SET METRICS:")
        print(f"Accuracy:  {accuracy_score(self.y_test, y_pred_test):.4f}")
        print(f"Precision: {precision_score(self.y_test, y_pred_test, zero_division=0):.4f}")
        print(f"Recall:    {recall_score(self.y_test, y_pred_test, zero_division=0):.4f}")
        print(f"F1-Score:  {f1_score(self.y_test, y_pred_test, zero_division=0):.4f}")
        
        print("\nCONFUSION MATRIX (Test Set):")
        cm = confusion_matrix(self.y_test, y_pred_test)
        print(cm)
        print("="*50)
    
    def save_model(self, model_path='models/phishing_model.pkl', scaler_path='models/scaler.pkl'):
        """Save trained model and scaler"""
        os.makedirs(os.path.dirname(model_path) or '.', exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"\nModel saved to {model_path}")
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to {scaler_path}")
    
    def feature_importance(self):
        """Print feature importance"""
        print("\n" + "="*50)
        print("FEATURE IMPORTANCE")
        print("="*50)
        
        feature_names = [
            "URL Length",
            "Domain Length", 
            "Special Characters",
            "HTTPS Protocol",
            "Hyphens Count",
            "Dots Count",
            "Numeric Characters",
            "@ Symbol Present"
        ]
        
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        for i, idx in enumerate(indices, 1):
            print(f"{i}. {feature_names[idx]}: {importances[idx]:.4f}")
        print("="*50)


def main():
    """Main function to train and evaluate model"""
    trainer = PhishingModelTrainer()
    trainer.train('datasets/phishing.csv')  # Full dataset
    trainer.evaluate()
    trainer.feature_importance()
    trainer.save_model()
    print("\n✓ Model training completed successfully!")


if __name__ == "__main__":
    main()
