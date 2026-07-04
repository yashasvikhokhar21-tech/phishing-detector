"""
Flask Application for Phishing Website Detection
Integrated with MongoDB Atlas for prediction logging and threat intelligence
"""

import logging
import os
import pickle
import sys
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import feature extractor and rule-based detector
from features.url_features import URLFeatureExtractor, check_url_rules
from services.threat_intel import check_threat_intelligence

# Import MongoDB client for logging predictions
try:
    from db import get_mongodb_client, log_prediction
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("⚠ MongoDB module not available. Running in file-logging mode.")


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max

# Load trained model and scaler
MODEL_PATH = 'models/phishing_model.pkl'
SCALER_PATH = 'models/scaler.pkl'
LOG_DIR = 'logs'
LOG_PATH = os.path.join(LOG_DIR, 'predictions.log')

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logger = logging.getLogger('phishing_detector')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_PATH, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

model = None
scaler = None
extractor = URLFeatureExtractor()

# Initialize MongoDB client if available
mongodb_client = None
if MONGODB_AVAILABLE:
    try:
        mongodb_client = get_mongodb_client()
        if mongodb_client.health_check():
            logger.info("✓ MongoDB Atlas connected successfully")
    except Exception as e:
        logger.warning(f"⚠ MongoDB connection failed: {e}. Using file logging only.")
        mongodb_client = None


def load_model():
    """Load the trained model and scaler"""
    global model, scaler
    
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            with open(SCALER_PATH, 'rb') as f:
                scaler = pickle.load(f)
            print("✓ Model and scaler loaded successfully")
            return True
        else:
            print("⚠ Model files not found. Train model first using ml/train_model.py")
            return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def predict_phishing(url):
    """
    Predict if a URL is phishing or legitimate
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        dict: Prediction result with confidence
    """
    try:
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Extract features
        features = extractor.extract_features(url)
        print("URL:", url)
        print("Extracted Features:", features)
        features_array = np.array([features])
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        confidence = max(model.predict_proba(features_scaled)[0])
        
        rule_result = check_url_rules(url)
        threat_result = check_threat_intelligence(url)
        
        final_score = min(1.0, float(confidence) * 0.6 + float(rule_result['score']) * 0.2 + float(threat_result['score']) * 0.2)
        
        # Determine final prediction based on threat intelligence
        is_phishing = bool(prediction) or threat_result['blacklisted']

        result = {
            'url': url,
            'is_phishing': is_phishing,
            'confidence': float(confidence),
            'rule_score': float(rule_result['score']),
            'rule_reasons': rule_result['reasons'],
            'threat_intel_result': threat_result,
            'final_score': float(final_score),
            'prediction_text': 'Phishing Detected ⚠️' if is_phishing else 'Legitimate ✓',
            'features': {
                'URL Length': features[0],
                'Dots Count': features[1],
                'Hyphens in Domain': features[2],
                'Has @ Symbol': features[3],
                'HTTPS Protocol': features[4],
                'Domain Length': features[5],
                'Numeric Ratio': f"{features[6]*100:.2f}%",
                'Special Characters': features[7]
            }
        }

        # Log prediction to file
        logger.info(
            'URL=%s | prediction=%s | confidence=%.4f | rule_score=%.4f | threat_intel=%s | final_score=%.4f',
            url,
            result['prediction_text'],
            result['confidence'],
            result['rule_score'],
            threat_result['blacklisted'],
            result['final_score']
        )
        
        # Log prediction to MongoDB if available
        if mongodb_client:
            try:
                user_ip = request.remote_addr if request else None
                log_prediction(
                    url=url,
                    prediction_result='phishing' if is_phishing else 'legitimate',
                    confidence=confidence,
                    threat_intel_result=threat_result,
                    rule_based_result=rule_result,
                    user_ip=user_ip
                )
            except Exception as e:
                logger.warning(f"Failed to log prediction to MongoDB: {e}")

        return result
    except Exception as e:
        return {
            'error': str(e),
            'is_phishing': None,
            'confidence': 0
        }


@app.route('/')
def index():
    """Home page"""
    model_loaded = model is not None
    mongodb_status = "Connected" if mongodb_client else "Not Available"
    return render_template('index.html', model_loaded=model_loaded, mongodb_status=mongodb_status)


@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for prediction"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL cannot be empty'}), 400
        
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.',
                'is_phishing': None
            }), 503
        
        result = predict_phishing(url)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({'error': 'No URLs provided'}), 400
        
        if model is None:
            return jsonify({
                'error': 'Model not loaded',
                'results': []
            }), 503
        
        results = []
        for url in urls[:100]:  # Limit to 100 URLs
            result = predict_phishing(url.strip())
            results.append(result)
        
        safe_count = sum(1 for r in results if r.get('is_phishing') is False and 'error' not in r)
        phishing_count = sum(1 for r in results if r.get('is_phishing') is True)
        
        return jsonify({
            'total': len(results),
            'phishing_count': phishing_count,
            'safe_count': safe_count,
            'error_count': error_count,
            'results': results
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    mongodb_healthy = False
    if mongodb_client:
        try:
            mongodb_healthy = mongodb_client.health_check()
        except Exception as e:
            logger.warning(f"MongoDB health check failed: {e}")
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'mongodb_connected': mongodb_healthy
    }), 200


@app.route('/stats')
def stats():
    """Get prediction statistics from MongoDB"""
    if not mongodb_client:
        return jsonify({'error': 'MongoDB not available'}), 503
    
    try:
        from db import get_prediction_stats
        stats_data = get_prediction_stats(limit_days=30)
        return jsonify(stats_data), 200
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Initializing Phishing Detector App...")
    print("=" * 60)
    
    # Load model
    if load_model():
        print("\n✓ Model loaded successfully")
        if mongodb_client:
            print("✓ MongoDB Atlas connected")
        else:
            print("⚠ MongoDB not connected - using file logging only")
        print("\nStarting Flask app on http://localhost:5000")
        print("=" * 60)
        app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        print("✗ Unable to start app without trained model")
        print("Please run: python ml/train_model.py")
        print("=" * 60)
