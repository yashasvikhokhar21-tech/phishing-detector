# 🚀 Setup Guide - Phishing Detector

A step-by-step guide to get the Phishing Detector up and running.

## Table of Contents

1. [Quick Start (5 minutes)](#quick-start-5-minutes)
2. [Detailed Installation](#detailed-installation)
3. [Training the Model](#training-the-model)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start (5 minutes)

### For Windows Users

```bash
# 1. Navigate to project directory
cd phishing-detector

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model
python ml/train_model.py

# 5. Run the application
python app/app.py

# 6. Open browser to http://localhost:5000
```

### For macOS/Linux Users

```bash
# 1. Navigate to project directory
cd phishing-detector

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model
python ml/train_model.py

# 5. Run the application
python app/app.py

# 6. Open browser to http://localhost:5000
```

---

## Detailed Installation

### Requirements

- **Python**: 3.8 or higher
- **pip**: Python package manager (comes with Python)
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (recommended 4GB+)
- **Disk Space**: ~500MB for dependencies and models

### Step 1: Check Python Installation

```bash
python --version
# or
python3 --version
```

Should show Python 3.8 or higher.

### Step 2: Download/Clone Project

If you haven't already:
```bash
cd Downloads
# Assuming project is already extracted
cd phishing-detector
```

### Step 3: Create Virtual Environment

**Why virtual environment?** It isolates project dependencies from system Python, preventing conflicts.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verification:**
You should see `(venv)` at the beginning of your terminal line.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**What's being installed:**
- `Flask`: Web framework
- `scikit-learn`: Machine learning library
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `Werkzeug`: WSGI utilities
- `joblib`: Serialization

**Verification:**
```bash
pip list
```

---

## Training the Model

### Run Training Script

```bash
python ml/train_model.py
```

### What Happens

1. **Creates Sample Dataset**: 12 legitimate + 12 phishing URLs
2. **Extracts Features**: Analyzes each URL
3. **Trains Model**: Random Forest with 100 estimators
4. **Evaluates Performance**: Shows accuracy, precision, recall
5. **Saves Model**: Saves to `models/phishing_model.pkl`
6. **Saves Scaler**: Saves to `models/scaler.pkl`

### Expected Output

```
Creating sample dataset...
Dataset size: 24 URLs
Legitimate URLs: 12
Phishing URLs: 12

Training Random Forest model...
Training completed!

==================================================
MODEL EVALUATION
==================================================

TRAINING SET METRICS:
Accuracy:  1.0000
Precision: 1.0000
Recall:    1.0000
F1-Score:  1.0000

TEST SET METRICS:
Accuracy:  0.8000
Precision: 1.0000
Recall:    0.6667
F1-Score:  0.8000

CONFUSION MATRIX (Test Set):
[[2 0]
 [1 2]]

==================================================
FEATURE IMPORTANCE
==================================================

1. URL Length: 0.3542
2. Hyphens in Domain: 0.2156
3. Special Characters: 0.1893
4. @ Symbol: 0.0945
...

✓ Model training completed successfully!
```

### Files Generated

After running `train_model.py`, two new files are created:

```
models/
├── phishing_model.pkl     (Random Forest model)
└── scaler.pkl             (Feature scaler)
```

These files are required to run the Flask application.

---

## Running the Application

### Start Flask Server

```bash
python app/app.py
```

### Expected Output

```
Initializing Phishing Detector App...
✓ Model and scaler loaded successfully
Starting Flask app on http://localhost:5000
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Access Web Interface

Open your browser and go to:
```
http://localhost:5000
```

### Web Interface Features

**Home Page:**
- Check Single URL
- Check Multiple URLs
- Information about how it works
- Explanation of features

**Results Display:**
- Phishing/Legitimate indicator
- Confidence score (0-100%)
- Extracted features
- Batch statistics

### Stopping the Server

Press `Ctrl+C` in the terminal running the Flask app.

---

## Testing

### Test 1: Feature Extraction

```bash
python example.py
```

This demonstrates how the feature extractor works without needing the trained model.

### Test 2: Single URL Check

1. Go to http://localhost:5000
2. Enter a URL: `https://www.google.com`
3. Click "Analyze URL"
4. Should show **Legitimate** with high confidence

### Test 3: Batch URLs

1. Enter multiple URLs:
   ```
   https://www.google.com
   https://github.com
   https://fake-paypal-login.xyz
   ```
2. Click "Analyze URLs"
3. Should detect the suspicious ones

### Test 4: API Testing

Using curl or Postman:

```bash
# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'

# Batch prediction
curl -X POST http://localhost:5000/batch-predict \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://fake-bank.xyz"]}'

# Health check
curl http://localhost:5000/health
```

---

## Troubleshooting

### Issue 1: Python Not Found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
- Add Python to system PATH
- Use `python3` instead of `python`
- Reinstall Python with "Add to PATH" checked

### Issue 2: Virtual Environment Not Activating

**Windows:**
```bash
# Try PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Issue 3: Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
pip install -r requirements.txt
```

Make sure virtual environment is activated first.

### Issue 4: Model Files Not Found

**Error:**
```
⚠ Model files not found
```

**Solution:**
```bash
python ml/train_model.py
```

Models must be trained before running the Flask app.

### Issue 5: Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

Or use a different port:
```bash
# Edit app/app.py, change port parameter
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue 6: Import Errors from Features Module

**Error:**
```
ModuleNotFoundError: No module named 'features'
```

**Solution:**
- Make sure you're running scripts from the project root directory
- Check that `features/__init__.py` exists
- Check the import paths in scripts

### Issue 7: CORS Errors in Frontend

**Error:**
```
Cross-Origin Request Blocked
```

**Solution:**
Currently, the demo runs on the same origin. For development:
- If frontend and backend on different ports, add CORS support

```python
from flask_cors import CORS
CORS(app)
```

Then install: `pip install flask-cors`

---

## Next Steps

After successful setup:

### 1. Explore the Code
- Read through `features/url_features.py` to understand feature extraction
- Review `ml/train_model.py` to see how the model is trained
- Check `app/app.py` for Flask routes and API endpoints

### 2. Test with More URLs
- Add legitimate URLs to test
- Add known phishing URLs
- Observe confidence scores

### 3. Improve the Model
- Collect more training data
- Add new features
- Experiment with different algorithms

### 4. Deploy to Production
- Use a production WSGI server (Gunicorn, uWSGI)
- Set up environment variables
- Deploy to cloud (AWS, Azure, Heroku, etc.)

### 5. Extend Functionality
- Add URL database for caching
- Implement user accounts
- Add API rate limiting
- Create browser extension

---

## File Locations Quick Reference

```
phishing-detector/
├── app/
│   ├── app.py                    ← Main Flask app (Run this)
│   └── __init__.py
├── ml/
│   ├── train_model.py            ← Train model (Run this first)
│   └── __init__.py
├── features/
│   ├── url_features.py           ← Feature extraction logic
│   └── __init__.py
├── static/
│   ├── style.css                 ← Styling
│   └── script.js                 ← Frontend logic
├── templates/
│   └── index.html                ← Web interface
├── models/                       ← Generated after training
│   ├── phishing_model.pkl
│   └── scaler.pkl
├── config.py                     ← Configuration
├── requirements.txt              ← Dependencies
├── README.md                     ← Full documentation
├── SETUP_GUIDE.md               ← This file
├── example.py                   ← Feature extraction example
└── .gitignore
```

---

## Performance Tips

### Faster Training
- Comment out detailed output
- Use sample_fract for larger datasets
- Parallelize with n_jobs=-1 (already enabled)

### Faster Predictions
- Use caching for repeated URLs
- Implement batch processing
- Use async/await for concurrent requests

### Reduce Memory Usage
- Use fewer trees in Random Forest
- Reduce dataset size
- Use pickle protocol 4 for models

---

## Getting Help

1. **Check the README.md** - Comprehensive documentation
2. **Review example.py** - Working example
3. **Check error messages** - Usually helpful
4. **Read code comments** - Well-documented code
5. **Review troubleshooting** - Common issues above

---

## Success Checklist

- ✅ Python 3.8+ installed
- ✅ Virtual environment created and activated
- ✅ Dependencies installed from requirements.txt
- ✅ Model trained with `python ml/train_model.py`
- ✅ Model files created in `models/` folder
- ✅ Flask app running with `python app/app.py`
- ✅ Web interface accessible at localhost:5000
- ✅ Can check URLs and get predictions

---

**Congratulations!** 🎉 Your Phishing Detector is ready to use!

For advanced topics, see README.md.
