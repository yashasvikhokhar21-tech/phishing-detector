# 📖 Quick Reference Guide

A quick cheat sheet for the Phishing Detector project.

## 🎯 3-Step Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train model
python ml/train_model.py

# 3. Run app
python app/app.py
# Then open: http://localhost:5000
```

---

## 📁 Directory Map

```
app/app.py              ← Flask web app (run this)
ml/train_model.py       ← Train ML model (run this first)
features/url_features.py ← URL analysis engine
config.py               ← Settings
static/style.css        ← Styling
static/script.js        ← Frontend logic
templates/index.html    ← Web interface
README.md               ← Full docs
SETUP_GUIDE.md         ← Step-by-step
```

---

## 🔧 Common Commands

| Task | Command |
|------|---------|
| Activate venv (Windows) | `venv\Scripts\activate` |
| Activate venv (Mac/Linux) | `source venv/bin/activate` |
| Install dependencies | `pip install -r requirements.txt` |
| Train model | `python ml/train_model.py` |
| Run app | `python app/app.py` |
| Test feature extraction | `python example.py` |
| Check if port 5000 in use | `netstat -ano \| findstr :5000` |

---

## 🚀 URL Features (8 Total)

1. URL Length
2. Dots Count
3. Hyphens in Domain
4. @ Symbol Presence
5. HTTPS Protocol
6. Domain Length
7. Numeric Ratio
8. Special Characters Count

---

## 🤖 Model Details

- **Type**: Random Forest Classifier
- **Trees**: 100
- **Time to train**: < 1 second
- **Output**: Binary (Phishing/Legitimate)
- **Confidence**: 0.0 - 1.0

---

## 🌐 API Endpoints

```
POST /predict
  Body: {"url": "https://..."}
  Returns: prediction, confidence, features

POST /batch-predict
  Body: {"urls": ["https://...", "https://..."]}
  Returns: array of predictions

GET /health
  Returns: status, model_loaded
```

---

## 💻 Key Code Snippets

### Extract Features from URL
```python
from features.url_features import URLFeatureExtractor
extractor = URLFeatureExtractor()
features = extractor.extract_features("https://example.com")
print(features)  # [length, dots, hyphens, @, https, domain_len, numeric, special]
```

---

## 📊 Data Preprocessing Quick Start

### Option 1: Simple Loader (No Dependencies)

```python
from ml.simple_loader import SimpleDataLoader

loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
loader.load_csv()
X, y = loader.separate_features_labels(drop_cols=['url'])
loader.print_summary()
```

**Run:** `python ml/simple_loader.py`

### Option 2: Advanced Loader (Pandas)

```python
from ml.data_loader import DataLoader

loader = DataLoader('datasets/sample_phishing_data.csv')
loader.load_data()
loader.clean_data(handle_missing='mean')
X, y = loader.separate_features_and_labels()
loader.print_summary()
```

**Install:** `pip install pandas numpy scikit-learn`

**Run:** `python ml/preprocess_example.py`

---

## 📋 Data Loading API

| Method | Purpose |
|--------|---------|
| `load_csv()` / `load_data()` | Load CSV file |
| `print_info()` / `display_info()` | Show dataset info |
| `separate_features_labels()` / `separate_features_and_labels()` | Split X and y |
| `print_summary()` | Show statistics |
| `clean_data()` | Handle missing values (DataLoader only) |
| `save_processed_data()` | Save to CSV (DataLoader only) |

---

## 🎯 Data Preprocessing Patterns

**Access first sample:**
```python
print(X[0])  # {'domain_length': 11.0, 'special_chars': 3.0, ...}
```

**Check class balance:**
```python
from collections import Counter
print(Counter(y))  # Counter({0: 13, 1: 12})
```

**Feature statistics:**
```python
values = [sample['domain_length'] for sample in X]
print(f"Avg: {sum(values)/len(values):.1f}")
```

**Train-test split:**
```python
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
```

**With scikit-learn:**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test):.2%}")
```

---

## 📁 Data Files

```
datasets/sample_phishing_data.csv    ← Sample data (25 URLs)
ml/simple_loader.py                   ← Simple implementation (pure Python)
ml/data_loader.py                     ← Advanced implementation (pandas)
ml/preprocess_example.py              ← Interactive examples
ml/DATA_PREPROCESSING_GUIDE.md        ← Detailed documentation
```

---

## 🔍 Sample Dataset

- **Samples:** 25 URLs
- **Features:** 8 (domain_length, special_chars, https, hyphens, dots, numeric_chars, @symbol)
- **Class balance:** 13 safe (52%), 12 phishing (48%)
- **Format:** CSV with header row

---

## ⚠️ Troubleshooting Data Loading

| Issue | Fix |
|-------|-----|
| `FileNotFoundError` | Check path: `import os; os.path.exists('path')` |
| `KeyError` on column | Check column name exists in CSV |
| `ModuleNotFoundError: pandas` | Install: `pip install pandas` |
| No data after load | Call `load_csv()` first |
| Empty features (X) | Don't drop all columns with `drop_cols` |

---

## 📚 Full Documentation

- **Data Preprocessing:** [DATA_PREPROCESSING_GUIDE.md](ml/DATA_PREPROCESSING_GUIDE.md)
- **Data Reference:** [DATA_PREPROCESSING_README.md](ml/DATA_PREPROCESSING_README.md)
- **Project Setup:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Full Documentation:** [README.md](README.md)

### Train Model
```python
from ml.train_model import PhishingModelTrainer
trainer = PhishingModelTrainer()
trainer.train()
trainer.evaluate()
trainer.save_model()
```

### Make Prediction
```python
import pickle
with open('models/phishing_model.pkl', 'rb') as f:
    model = pickle.load(f)
# Use model.predict(features_scaled)
```

---

## 🔍 Troubleshooting Guide

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Model not found | `python ml/train_model.py` |
| Port in use | Kill process on 5000 or use different port |
| ImportError: features | Ensure __init__.py exists in features/ |
| Virtual env not working | Try: `python -m venv venv` |

---

## 📊 File Sizes (Approximate)

- `phishing_model.pkl` - 50-100 KB
- `scaler.pkl` - 5 KB
- `app.py` - 5 KB
- `url_features.py` - 4 KB
- `train_model.py` - 6 KB
- Total dependencies - ~150 MB

---

## 🎨 UI Features

```
Frontend
├── Single URL Analysis
│   ├── Input field
│   ├── Analyze button
│   └── Results display
│
├── Batch Analysis
│   ├── Textarea (up to 100 URLs)
│   ├── Analyze button
│   └── Results table
│
└── Info Sections
    ├── How it works
    └── Feature explanations
```

---

## 🔐 Security Notes

- Input validation on all endpoints
- URL format checking
- No URL logging by default
- XSS protection via HTML escaping
- CORS can be added if needed

---

## 📈 Improvement Ideas

✓ Add more training samples
✓ Use real phishing datasets (PhishTank)
✓ Add SSL certificate features
✓ Implement domain reputation scoring
✓ Add user feedback mechanism
✓ Deploy with Docker
✓ Add database logging
✓ Implement API authentication

---

## 🚢 Deployment Checklist

- ✅ Change SECRET_KEY in config.py
- ✅ Set DEBUG = False
- ✅ Use Gunicorn/uWSGI instead of Flask dev server
- ✅ Set up environment variables
- ✅ Use HTTPS
- ✅ Configure CORS headers
- ✅ Set up rate limiting
- ✅ Add database for caching
- ✅ Monitor error logs
- ✅ Regular model retraining

---

## 📚 Related Files

- **requirements.txt** - See all dependencies
- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Detailed setup instructions
- **project_setup.md** - Architecture overview
- **config.py** - Configuration options
- **.gitignore** - What to ignore in git

---

## 🎯 Learning Resources

- scikit-learn: https://scikit-learn.org/
- Flask: https://flask.palletsprojects.com/
- URL Analysis: Research phishing detection papers
- ML Fundamentals: Andrew Ng's course

---

## ❓ FAQ

**Q: Can I modify features?**
A: Yes! Edit `features/url_features.py` and retrain with `python ml/train_model.py`

**Q: How do I add more training data?**
A: Modify `create_sample_dataset()` in `ml/train_model.py`

**Q: Can I use a different ML model?**
A: Yes! Replace RandomForestClassifier in `ml/train_model.py`

**Q: How do I deploy to production?**
A: Use Gunicorn, Docker, and a cloud provider (AWS/Azure/GCP)

**Q: Is it 100% accurate?**
A: No. No detection system is perfect. Always verify suspicious sites.

---

**Last Updated**: 2024
**Version**: 1.0
**Status**: Production-Ready (Demo Data)
