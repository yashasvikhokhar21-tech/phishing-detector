"""
MongoDB Connection Test Script
Run this to verify your MongoDB Atlas connection is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("=" * 70)
print("MongoDB Atlas Connection Test")
print("=" * 70)

# Check if MONGODB_URI is set
mongodb_uri = os.environ.get('MONGODB_URI')

if not mongodb_uri:
    print("\n✗ MONGODB_URI not found in environment variables")
    print("\nTo set MONGODB_URI:")
    print("  1. Create a .env file in the project root")
    print("  2. Add: MONGODB_URI=your_connection_string")
    print("  3. Get connection string from MongoDB Atlas console")
    print("\nSee .env.example for template")
    sys.exit(1)

print("\n✓ MONGODB_URI found")
print(f"  Connection string: {mongodb_uri[:50]}...")

# Verify pymongo is installed
try:
    import pymongo
    print("✓ PyMongo installed")
except ImportError:
    print("\n✗ PyMongo not installed")
    print("  Run: pip install pymongo>=4.0.0")
    sys.exit(1)

# Try to connect
print("\nAttempting to connect to MongoDB Atlas...")

try:
    from pymongo import MongoClient
    
    client = MongoClient(
        mongodb_uri,
        connectTimeoutMS=5000,
        serverSelectionTimeoutMS=5000
    )
    
    # Ping the server
    client.admin.command('ping')
    print("✓ Successfully connected to MongoDB Atlas!")
    
    # Get database info
    db_name = os.environ.get('MONGODB_DB_NAME', 'phishing_detector')
    db = client[db_name]
    
    print(f"\n✓ Database: {db.name}")
    print(f"  Collections: {db.list_collection_names()}")
    
    # Check if our collections exist
    expected_collections = ['predictions', 'phishing_domains', 'app_config']
    for collection in expected_collections:
        if collection in db.list_collection_names():
            count = db[collection].count_documents({})
            print(f"  - {collection}: {count} documents")
        else:
            print(f"  - {collection}: NOT FOUND (run init_mongodb.py)")
    
    # Close connection
    client.close()
    
    print("\n" + "=" * 70)
    print("Connection test PASSED ✓")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run: python init_mongodb.py (if collections missing)")
    print("  2. Run: python app/app.py (to start the application)")
    print("  3. Visit: http://localhost:5000 in your browser")
    
    sys.exit(0)

except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    print("\n" + "=" * 70)
    print("Troubleshooting:")
    print("=" * 70)
    print("\n1. Check your IP address is whitelisted:")
    print("   - Go to MongoDB Atlas console")
    print("   - Network Access -> Add IP Address")
    print("   - Add: 0.0.0.0/0 (allow from anywhere)")
    
    print("\n2. Verify connection string format:")
    print("   Format: mongodb+srv://username:password@cluster.xxxxx.mongodb.net/")
    print("   - Replace <password> with actual password")
    print("   - No special characters in password (or URL encode them)")
    
    print("\n3. Check MongoDB Atlas cluster status:")
    print("   - Is cluster running?")
    print("   - Is network access configured?")
    print("   - Is IP whitelisted?")
    
    print("\n4. Try updating pymongo:")
    print("   pip install --upgrade pymongo")
    
    sys.exit(1)
