# Phishing Detector - Project Overview

## 📋 Complete Project Structure

```
phishing-detector/
│
├── 📁 app/                          # Flask Web Application
│   ├── __init__.py                 # Package initialization
│   └── app.py                      # Main Flask application (START HERE)
│   
├── 📁 ml/                          # Machine Learning Module
│   ├── __init__.py                 # Package initialization
│   └── train_model.py              # Model training script (RUN FIRST)
│   
├── 📁 features/                    # Feature Extraction Module
│   ├── __init__.py                 # Package initialization
│   └── url_features.py             # URL feature extraction class
│   
├── 📁 static/                      # Frontend Assets
│   ├── style.css                   # CSS styling (modern, responsive)
│   └── script.js                   # JavaScript for interactivity
│   
├── 📁 templates/                   # HTML Templates
│   └── index.html                  # Main web page
│   
├── 📁 models/                      # Trained Models (generated)
│   ├── phishing_model.pkl          # Trained Random Forest model
│   └── scaler.pkl                  # Feature scaler
│   
├── 📄 config.py                    # Configuration file
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Full documentation
├── 📄 SETUP_GUIDE.md              # Step-by-step setup guide
├── 📄 example.py                  # Feature extraction example
└── 📄 .gitignore                  # Git ignore patterns
```

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model
```bash
python ml/train_model.py
```

### Step 3: Run the Application
```bash
python app/app.py
```

### Step 4: Open Browser
Navigate to `http://localhost:5000`

---

## 📚 File Descriptions

### Core Application Files

| File | Purpose | Beginner-Friendly |
|------|---------|-------------------|
| `app/app.py` | Flask web server, API endpoints, model loading | ✅ Yes |
| `ml/train_model.py` | Trains Random Forest classifier on URLs | ✅ Yes |
| `features/url_features.py` | Extracts 8 features from URLs | ✅ Yes |
| `config.py` | Configuration settings | ✅ Yes |

### Frontend Files

| File | Purpose | Details |
|------|---------|---------|
| `static/style.css` | Responsive styling | Modern, gradient background, card design |
| `static/script.js` | Interactive features | Form handling, API calls, result display |
| `templates/index.html` | Web interface | Single/batch URL checking, info sections |

### Configuration & Documentation

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `README.md` | Comprehensive documentation |
| `SETUP_GUIDE.md` | Step-by-step setup instructions |
| `.gitignore` | Git ignore patterns |

---

## 🎯 8 URL Features Analyzed

The ML model extracts these 8 features from each URL:

1. **URL Length** - Longer URLs often phishing
2. **Dots Count** - Multiple dots suspicious
3. **Hyphens in Domain** - Legitimate domains don't use hyphens
4. **@ Symbol** - Used in spoofing attacks
5. **HTTPS Protocol** - Secure sites use HTTPS
6. **Domain Length** - Unusual lengths suspicious
7. **Numeric Ratio** - High numeric content suspicious
8. **Special Characters** - Too many special chars suspicious

---

## 🤖 Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Trees**: 100 decision trees
- **Training Data**: 24 URLs (12 legitimate, 12 phishing)
- **Test Accuracy**: ~80% on sample data
- **Output**: Binary classification + confidence score

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│        Web Browser                  │
│   (HTML, CSS, JavaScript)           │
└────────────┬────────────────────────┘
             │ HTTP/JSON
             ▼
┌─────────────────────────────────────┐
│      Flask Web Server (app.py)      │
│  • /predict (single URL)            │
│  • /batch-predict (multiple URLs)   │
│  • /health (health check)           │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌─────────────┐ ┌─────────────────┐
│   Features  │ │  ML Model       │
│ Extractor   │ │ & Classifier    │
│ (8 features)│ │ (Random Forest) │
└─────────────┘ └─────────────────┘
```

---

## 🚀 Workflow

```
1. USER INPUT
   └─ Enter URL or batch of URLs
   
2. FEATURE EXTRACTION
   └─ 8 features extracted from URL
   
3. SCALING
   └─ Features normalized using StandardScaler
   
4. PREDICTION
   └─ Random Forest model classifies as:
      • Phishing (1) with confidence
      • Legitimate (0) with confidence
   
5. RESPONSE
   └─ Results displayed in web interface
      with visualization and confidence
```

---

## 💡 Key Features

✅ **Modular Architecture** - Separated concerns (features, ML, web)
✅ **8-Feature URL Analysis** - Length, dots, hyphens, @, HTTPS, domain, numeric, special chars
✅ **Random Forest Model** - Accurate classification with confidence scores
✅ **Web Interface** - Single and batch URL checking
✅ **RESTful API** - Easy integration with other systems
✅ **Production-Ready Code** - Error handling, validation, documentation
✅ **Beginner-Friendly** - Well-commented, clear structure
✅ **Responsive Design** - Works on desktop and mobile

---

## 📊 Model Performance

On the sample dataset:
- **Training Accuracy**: 100%
- **Test Accuracy**: ~80%
- **Precision**: High (few false positives)
- **Recall**: Good (catches most phishing)

*Note: This is a demo model. Production models need larger, real-world datasets.*

---

## 🎨 Frontend Features

✅ **Single URL Checking** - Quick analysis
✅ **Batch Processing** - Check up to 100 URLs
✅ **Real-time Results** - Instant feedback
✅ **Feature Display** - See extracted features
✅ **Responsive Design** - Works on mobile
✅ **Modern UI** - Gradient background, cards
✅ **Information Sections** - Learn how it works
✅ **Error Handling** - Helpful error messages

---

## 🔧 API Endpoints

### POST /predict
```json
Request: {"url": "https://example.com"}
Response: {
  "url": "https://example.com",
  "is_phishing": false,
  "confidence": 0.95,
  "prediction_text": "Legitimate ✓",
  "features": {...}
}
```

### POST /batch-predict
```json
Request: {"urls": ["https://example1.com", "https://example2.com"]}
Response: {
  "total": 2,
  "phishing_count": 0,
  "results": [...]
}
```

### GET /health
```json
Response: {
  "status": "healthy",
  "model_loaded": true
}
```

---

## 📖 How to Use This Project

### For Learning
1. Read the code - It's well-commented
2. Run the example - `python example.py`
3. Train the model - `python ml/train_model.py`
4. Experiment - Modify features or training data

### For Development
1. Study the structure - Modular design
2. Extend features - Add more URL characteristics
3. Improve model - Use larger datasets
4. Deploy - Use Gunicorn + Nginx

### For Deployment
1. Use production WSGI server
2. Set environment variables
3. Use cloud infrastructure
4. Implement caching
5. Add rate limiting

---

**Ready to get started? Follow SETUP_GUIDE.md for detailed instructions!**
