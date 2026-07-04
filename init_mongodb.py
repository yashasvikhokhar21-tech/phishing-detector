"""
MongoDB Atlas Initialization Script
Run this once to initialize your MongoDB database with collections and indexes
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import get_mongodb_client


def initialize_mongodb():
    """Initialize MongoDB collections and indexes"""
    
    print("=" * 60)
    print("MongoDB Atlas Initialization Script")
    print("=" * 60)
    
    try:
        # Get MongoDB client
        client = get_mongodb_client()
        
        print("\n1. Connecting to MongoDB Atlas...")
        try:
            if client.health_check():
                print("   ✓ Connected successfully!")
            else:
                print("   ✗ Connection check failed!")
                return False
        except Exception as e:
            print(f"   ✗ Connection error: {e}")
            return False
        
        db = client.db
        print(f"\n2. Using database: {db.name}")
        
        # Create collections
        print("\n3. Creating collections...")
        
        # Predictions collection
        if 'predictions' not in db.list_collection_names():
            db.create_collection('predictions')
            print("   ✓ Created 'predictions' collection")
        else:
            print("   - 'predictions' collection already exists")
        
        # Phishing domains collection
        if 'phishing_domains' not in db.list_collection_names():
            db.create_collection('phishing_domains')
            print("   ✓ Created 'phishing_domains' collection")
        else:
            print("   - 'phishing_domains' collection already exists")
        
        # App config collection
        if 'app_config' not in db.list_collection_names():
            db.create_collection('app_config')
            print("   ✓ Created 'app_config' collection")
        else:
            print("   - 'app_config' collection already exists")
        
        # Create indexes
        print("\n4. Creating indexes for better performance...")
        
        predictions = db['predictions']
        predictions.create_index('timestamp')
        predictions.create_index('url')
        predictions.create_index([('timestamp', -1)])
        print("   ✓ Indexes created on 'predictions' collection")
        
        domains = db['phishing_domains']
        domains.create_index('domain')
        print("   ✓ Indexes created on 'phishing_domains' collection")
        
        # Initialize phishing domains with seed data (optional)
        print("\n5. Initializing seed data...")
        
        seed_domains = [
            "paypal-secure-login.com",
            "bankofamerica-login.net",
            "amazon-security-alert.org",
            "microsoft-support-help.com",
            "google-account-recovery.net",
            "facebook-security-check.org",
            "apple-id-verification.com",
            "netflix-account-update.net",
            "linkedin-password-reset.org",
            "twitter-suspension-alert.com"
        ]
        
        domains_col = db['phishing_domains']
        existing_count = domains_col.count_documents({})
        
        if existing_count == 0:
            from datetime import datetime
            seed_docs = [
                {
                    'domain': domain,
                    'added_date': datetime.utcnow(),
                    'status': 'active'
                }
                for domain in seed_domains
            ]
            domains_col.insert_many(seed_docs)
            print(f"   ✓ Inserted {len(seed_docs)} seed phishing domains")
        else:
            print(f"   - Phishing domains already exist ({existing_count} domains)")
        
        # Print summary
        print("\n" + "=" * 60)
        print("Initialization Complete!")
        print("=" * 60)
        print(f"\nDatabase: {db.name}")
        print(f"Collections: {', '.join(db.list_collection_names())}")
        print(f"Phishing domains: {domains_col.count_documents({})}")
        print("\nYour MongoDB Atlas is ready for use!")
        print("\n" + "=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = initialize_mongodb()
    sys.exit(0 if success else 1)
