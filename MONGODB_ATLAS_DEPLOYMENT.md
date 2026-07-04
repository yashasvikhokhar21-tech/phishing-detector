# MongoDB Atlas Deployment Guide

## Step-by-Step Process to Deploy Phishing Detector on MongoDB Atlas

### PHASE 1: MongoDB Atlas Setup

#### Step 1: Create a MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Start Free" or "Try Free"
3. Sign up with email, Google, or GitHub account
4. Verify your email address

#### Step 2: Create a Free Cluster
1. After login, click "Create a Cluster"
2. Choose **Free Tier** (M0 - fully free, adequate for testing)
3. Select your preferred **Cloud Provider** (AWS, GCP, or Azure)
4. Select **Region** closest to your deployment location
5. Click "Create Deployment"
6. Wait 1-2 minutes for cluster to initialize

#### Step 3: Create a Database User
1. Go to **Database Access** in the left sidebar
2. Click **"Add New Database User"**
3. Enter:
   - **Username**: `phishing_app_user`
   - **Password**: Generate a strong password and **save it**
   - **Built-in Role**: Select **"Read and write to any database"**
4. Click **"Add User"**

#### Step 4: Configure Network Access
1. Go to **Network Access** in the left sidebar
2. Click **"Add IP Address"**
3. Options:
   - **For Development**: Click "Allow Access from Anywhere" (0.0.0.0/0)
   - **For Production**: Add your specific server IP address
4. Click **"Confirm"**

#### Step 5: Get Connection String
1. Go back to **Clusters**
2. Click **"Connect"** on your cluster
3. Choose **"Drivers"** (not "MongoDB Compass")
4. Select **Python** and version **3.6 or later**
5. Copy the **connection string** that looks like:
   ```
   mongodb+srv://phishing_app_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual password
7. **Save this connection string securely**

---

### PHASE 2: Local Development Setup

#### Step 6: Update Python Requirements
Run in your project directory:
```bash
pip install pymongo python-dotenv
```

Or update `requirements.txt` with:
```
pymongo>=4.0.0
python-dotenv>=0.19.0
```

#### Step 7: Create Environment Configuration
Create `.env` file in your project root:
```env
# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://phishing_app_user:your_password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=phishing_detector
MONGODB_COLLECTION_PREDICTIONS=predictions
MONGODB_COLLECTION_BLACKLIST=phishing_domains
MONGODB_COLLECTION_CONFIG=app_config

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DEBUG=False
```

**Important**: Never commit `.env` to git!

#### Step 8: Create `.env.example`
Create `.env.example` for documentation:
```env
# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=phishing_detector
MONGODB_COLLECTION_PREDICTIONS=predictions
MONGODB_COLLECTION_BLACKLIST=phishing_domains
MONGODB_COLLECTION_CONFIG=app_config

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=change-this-to-your-secret-key
DEBUG=False
```

#### Step 9: Test MongoDB Connection Locally
Create `test_mongodb_connection.py`:
```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.environ.get('MONGODB_URI')
try:
    client = MongoClient(uri)
    # Ping the database to verify connection
    client.admin.command('ping')
    print("✓ MongoDB Atlas connection successful!")
    print(f"✓ Databases: {client.list_database_names()}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

Run:
```bash
python test_mongodb_connection.py
```

---

### PHASE 3: Code Modifications

All code files have been modified to support MongoDB. See the following sections for details on which files were changed:

#### Modified Files:
1. `config.py` - Added MongoDB configuration
2. `app/app.py` - Integrated MongoDB logging
3. `services/threat_intel.py` - MongoDB blacklist storage
4. `requirements.txt` - Added pymongo and python-dotenv
5. Created `db/mongodb_client.py` - MongoDB connection manager

#### New Files:
1. `.env.example` - Environment variables template
2. `db/mongodb_client.py` - MongoDB utility functions
3. `INIT_MONGODB.md` - Database initialization guide

---

### PHASE 4: Initialize MongoDB Collections

#### Step 10: Initialize Database Collections
Run this script once to create collections and indexes:
```bash
python init_mongodb.py
```

Or manually in MongoDB Atlas:

1. Go to **Collections** tab
2. Create collections:
   - `predictions` - For storing prediction logs
   - `phishing_domains` - For blacklist
   - `app_config` - For application settings

3. Create indexes for better performance:
   ```javascript
   // In MongoDB Atlas Web Shell
   db.predictions.createIndex({ "timestamp": -1 });
   db.predictions.createIndex({ "url": 1 });
   db.phishing_domains.createIndex({ "domain": 1 });
   ```

---

### PHASE 5: Deployment (Heroku Example)

#### Step 11: Prepare for Cloud Deployment

**For Heroku:**

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. Create `Procfile`:
   ```
   web: gunicorn app.app:app
   ```

3. Create `runtime.txt`:
   ```
   python-3.9.16
   ```

4. Update `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

5. Initialize git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

6. Create Heroku app:
   ```bash
   heroku login
   heroku create your-app-name
   ```

7. Set environment variables on Heroku:
   ```bash
   heroku config:set MONGODB_URI="your_mongodb_atlas_uri"
   heroku config:set FLASK_ENV="production"
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG="False"
   ```

8. Deploy to Heroku:
   ```bash
   git push heroku main
   ```

9. View logs:
   ```bash
   heroku logs --tail
   ```

---

### PHASE 6: Monitoring and Maintenance

#### Step 12: Monitor Your Application

**In MongoDB Atlas:**
1. Go to **Metrics** to view database performance
2. Go to **Alerts** to set up notifications
3. Use **MongoDB Charts** to visualize prediction data
4. Regularly check **Activity** logs

**Useful MongoDB Queries:**

View recent predictions:
```javascript
db.predictions.find().sort({ timestamp: -1 }).limit(10)
```

Count predictions by result:
```javascript
db.predictions.aggregate([
  { $group: { _id: "$prediction_result", count: { $sum: 1 } } }
])
```

View blacklist:
```javascript
db.phishing_domains.find()
```

Add new domain to blacklist:
```javascript
db.phishing_domains.insertOne({ domain: "evil-domain.com", added_date: new Date() })
```

---

### PHASE 7: Backup and Security

#### Step 13: Enable Automated Backups
1. Go to **Backup** in MongoDB Atlas
2. Click **Enable Backup**
3. Configure backup schedule (defaults are recommended)
4. MongoDB Atlas automatically backs up your data

#### Step 14: Security Best Practices
1. ✓ Use strong passwords (MongoDB already required this)
2. ✓ Enable IP whitelisting (done in Step 4)
3. ✓ Use environment variables for sensitive data
4. ✓ Never commit `.env` to version control
5. ✓ Enable MongoDB encryption at rest (enabled by default)
6. ✓ Enable TLS/SSL (required by default for MongoDB Atlas)

---

## Troubleshooting

### Connection Issues

**Error: "Unable to connect to MongoDB Atlas"**
- Verify IP address is whitelisted in Network Access
- Check username and password are correct
- Ensure connection string is properly formatted
- Check internet connection

**Error: "Authentication failed"**
- Verify database username and password
- Ensure password doesn't contain special characters that need URL encoding
- Try recreating the database user

### Deployment Issues

**Heroku: "ModuleNotFoundError: No module named 'pymongo'"**
- Ensure `requirements.txt` includes `pymongo`
- Run `git push heroku main` again

**Heroku: "Cannot import .env"**
- Set environment variables using `heroku config:set`
- Don't rely on `.env` file in production

---

## Performance Optimization

### For Large Scale Deployment:

1. **Use Connection Pooling** (already in `db/mongodb_client.py`)
2. **Create Indexes** on frequently queried fields
3. **Archive Old Predictions** periodically
4. **Upgrade to Paid Tier** if approaching limits:
   - M0 (Free): 512MB storage
   - M2 (Paid): 2GB storage, ~$9/month
   - M5 (Paid): 10GB storage, ~$57/month

### Sample Archival Script:

```python
from datetime import datetime, timedelta

def archive_old_predictions(db, days=90):
    """Archive predictions older than specified days"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Move to archive collection
    result = db.predictions.delete_many({
        "timestamp": {"$lt": cutoff_date}
    })
    print(f"Archived {result.deleted_count} old predictions")
```

---

## Summary Checklist

- [ ] MongoDB Atlas account created
- [ ] Free cluster created and initialized
- [ ] Database user created
- [ ] Network access configured
- [ ] Connection string obtained
- [ ] `.env` file created with connection string
- [ ] Python requirements installed
- [ ] Local connection tested
- [ ] Code modifications implemented
- [ ] Collections initialized
- [ ] Application tested locally
- [ ] Cloud deployment configured (Heroku/other)
- [ ] Environment variables set on cloud platform
- [ ] Application deployed
- [ ] Backups enabled
- [ ] Monitoring configured

---

## Additional Resources

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Heroku Deployment Guide](https://devcenter.heroku.com/)
- [MongoDB Security Checklist](https://docs.mongodb.com/manual/administration/security-checklist/)

