# MongoDB Atlas Implementation Guide

## Complete Implementation Summary

This guide summarizes all the changes made to integrate MongoDB Atlas with your phishing-detector application.

---

## What Was Done

### 1. **Created MongoDB Integration Layer** (`db/` directory)

#### Files Created:
- `db/__init__.py` - Package initialization with exported functions
- `db/mongodb_client.py` - MongoDB connection manager and utility functions

#### Key Features:
- ✓ Singleton MongoDB client for connection pooling
- ✓ Health check functionality
- ✓ Index creation for query optimization
- ✓ Helper functions for logging predictions
- ✓ Domain blacklist management
- ✓ Prediction statistics aggregation

### 2. **Updated Application Files**

#### `config.py` - Added MongoDB Configuration
```python
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')
MONGODB_COLLECTION_PREDICTIONS = os.environ.get('MONGODB_COLLECTION_PREDICTIONS')
MONGODB_COLLECTION_BLACKLIST = os.environ.get('MONGODB_COLLECTION_BLACKLIST')
MONGODB_COLLECTION_CONFIG = os.environ.get('MONGODB_COLLECTION_CONFIG')
```

#### `app/app.py` - Integrated MongoDB Logging
- Imports MongoDB client for logging
- Logs all predictions to MongoDB
- Added `/health` endpoint with MongoDB status
- Added `/stats` endpoint for prediction statistics
- Graceful fallback if MongoDB unavailable

#### `services/threat_intel.py` - MongoDB-Backed Blacklist
- Changed from hardcoded Python set to MongoDB storage
- Maintains in-memory cache for performance
- Supports adding/removing domains via MongoDB
- Automatic cache refresh capability

### 3. **Environment Configuration**

#### Files Created:
- `.env.example` - Template for environment variables
- `requirements.txt` - Updated with new dependencies

#### New Dependencies Added:
```
pymongo>=4.0.0
python-dotenv>=0.19.0
gunicorn>=20.1.0
```

### 4. **Database Initialization**

#### `init_mongodb.py`
Automated script to:
- Create MongoDB collections
- Create database indexes
- Initialize seed data
- Verify connection

### 5. **Testing & Deployment Files**

#### `test_mongodb_connection.py`
- Verifies MongoDB Atlas connection
- Checks collection creation
- Provides troubleshooting guidance

#### `Procfile`
- Heroku deployment configuration

#### `runtime.txt`
- Python version specification

### 6. **Documentation**

#### Created:
- `MONGODB_ATLAS_DEPLOYMENT.md` - Complete 7-phase deployment guide
- `MONGODB_QUICK_REFERENCE.md` - Quick setup and commands
- `HEROKU_DEPLOYMENT_GUIDE.md` - Heroku-specific deployment

---

## Database Structure

### Collections Created

#### 1. **predictions**
```javascript
{
  _id: ObjectId,
  timestamp: Date,
  url: String,
  prediction_result: String,  // "phishing" or "legitimate"
  confidence: Number,
  threat_intel_result: Object,
  rule_based_result: Object,
  user_ip: String
}
```

**Indexes:**
- `timestamp` (ascending)
- `url` (ascending)
- `timestamp` (descending) - for sorting

#### 2. **phishing_domains**
```javascript
{
  _id: ObjectId,
  domain: String,  // lowercase
  added_date: Date,
  status: String  // "active"
}
```

**Indexes:**
- `domain` (ascending)

#### 3. **app_config**
```javascript
{
  _id: ObjectId,
  setting_name: String,
  setting_value: Any,
  last_updated: Date
}
```

---

## Configuration Setup

### Required Environment Variables

Create `.env` file in project root:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=phishing_detector
MONGODB_COLLECTION_PREDICTIONS=predictions
MONGODB_COLLECTION_BLACKLIST=phishing_domains
MONGODB_COLLECTION_CONFIG=app_config

# Flask
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DEBUG=False
USE_MONGODB_LOGGING=True
```

**Never commit this file!** It's in `.gitignore`.

---

## Step-by-Step Setup Instructions

### Phase 1: MongoDB Atlas Setup (10 minutes)

```bash
# 1. Create Account: https://www.mongodb.com/cloud/atlas
# 2. Create Free Cluster (M0 tier)
# 3. Create Database User
# 4. Whitelist IP Address
# 5. Get Connection String
```

### Phase 2: Local Setup (5 minutes)

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env with your MongoDB credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test MongoDB connection
python test_mongodb_connection.py

# 4. Initialize database
python init_mongodb.py
```

### Phase 3: Run Application

```bash
# Start the Flask application
python app/app.py

# Application will be available at: http://localhost:5000
```

### Phase 4: Deploy to Production

See `HEROKU_DEPLOYMENT_GUIDE.md` for complete deployment steps.

---

## API Endpoints

### Authentication & Predictions

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/` | GET | Home page | HTML page |
| `/predict` | POST | Single URL prediction | JSON with prediction |
| `/batch-predict` | POST | Batch predictions | JSON with results |
| `/health` | GET | Health check | Status object |
| `/stats` | GET | Statistics | Prediction stats |

### Example Requests

**Single Prediction:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Statistics:**
```bash
curl http://localhost:5000/stats
```

---

## MongoDB Operations

### Python API

```python
# Import functions
from db import (
    get_mongodb_client,
    log_prediction,
    get_phishing_domains,
    add_phishing_domain,
    remove_phishing_domain,
    get_prediction_stats
)

# Get client
client = get_mongodb_client()

# Get collection
predictions = client.get_collection('predictions')

# Query predictions
recent = predictions.find().sort('timestamp', -1).limit(10)

# Get statistics
stats = get_prediction_stats(limit_days=30)

# Manage blacklist
add_phishing_domain("evil.com")
remove_phishing_domain("evil.com")
get_phishing_domains()
```

### MongoDB Shell Commands

```javascript
// Connect in MongoDB Atlas Web Shell

// View recent predictions
db.predictions.find().sort({ timestamp: -1 }).limit(10)

// Count predictions by type
db.predictions.aggregate([
  { $group: { _id: "$prediction_result", count: { $sum: 1 } } }
])

// View blacklist
db.phishing_domains.find()

// Add domain
db.phishing_domains.insertOne({ 
  domain: "evil.com", 
  added_date: new Date(), 
  status: "active" 
})

// Create index
db.predictions.createIndex({ timestamp: -1 })
```

---

## Performance Optimization

### Implemented Features

1. **Connection Pooling** - Reuses MongoDB connections
2. **Indexes** - Created automatically for frequent queries
3. **Caching** - Phishing domains cached in memory
4. **Batch Operations** - Supports up to 100 URLs per batch

### Recommended Practices

```python
# ✓ DO: Use batch predictions for multiple URLs
POST /batch-predict with 50-100 URLs

# ✓ DO: Cache frequently accessed data
from db import get_phishing_domains
domains = get_phishing_domains()  # Cached after first call

# ✓ DO: Archive old predictions periodically
db.predictions.deleteMany({ timestamp: { $lt: cutoff_date } })

# ❌ DON'T: Make excessive database calls
# ❌ DON'T: Store large files in MongoDB
# ❌ DON'T: Run queries without indexes
```

---

## Troubleshooting

### Connection Issues

**Error: "Couldn't connect to server"**
```
Solution:
1. Verify IP is whitelisted in MongoDB Atlas
2. Check MONGODB_URI has correct password
3. Ensure cluster is running
```

**Error: "authentication failed"**
```
Solution:
1. Verify username and password
2. Check for special characters in password
3. Try URL-encoding the password
```

### Runtime Issues

**Error: "ModuleNotFoundError: No module named 'pymongo'"**
```bash
pip install pymongo>=4.0.0
```

**Error: "Model not loaded"**
```bash
# Train the model first
python ml/train_model.py
```

### Deployment Issues

**Heroku: "Application error"**
```bash
# Check logs
heroku logs --tail

# Verify environment variables
heroku config

# Restart app
heroku restart
```

---

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] MongoDB password is strong
- [ ] `MONGODB_URI` never hardcoded
- [ ] IP whitelisting configured
- [ ] `SECRET_KEY` is random and long
- [ ] `DEBUG` is False in production
- [ ] HTTPS enabled (automatic in Heroku)
- [ ] Regular backups enabled
- [ ] Monitoring configured

---

## Monitoring & Maintenance

### Daily
- Check application logs
- Monitor error rates
- Verify MongoDB connection

### Weekly
- Review prediction statistics
- Check disk usage
- Monitor performance metrics

### Monthly
- Archive old predictions
- Review and update blacklist
- Rotate credentials if needed
- Check backup status

### Quarterly
- Update dependencies
- Review security settings
- Audit database size
- Plan capacity upgrades

---

## Rollback Procedures

### If Something Goes Wrong

```bash
# 1. Stop the application
# 2. Check logs for errors
# 3. Verify MongoDB connection
# 4. Check environment variables
# 5. Restart application

# For Heroku:
heroku rollback v5  # Rollback to previous version
git push heroku HEAD~1:main  # Push previous commit
```

---

## Next Steps

1. **Complete Deployment:**
   - Follow `MONGODB_ATLAS_DEPLOYMENT.md`
   - Deploy to Heroku using `HEROKU_DEPLOYMENT_GUIDE.md`

2. **Test & Validate:**
   - Run `test_mongodb_connection.py`
   - Test API endpoints
   - Verify predictions logging

3. **Monitor & Maintain:**
   - Set up alerts
   - Configure backups
   - Plan scaling strategy

4. **Enhance Application:**
   - Add more threat intelligence sources
   - Implement additional ML models
   - Create admin dashboard

---

## Support Resources

- **MongoDB Docs**: https://docs.mongodb.com/
- **PyMongo Docs**: https://pymongo.readthedocs.io/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Heroku Docs**: https://devcenter.heroku.com/

---

## Changes Summary Table

| Component | Changed | Details |
|-----------|---------|---------|
| Database | Added | MongoDB Atlas integration |
| Logging | Enhanced | Now logs to MongoDB |
| Blacklist | Migrated | From hardcoded set to MongoDB |
| Config | Expanded | Added MongoDB settings |
| API | Extended | Added `/stats` endpoint |
| Requirements | Updated | Added pymongo, python-dotenv, gunicorn |
| Deployment | Added | Heroku support (Procfile, runtime.txt) |
| Testing | Added | MongoDB connection test script |
| Documentation | Created | 3 new comprehensive guides |

---

**Implementation Date:** May 24, 2026  
**Versions:** Python 3.9+, MongoDB 4.0+, Flask 2.3+, PyMongo 4.0+

