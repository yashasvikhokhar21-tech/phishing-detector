# MongoDB Atlas Quick Reference Guide

## Quick Setup (5 Minutes)

### 1. Create MongoDB Atlas Account
```bash
# Visit: https://www.mongodb.com/cloud/atlas
# Sign up → Create Free Cluster
# Location: Choose closest region
# Wait 1-2 minutes for initialization
```

### 2. Create Database User
- Navigate to **Database Access**
- Click **Add New Database User**
- Username: `phishing_app_user`
- Password: Generate strong password (save it!)
- Role: Read and write to any database

### 3. Configure Network
- Go to **Network Access**
- Click **Add IP Address**
- For testing: **Allow from Anywhere** (0.0.0.0/0)
- For production: Add specific IP

### 4. Get Connection String
- Click **Connect** on your cluster
- Select **Drivers**
- Choose Python 3.6+
- Copy connection string
- Replace `<password>` with your actual password

Connection string format:
```
mongodb+srv://phishing_app_user:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 5. Create .env File
```bash
# In project root directory
cp .env.example .env

# Edit .env and replace:
# - MONGODB_URI with your connection string
# - SECRET_KEY with a random string
```

### 6. Install Dependencies
```bash
pip install -r requirements.txt
```

### 7. Initialize Database
```bash
python init_mongodb.py
```

### 8. Test Connection
```bash
python test_mongodb_connection.py
```

### 9. Run Application
```bash
python app/app.py
```

---

## Common Commands

### MongoDB Operations

**Check MongoDB Connection:**
```python
from db import get_mongodb_client
client = get_mongodb_client()
print(client.health_check())
```

**View Predictions:**
```javascript
// In MongoDB Atlas Web Shell
db.predictions.find().sort({ timestamp: -1 }).limit(10)
```

**View Phishing Domains:**
```javascript
db.phishing_domains.find()
```

**Add Domain to Blacklist:**
```python
from db import add_phishing_domain
add_phishing_domain("evil-domain.com")
```

**Get Prediction Statistics:**
```python
from db import get_prediction_stats
stats = get_prediction_stats(limit_days=30)
print(stats)
```

### Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/predict` | POST | Single URL prediction |
| `/batch-predict` | POST | Batch URL predictions |
| `/health` | GET | Health check & status |
| `/stats` | GET | Prediction statistics |

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MONGODB_URI` | Required | MongoDB Atlas connection string |
| `MONGODB_DB_NAME` | phishing_detector | Database name |
| `FLASK_ENV` | production | Flask environment |
| `SECRET_KEY` | Required | Flask secret key |
| `DEBUG` | False | Debug mode |
| `USE_MONGODB_LOGGING` | True | Enable MongoDB logging |

---

## API Examples

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
  -d '{
    "urls": [
      "https://example1.com",
      "https://example2.com"
    ]
  }'
```

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Statistics
```bash
curl http://localhost:5000/stats
```

---

## Deployment Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] Network access configured
- [ ] Connection string obtained
- [ ] `.env` file created locally
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Database initialized: `python init_mongodb.py`
- [ ] Local testing passed
- [ ] `.env` configured for production
- [ ] `requirements.txt` updated
- [ ] Code deployed to cloud
- [ ] Environment variables set on cloud platform
- [ ] Health check endpoint working
- [ ] Predictions logging to MongoDB
- [ ] Monitoring configured

---

## Troubleshooting

### Connection Refused
```
Error: Couldn't connect to MongoDB Atlas
```
**Solution:**
- Verify IP is whitelisted in Network Access
- Check connection string has correct password
- Ensure `MONGODB_URI` is set in `.env`

### Authentication Failed
```
Error: authentication failed
```
**Solution:**
- Verify username and password
- Check special characters in password (URL encode if needed)
- Recreate the database user

### Module Not Found
```
ModuleNotFoundError: No module named 'pymongo'
```
**Solution:**
```bash
pip install pymongo>=4.0.0
```

### MongoDB Not Available
```
⚠ MongoDB module not available
```
**Solution:**
- Install pymongo: `pip install pymongo`
- App will use file logging as fallback

---

## Performance Tips

1. **Use Indexes**: Automatically created during `init_mongodb.py`
2. **Connection Pooling**: Enabled by default in `db/mongodb_client.py`
3. **Caching**: Domains blacklist cached in memory
4. **Batch Operations**: Use `/batch-predict` for multiple URLs
5. **Archive Old Data**: Remove predictions older than 90 days periodically

---

## Security Reminders

✓ Never commit `.env` to git  
✓ Use strong database passwords  
✓ Whitelist specific IPs in production  
✓ Enable MongoDB encryption (default)  
✓ Use environment variables for secrets  
✓ Enable backup and recovery  

---

## Support Resources

- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
- [PyMongo Docs](https://pymongo.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Project README](README.md)
- [Main Deployment Guide](MONGODB_ATLAS_DEPLOYMENT.md)

