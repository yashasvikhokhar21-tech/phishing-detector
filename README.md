# 🛡️ Phishing Website Detector

An AI-powered machine learning system to detect phishing websites using URL feature extraction and Random Forest classification.

## Features

- **URL Analysis**: Extracts 8 key features from URLs for detection
- **ML Model**: Random Forest classifier trained on legitimate and phishing URLs
- **Web Interface**: Clean, modern Flask web application
- **Batch Analysis**: Check multiple URLs at once
- **Real-time Predictions**: Instant results with confidence scores
- **Production-Ready**: Modular, scalable, and well-documented code

## Project Structure

```
phishing-detector/
├── app/
│   └── app.py                 # Flask application
├── ml/
│   └── train_model.py         # ML model training script
├── features/
│   └── url_features.py        # URL feature extraction module
├── static/
│   ├── style.css              # CSS styling
│   └── script.js              # Frontend JavaScript
├── templates/
│   └── index.html             # Main HTML page
├── models/                    # Trained models (generated after training)
│   ├── phishing_model.pkl
│   └── scaler.pkl
├── config.py                  # Configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .gitignore                 # Git ignore file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone/Download the project**
   ```bash
   cd phishing-detector
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Train the Model

First, you need to train the machine learning model:

```bash
python ml/train_model.py
```

This will:
- Create a sample dataset of legitimate and phishing URLs
- Train a Random Forest classifier
- Save the model to `models/phishing_model.pkl`
- Save the scaler to `models/scaler.pkl`
- Display performance metrics

**Expected Output:**
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

...
```

### Step 2: Run the Flask Application

```bash
python app/app.py
```

The application will start at `http://localhost:5000`

### Step 3: Use the Web Interface

Open your browser and navigate to `http://localhost:5000`

**Features:**
- **Check Single URL**: Enter a URL and analyze it
- **Batch Analysis**: Enter multiple URLs (one per line)
- **Results**: View predictions with confidence scores and extracted features

## Extracted URL Features

The model analyzes these 8 features from each URL:

1. **URL Length**: Longer URLs are often phishing attempts
2. **Dots Count**: Multiple dots can indicate suspicious domains
3. **Hyphens in Domain**: Legitimate domains rarely use hyphens
4. **@ Symbol**: Presence indicates potential spoofing
5. **HTTPS Protocol**: Legitimate sites typically use HTTPS
6. **Domain Length**: Unusual lengths may be suspicious
7. **Numeric Ratio**: High numeric content can be suspicious
8. **Special Characters**: Excessive special characters are suspicious

## API Endpoints

### Single URL Prediction
```
POST /predict
Content-Type: application/json

{
  "url": "https://example.com"
}

Response:
{
  "url": "https://example.com",
  "is_phishing": false,
  "confidence": 0.95,
  "prediction_text": "Legitimate ✓",
  "features": {...}
}
```

### Batch URL Prediction
```
POST /batch-predict
Content-Type: application/json

{
  "urls": ["https://example1.com", "https://example2.com"]
}

Response:
{
  "total": 2,
  "phishing_count": 0,
  "results": [...]
}
```

### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "model_loaded": true
}
```

## Configuration

Edit `config.py` to customize:
- Flask settings (DEBUG, SECRET_KEY)
- Model paths
- Maximum file sizes
- Batch prediction limits

## Development

### Running Tests

```bash
python test.py
```

### Code Structure

**`features/url_features.py`**
- `URLFeatureExtractor`: Extracts 8 features from URLs
- Used by both training and prediction

**`ml/train_model.py`**
- `PhishingModelTrainer`: Trains Random Forest model
- Handles data creation, model training, and evaluation
- Saves models for inference

**`app/app.py`**
- Flask routes for web interface and API
- Handles single and batch predictions
- Loads trained models for inference

**`static/`**
- Frontend CSS and JavaScript
- Modern, responsive UI
- Real-time form validation

**`templates/`**
- HTML templates for web interface
- Information about how the detector works
- Feature explanations

## Model Performance

On the sample dataset:
- **Training Accuracy**: 100%
- **Test Accuracy**: 80%
- **Precision**: High (minimal false positives)
- **Recall**: Good coverage of phishing attempts

*Note: This is a demonstration model. For production use, train on larger, real-world datasets.*

## Improving the Model

To improve accuracy:

1. **Expand Dataset**
   - Collect more URLs (legitimate and phishing)
   - Use public datasets (e.g., PhishTank, UCI Machine Learning Repository)

2. **Add Features**
   - SSL certificate information
   - Domain age
   - User engagement metrics
   - Content-based features

3. **Feature Engineering**
   - Domain similarity to popular brands
   - Entropy analysis
   - Lexical patterns

4. **Ensemble Methods**
   - Combine multiple models
   - Try Gradient Boosting or XGBoost
   - Weighted voting

5. **Hyperparameter Tuning**
   - Use GridSearchCV or RandomizedSearchCV
   - Optimize n_estimators, max_depth, etc.

## Troubleshooting

### Model Not Loading
**Error**: "Model files not found"

**Solution**: 
```bash
python ml/train_model.py
```

### Port Already in Use
**Error**: "Address already in use"

**Solution**:
```bash
# Kill the process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Import Errors
**Error**: "ModuleNotFoundError"

**Solution**:
```bash
pip install -r requirements.txt
```

## Security Considerations

- **HTTPS Only**: Always use HTTPS in production
- **Input Validation**: URLs are validated before processing
- **Rate Limiting**: Consider adding rate limiting for production
- **CORS**: Configure appropriate CORS policies
- **Secrets**: Change SECRET_KEY in production
- **Model Protection**: Keep trained models secure

## Best Practices Used

✓ **Modularity**: Separate concerns (features, ML, web)
✓ **Configuration**: Centralized config management
✓ **Error Handling**: Comprehensive error handling
✓ **Documentation**: Clear docstrings and comments
✓ **Validation**: Input validation on all endpoints
✓ **Scalability**: Stateless design for deployment
✓ **Testing**: Sample test cases included
✓ **Security**: Input sanitization and validation

## Future Enhancements

- [ ] Deep Learning models (CNN, RNN)
- [ ] Real-time database of known phishing URLs
- [ ] Browser extension integration
- [ ] Advanced visualization of analysis
- [ ] User feedback loop for model improvement
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Cloud deployment (AWS, Azure, GCP)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact & Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email]

## Disclaimer

This tool is for educational purposes. While it can detect many phishing attempts, no detection system is 100% accurate. Always verify websites before entering sensitive information.

---

**Made with ❤️ for cybersecurity education**
