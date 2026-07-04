# 🎓 Learning & Development Guide

A guide to understand and extend the Phishing Detector system.

## 📚 Code Structure

### Layer 1: Feature Extraction
**File**: `features/url_features.py`

```python
URLFeatureExtractor class:
├── extract_features(url) → [8 features]
├── _get_url_length_feature()
├── _get_dots_count()
├── _get_hyphens_in_domain()
├── _get_at_symbol_feature()
├── _get_protocol_feature()
├── _get_domain_length()
├── _get_numeric_ratio()
└── _get_special_chars_count()
```

**Purpose**: Convert any URL string into 8 numerical features
**Input**: URL string (e.g., "https://google.com")
**Output**: List of 8 numbers (e.g., [26, 1, 0, 0, 1, 10, 0, 5])

**Example Usage**:
```python
from features.url_features import URLFeatureExtractor
extractor = URLFeatureExtractor()
features = extractor.extract_features("https://google.com")
print(features)  # [26, 1, 0, 0, 1, 10, 0.023, 5]
```

---

### Layer 2: Machine Learning Model
**File**: `ml/train_model.py`

```python
PhishingModelTrainer class:
├── __init__()
├── create_sample_dataset() → (X, y)
├── train()
│   ├── Split data (80% train, 20% test)
│   ├── Scale features (StandardScaler)
│   └── Train model (RandomForest)
├── evaluate() → metrics
├── save_model() → pkl files
└── feature_importance() → importance scores
```

**Purpose**: Train a machine learning classifier

**Data Flow**:
```
Sample URLs (24)
    ↓
Extract Features (8 per URL)
    ↓
Create X, y arrays
    ↓
Train/Test Split
    ↓
Scale Features
    ↓
Train Random Forest
    ↓
Evaluate & Save
```

**Example Usage**:
```python
from ml.train_model import PhishingModelTrainer
trainer = PhishingModelTrainer()
trainer.train()
trainer.evaluate()
trainer.save_model('models/phishing_model.pkl', 'models/scaler.pkl')
```

---

### Layer 3: Flask Web Application
**File**: `app/app.py`

```python
Flask Routes:
├── GET  / → index.html
├── POST /predict → single prediction
├── POST /batch-predict → multiple predictions
└── GET  /health → health check

Helper Functions:
├── load_model() → loads pkl files
└── predict_phishing(url) → prediction dict
```

**Purpose**: Web interface and API endpoints

**Request-Response Flow**:
```
1. User enters URL (Browser)
   ↓
2. POST /predict (AJAX)
   ↓
3. Flask endpoint receives JSON
   ↓
4. Extract features from URL
   ↓
5. Scale features
   ↓
6. Model prediction
   ↓
7. Return JSON response
   ↓
8. JavaScript displays results
   ↓
9. User sees Phishing/Legitimate status
```

**Example Usage**:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

---

### Layer 4: Frontend
**File**: `templates/index.html`, `static/style.css`, `static/script.js`

```javascript
JavaScript Functions:
├── checkUrl() → single URL check
├── checkBatch() → multiple URLs
├── isValidUrl(url) → validation
├── displayResult(data) → show results
├── displayBatchResults(data) → show batch results
└── escapeHtml(text) → security

CSS Classes:
├── .card → content containers
├── .btn-primary → buttons
├── .result-container → results
├── .alert → notifications
└── Responsive grid layout
```

**Purpose**: User interface and interaction

---

## 🔄 Complete Data Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. USER INTERACTION (Browser)                           │
│    User enters "https://google.com"                     │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 2. VALIDATION (script.js)                               │
│    • Check if URL not empty                             │
│    • Check valid URL format                             │
│    • Add https:// if missing                            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 3. API REQUEST (fetch)                                  │
│    POST /predict                                        │
│    {"url": "https://google.com"}                        │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 4. FEATURE EXTRACTION (url_features.py)                │
│    Extract 8 features from URL:                         │
│    [26, 1, 0, 0, 1, 10, 0.023, 5]                      │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 5. FEATURE SCALING (StandardScaler)                     │
│    Normalize features to mean=0, std=1                  │
│    [-0.5, 0.2, -0.3, -0.1, 0.8, 0.1, -0.6, 0.4]       │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 6. MODEL PREDICTION (RandomForest)                      │
│    100 decision trees vote                              │
│    Output class: 0 (Legitimate)                         │
│    Confidence: 0.95 (95%)                               │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 7. RESPONSE (JSON)                                      │
│    {                                                    │
│      "url": "https://google.com",                       │
│      "is_phishing": false,                              │
│      "confidence": 0.95,                                │
│      "features": {...}                                  │
│    }                                                    │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│ 8. DISPLAY RESULTS (Browser)                            │
│    Show ✓ Legitimate with confidence and features       │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Extending the System

### Add a New Feature

1. **Edit `features/url_features.py`**:
```python
def _get_new_feature(self, url):
    """New feature description"""
    # Extract feature from URL
    return feature_value

# Add to extract_features() method:
features.append(self._get_new_feature(url))
# Make it the 9th feature (index 8)
```

2. **Retrain model**:
```bash
python ml/train_model.py
```

3. **Update documentation** in README.md

---

### Change Machine Learning Algorithm

1. **Edit `ml/train_model.py`**:
```python
# Instead of RandomForestClassifier:
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC

# In PhishingModelTrainer.__init__():
self.model = GradientBoostingClassifier(n_estimators=100)
# or
self.model = SVC(kernel='rbf', probability=True)
```

2. **Retrain**:
```bash
python ml/train_model.py
```

3. **Compare metrics** and choose best performer

---

### Add Custom CSS Theme

**Edit `static/style.css`**:
```css
:root {
    --primary-color: #ff6b6b;      /* Change colors */
    --success-color: #51cf66;
    --warning-color: #ffd43b;
    --danger-color: #ff6b6b;
}

/* Add custom styles */
.custom-class {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 8px;
}
```

---

### Add Database Integration

1. **Install SQLAlchemy**:
```bash
pip install flask-sqlalchemy
```

2. **Create models**:
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class URLAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    is_phishing = db.Column(db.Boolean)
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

3. **Save predictions** to database

---

## 📊 Testing Strategies

### Unit Test Example
```python
# test_features.py
from features.url_features import URLFeatureExtractor

def test_url_length_feature():
    extractor = URLFeatureExtractor()
    url = "https://google.com"
    features = extractor.extract_features(url)
    assert features[0] == len(url)  # First feature is length
    print("✓ URL length test passed")

def test_phishing_detection():
    assert extractor._get_hyphens_in_domain("https://legit-bank.com") == 1
    assert extractor._get_at_symbol_feature("https://google.com@fake.com") == 1
    print("✓ Phishing detection test passed")

if __name__ == "__main__":
    test_url_length_feature()
    test_phishing_detection()
```

---

## 🚀 Performance Optimization

### 1. Caching Results
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def predict_phishing(url):
    # ... prediction logic
    return result
```

### 2. Batch Processing
```python
# Already implemented in /batch-predict endpoint
# Process multiple URLs in one request
```

### 3. Model Optimization
```python
# Use simpler model structure
self.model = RandomForestClassifier(
    n_estimators=50,      # Fewer trees
    max_depth=5,          # Shallower trees
    n_jobs=-1             # Use all processors
)
```

### 4. Async Operations
```python
from flask import Flask
from celery import Celery

# Run heavy operations asynchronously
@app.route('/analyze-batch-async')
def analyze_batch_async():
    task = process_urls_async.delay(urls)
    return {'task_id': task.id}
```

---

## 🐛 Debugging Tips

### 1. Print Feature Values
```python
extractor = URLFeatureExtractor()
features = extractor.extract_features(url)
extractor.print_features(url, features)  # Built-in method
```

### 2. Check Model Loaded
```python
if model is None:
    print("Model not loaded!")
else:
    print(f"Model: {type(model).__name__}")
    print(f"Trees: {model.n_estimators}")
```

### 3. Debug API Requests
```python
import json
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print(f"Received: {json.dumps(data, indent=2)}")
    # ... rest of code
```

### 4. Check Feature Scaling
```python
scaler_train = scaler.fit_transform(X_train)
print(f"Mean: {scaler_train.mean(axis=0)}")
print(f"Std: {scaler_train.std(axis=0)}")
```

---

## 📚 Learning Path

### Beginner Level
1. Run SETUP_GUIDE.md
2. Try example.py
3. Read url_features.py comments
4. Check what each feature means

### Intermediate Level
1. Understand RandomForest algorithm
2. Modify training data
3. Add new feature
4. Retrain and compare

### Advanced Level
1. Try different ML algorithms
2. Implement database logging
3. Deploy to cloud
4. Build browser extension

---

## 🔗 Project Dependencies

### Core Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| scikit-learn | 1.3.0 | ML library |
| pandas | 2.0.3 | Data manipulation |
| numpy | 1.24.3 | Numerical computing |
| Werkzeug | 2.3.7 | WSGI utilities |

### Optional (for enhancement)

- flask-cors: Enable CORS
- flask-sqlalchemy: Database ORM
- celery: Async tasks
- gunicorn: Production server
- docker: Containerization
- pytest: Testing framework

---

## 🎯 Common Modifications

### Change model port
**File**: `app/app.py`
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Changed from 5000
```

### Change batch size limit
**File**: `app/app.py`
```python
urls = data.get('urls', [])
if urls:
    results = []
    for url in urls[:50]:  # Changed from 100
        result = predict_phishing(url.strip())
        results.append(result)
```

### Add new endpoint
**File**: `app/app.py`
```python
@app.route('/custom-endpoint', methods=['POST'])
def custom_endpoint():
    data = request.get_json()
    # Custom logic here
    return jsonify(result), 200
```

---

**Documentation Version**: 1.0
**Last Updated**: 2024
**Target Audience**: Developers & Educators
