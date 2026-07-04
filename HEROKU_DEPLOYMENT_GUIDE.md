# Heroku Deployment Guide

## Complete Guide to Deploy Phishing Detector on Heroku

Heroku is a cloud platform that makes it easy to deploy and run applications. This guide covers deploying your phishing detector with MongoDB Atlas backend.

---

## Prerequisites

1. **Heroku Account**: https://www.heroku.com (free tier available)
2. **Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
3. **Git**: https://git-scm.com/
4. **MongoDB Atlas Setup**: Complete [MONGODB_ATLAS_DEPLOYMENT.md](MONGODB_ATLAS_DEPLOYMENT.md) first

---

## Step-by-Step Deployment

### Step 1: Install Heroku CLI

**Windows:**
```bash
# Download installer from: https://cli-assets.heroku.com/heroku-x64.exe
# Or use choco:
choco install heroku-cli
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

Verify installation:
```bash
heroku --version
```

### Step 2: Initialize Git Repository

```bash
cd d:\Downloads\phishing-detector

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Phishing Detector with MongoDB"
```

### Step 3: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create new app (choose unique name)
heroku create your-phishing-app

# Or use existing app
heroku apps:create your-phishing-app --region us
```

**Output:**
```
Creating ⬢ your-phishing-app... done
https://your-phishing-app.herokuapp.com/ | https://git.heroku.com/your-phishing-app.git
```

Save the app name and Heroku git URL.

### Step 4: Create Required Files

#### Create `Procfile`
```
web: gunicorn app.app:app
```

#### Create `runtime.txt`
```
python-3.9.16
```

#### Update `requirements.txt`
Ensure it includes:
```
Flask>=2.3.0
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
pymongo>=4.0.0
python-dotenv>=0.19.0
werkzeug>=2.3.0
requests>=2.28.0
gunicorn>=20.1.0
```

### Step 5: Set Environment Variables

Set your MongoDB credentials on Heroku (never in .env):

```bash
# Set MongoDB URI
heroku config:set MONGODB_URI="mongodb+srv://phishing_app_user:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# Set Flask environment
heroku config:set FLASK_ENV="production"

# Set Secret Key (generate a random one)
heroku config:set SECRET_KEY="your-random-secret-key-here-make-it-long"

# Disable debug mode
heroku config:set DEBUG="False"

# Enable MongoDB logging
heroku config:set USE_MONGODB_LOGGING="True"
```

Verify configuration:
```bash
heroku config
```

### Step 6: Commit and Deploy

```bash
# Add new files
git add Procfile runtime.txt

# Commit all changes
git commit -m "Add Heroku deployment files"

# Deploy to Heroku
git push heroku main
```

If using `master` branch:
```bash
git push heroku master
```

### Step 7: Initialize MongoDB Collections

```bash
# Run the initialization script on Heroku
heroku run python init_mongodb.py
```

You should see:
```
Running python init_mongodb.py on ⬢ your-phishing-app... up, run.xxxx
============================================================
MongoDB Atlas Initialization Script
============================================================
1. Connecting to MongoDB Atlas...
   ✓ Connected successfully!
...
```

### Step 8: Test Deployment

```bash
# Check app logs
heroku logs --tail

# Health check
heroku open /health

# Or manually test
curl https://your-phishing-app.herokuapp.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "mongodb_connected": true
}
```

---

## Common Heroku Commands

### Logs and Monitoring

```bash
# View logs
heroku logs

# View logs in real-time
heroku logs --tail

# View logs for a specific dyno
heroku logs --dyno=web.1

# Download all logs
heroku logs > app.log
```

### Configuration

```bash
# Set environment variable
heroku config:set VAR_NAME="value"

# View all config
heroku config

# Remove config variable
heroku config:unset VAR_NAME
```

### Dyno Management

```bash
# View running dynos
heroku ps

# Restart app
heroku restart

# Scale dynos (free tier limited to 1)
heroku ps:scale web=2
heroku ps:scale web=1  # Scale down
```

### Database

```bash
# Run one-off command
heroku run python -c "from db import get_prediction_stats; print(get_prediction_stats())"

# Run bash shell
heroku run bash
```

### Deployment

```bash
# View deployment history
heroku releases

# Rollback to previous deployment
heroku rollback v5

# Check status
heroku status
```

---

## Monitoring and Maintenance

### Enable Papertrail (Free Log Aggregation)

```bash
# Add Papertrail to your app (free plan available)
heroku addons:create papertrail

# View in dashboard
heroku addons:open papertrail
```

### Monitor Performance

```bash
# View app metrics
heroku metrics

# View dyno metrics
heroku metrics --dyno=web.1
```

### Enable Application Performance Monitoring

```bash
# Add New Relic (free tier)
heroku addons:create newrelic:wayne

# View in dashboard
heroku addons:open newrelic
```

---

## Troubleshooting

### App Won't Start

```bash
# Check logs for errors
heroku logs --tail

# Common issues:
# - Model files not found
# - MongoDB connection failed
# - Missing environment variables
```

**Solution: Check requirements.txt and environment variables**

### Model Files Not Found

```
ERROR: Model files not found
```

**Solution:**
1. Upload model files to repository
2. Or train model on Heroku:
```bash
heroku run python ml/train_model.py
```

### MongoDB Connection Failed

```
✗ Connection failed: [Errno -2] Name or service not known
```

**Solution:**
1. Verify `MONGODB_URI` is set correctly
2. Check IP whitelist in MongoDB Atlas
3. Verify password has no special characters (or URL encode them)

### Out of Memory

```
Error: Dyno could not allocate memory
```

**Solution:**
- Upgrade to paid dyno: `heroku dyno:type standard`
- Reduce prediction batch size
- Archive old predictions from MongoDB

### Cold Start Issues

Heroku free tier sleeps after 30 minutes of inactivity.

**Solution: Use Paid Dyno or Uptime Monitoring**
```bash
# Upgrade to Eco ($5/month)
heroku dyno:type ecco --app your-app

# Or use free uptime monitor service to prevent sleeping
```

---

## Cost Optimization

### Free Tier Limitations
- 550 dyno hours/month (free tier)
- 512MB RAM per dyno
- Sleeps after 30 min inactivity
- Limited to 1 dyno

### Recommended Setup (Monthly Cost)

**Development:**
- Free tier Heroku dyno
- Free MongoDB Atlas cluster
- **Total: $0/month**

**Production:**
- Eco dyno ($5/month)
- M2 MongoDB Atlas ($9/month)
- **Total: ~$14/month**

---

## Best Practices

### 1. Environment Management
```bash
# Never hardcode secrets
# Always use environment variables

# ❌ WRONG
MONGODB_URI="mongodb+srv://user:pass@..."

# ✅ CORRECT
MONGODB_URI = os.environ.get('MONGODB_URI')
```

### 2. Logging
```bash
# Use Heroku's structured logging
# Avoid excessive logging (counts against dyno time)

logger.info("Important event")  # Use sparingly
logger.debug("Debug info")      # Only when needed
```

### 3. Database Queries
```bash
# Use indexes (created by init_mongodb.py)
# Cache frequently accessed data
# Archive old predictions monthly

# View index usage
db.predictions.getIndexes()
```

### 4. Error Handling
```bash
# Monitor error rates
# Set up alerts on critical errors
# Log all exceptions with context
```

### 5. Security
- ✓ Use strong database passwords
- ✓ Keep `MONGODB_URI` secret
- ✓ Don't commit `.env` file
- ✓ Rotate secrets periodically
- ✓ Use HTTPS only

---

## Deployment Checklist

- [ ] Heroku CLI installed and logged in
- [ ] Git repository initialized
- [ ] `Procfile` created
- [ ] `runtime.txt` created
- [ ] `requirements.txt` updated with gunicorn
- [ ] Heroku app created
- [ ] Environment variables set
- [ ] MongoDB initialized on Heroku
- [ ] App deployed successfully
- [ ] Health check endpoint working
- [ ] MongoDB connection verified
- [ ] Model files present
- [ ] Logs configured
- [ ] Monitoring enabled

---

## Next Steps

### Add Custom Domain
```bash
heroku domains:add www.yourdomain.com
```

### Enable HTTPS
```bash
# Free HTTPS is automatic with Heroku
# Verify in dashboard
```

### Continuous Deployment
```bash
# Connect GitHub repo for auto-deployment
heroku git:remote -a your-phishing-app
```

### Backup Database
```bash
# MongoDB Atlas handles automatic backups
# View in MongoDB Atlas console
```

---

## Alternative Hosting Platforms

If Heroku doesn't meet your needs:

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Railway** | Limited free | Simple Python apps |
| **Render** | Limited free | Reliable deployments |
| **PythonAnywhere** | Free tier | Python-specific |
| **AWS EC2** | 1 year free | Complex setups |
| **Google Cloud Run** | Free tier | Serverless |
| **Azure** | $200 credit | Enterprise |

---

## Support Resources

- [Heroku Documentation](https://devcenter.heroku.com/)
- [Heroku CLI Reference](https://devcenter.heroku.com/articles/heroku-cli)
- [Heroku Buildpacks](https://devcenter.heroku.com/articles/buildpacks)
- [Common Errors and Solutions](https://devcenter.heroku.com/articles/troubleshooting-node-deploys)
- [Main Deployment Guide](MONGODB_ATLAS_DEPLOYMENT.md)

