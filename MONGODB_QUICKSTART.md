# Quick Start Guide: MongoDB Atlas Deployment

## 🚀 5-Minute Quick Start

### Prerequisites
- MongoDB Atlas Account (create free: https://www.mongodb.com/cloud/atlas)
- Python 3.9+
- Git

### 1. Create MongoDB Cluster
```
1. Visit https://www.mongodb.com/cloud/atlas
2. Click "Create Free Cluster"
3. Select AWS, US region
4. Wait for initialization
```

### 2. Create Database User
```
1. Go to "Database Access"
2. Click "Add New Database User"
3. Username: phishing_app_user
4. Password: (generate strong password - save it!)
5. Role: Read and write to any database
```

### 3. Configure Network Access
```
1. Go to "Network Access"
2. Click "Add IP Address"
3. Select "Allow from Anywhere" (for testing)
4. Click "Confirm"
```

### 4. Get Connection String
```
1. Click "Connect" on your cluster
2. Select "Drivers"
3. Choose "Python 3.6 or later"
4. Copy connection string
5. Replace <password> with your actual password
```

### 5. Create .env File
```bash
# In project directory:
cp .env.example .env

# Edit .env and add your connection string:
MONGODB_URI=mongodb+srv://phishing_app_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### 6. Install & Initialize
```bash
# Install dependencies
pip install -r requirements.txt

# Test MongoDB connection
python test_mongodb_connection.py

# Initialize database
python init_mongodb.py
```

### 7. Run Application
```bash
# Start Flask server
python app/app.py

# Visit: http://localhost:5000
```

---

## 📋 Complete Documentation

| Guide | Purpose | Time |
|-------|---------|------|
| [MONGODB_ATLAS_DEPLOYMENT.md](MONGODB_ATLAS_DEPLOYMENT.md) | Complete 7-phase deployment | 2 hours |
| [MONGODB_QUICK_REFERENCE.md](MONGODB_QUICK_REFERENCE.md) | Quick commands & troubleshooting | 15 min |
| [MONGODB_IMPLEMENTATION_GUIDE.md](MONGODB_IMPLEMENTATION_GUIDE.md) | Technical implementation details | 30 min |
| [HEROKU_DEPLOYMENT_GUIDE.md](HEROKU_DEPLOYMENT_GUIDE.md) | Deploy to Heroku (free hosting) | 1 hour |

---

## ✅ What Changed

### New Files
- `db/mongodb_client.py` - MongoDB connection manager
- `db/__init__.py` - Database package
- `init_mongodb.py` - Database initialization script
- `test_mongodb_connection.py` - Connection test
- `Procfile` - Heroku deployment
- `runtime.txt` - Python version
- `.env.example` - Environment template

### Modified Files
- `config.py` - Added MongoDB settings
- `app/app.py` - Added MongoDB logging
- `services/threat_intel.py` - MongoDB-backed blacklist
- `requirements.txt` - Added new dependencies

---

## 🔄 Features Added

✅ **MongoDB Logging**
- All predictions logged to MongoDB
- Query prediction history
- Generate statistics

✅ **Threat Intelligence**
- Blacklist now stored in MongoDB
- Can add/remove domains dynamically
- Cached for performance

✅ **API Enhancements**
- `/health` - Check app status
- `/stats` - Get prediction statistics
- Better error handling

✅ **Production Ready**
- Environment-based configuration
- Connection pooling
- Error handling & graceful degradation
- Heroku deployment support

---

## 🐛 Troubleshooting

### MongoDB Connection Failed
```
Issue: "Connection refused"
Solution:
1. Check IP is whitelisted in MongoDB Atlas
2. Verify MONGODB_URI has correct password
3. Run: python test_mongodb_connection.py
```

### Model Not Loading
```
Issue: "Model files not found"
Solution:
1. Train model: python ml/train_model.py
2. Verify models/ directory has .pkl files
```

### Module Not Found
```
Issue: "No module named 'pymongo'"
Solution:
pip install -r requirements.txt
```

---

## 📊 Database Collections

### predictions
Stores all URL predictions with confidence scores

### phishing_domains  
Stores blacklist of known phishing domains

### app_config
Application settings and metadata

---

## 🚢 Deployment Options

### Option 1: Local Development
```bash
python app/app.py
# Runs on http://localhost:5000
```

### Option 2: Heroku (Free)
```bash
# See HEROKU_DEPLOYMENT_GUIDE.md for detailed steps
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: Other Platforms
- Railway
- Render
- PythonAnywhere
- Google Cloud Run
- AWS

---

## 📝 API Examples

### Single Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Batch Prediction
```bash
curl -X POST http://localhost:5000/batch-predict \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example1.com", "https://example2.com"]}'
```

### Check Status
```bash
curl http://localhost:5000/health
```

### Get Statistics
```bash
curl http://localhost:5000/stats
```

---

## 🔐 Security

- ✓ Never commit `.env` to git
- ✓ Use strong database passwords
- ✓ Enable IP whitelisting
- ✓ Rotate credentials periodically
- ✓ Enable automated backups
- ✓ Monitor access logs

---

## 📞 Support

If you encounter issues:

1. **Check Logs:**
   ```bash
   python test_mongodb_connection.py
   ```

2. **Read Documentation:**
   - Quick reference: `MONGODB_QUICK_REFERENCE.md`
   - Complete guide: `MONGODB_ATLAS_DEPLOYMENT.md`

3. **Verify Setup:**
   - MongoDB Atlas console
   - Check `.env` file
   - Verify IP whitelisting

4. **Resources:**
   - [MongoDB Documentation](https://docs.mongodb.com/)
   - [PyMongo Documentation](https://pymongo.readthedocs.io/)
   - [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🎯 Next Steps

1. ✅ Complete the 5-minute quick start above
2. 📖 Read the detailed deployment guide
3. 🧪 Test all API endpoints
4. 🚢 Deploy to your hosting platform
5. 📊 Monitor predictions and statistics

---

## ⚡ Performance Tips

- MongoDB connection pooling is automatic
- Phishing domains are cached in memory
- Use batch predictions for multiple URLs
- Archive old predictions monthly
- Enable indexes (done automatically)

---

## 📈 Scaling

**Free Tier (M0):**
- 512MB storage
- 100,000 reads/writes per month
- Good for development/testing

**Growth (M2 - $9/month):**
- 2GB storage
- More throughput
- Better for small production

**Production (M5+ - $57+/month):**
- 10GB+ storage
- Enterprise features
- Automatic backup & recovery

---

**Last Updated:** May 24, 2026  
**Status:** Production Ready ✓

