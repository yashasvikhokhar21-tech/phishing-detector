"""
MongoDB Client and Connection Manager
Handles all MongoDB Atlas interactions
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Singleton MongoDB client manager"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """
        Connect to MongoDB Atlas
        
        Raises:
            ConnectionFailure: If unable to connect
        """
        try:
            uri = os.environ.get('MONGODB_URI')
            if not uri:
                raise ValueError("MONGODB_URI not found in environment variables")
            
            # Create client with connection pooling and timeout
            self._client = MongoClient(
                uri,
                connectTimeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                retryWrites=True
            )
            
            # Verify connection
            self._client.admin.command('ping')
            
            db_name = os.environ.get('MONGODB_DB_NAME', 'phishing_detector')
            self._db = self._client[db_name]
            
            logger.info("✓ Successfully connected to MongoDB Atlas")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"✗ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Unexpected error connecting to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Disconnected from MongoDB Atlas")
    
    @property
    def db(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    @property
    def client(self):
        """Get client instance"""
        if self._client is None:
            self.connect()
        return self._client
    
    def get_collection(self, collection_name: str):
        """
        Get a specific collection
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            pymongo.collection.Collection
        """
        return self.db[collection_name]
    
    def create_indexes(self):
        """Create necessary indexes for optimal query performance"""
        try:
            # Predictions collection indexes
            predictions = self.get_collection('predictions')
            predictions.create_index('timestamp')
            predictions.create_index('url')
            predictions.create_index([('timestamp', -1)])  # For sorting
            
            # Phishing domains collection indexes
            domains = self.get_collection('phishing_domains')
            domains.create_index('domain')
            
            logger.info("✓ Database indexes created successfully")
            return True
        except Exception as e:
            logger.error(f"✗ Error creating indexes: {e}")
            return False
    
    def health_check(self) -> bool:
        """
        Check MongoDB connection health
        
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            self._client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"✗ Health check failed: {e}")
            return False


def get_mongodb_client() -> MongoDBClient:
    """
    Get the MongoDB client singleton
    
    Returns:
        MongoDBClient: The MongoDB client instance
    """
    return MongoDBClient()


# Collection helper functions
def log_prediction(url: str, prediction_result: str, confidence: float, 
                   threat_intel_result: dict, rule_based_result: dict,
                   user_ip: Optional[str] = None) -> bool:
    """
    Log a prediction to MongoDB
    
    Args:
        url (str): The URL analyzed
        prediction_result (str): 'phishing' or 'legitimate'
        confidence (float): Prediction confidence
        threat_intel_result (dict): Threat intelligence check result
        rule_based_result (dict): Rule-based detection result
        user_ip (str): Optional user IP address
        
    Returns:
        bool: True if logged successfully
    """
    try:
        client = get_mongodb_client()
        predictions = client.get_collection('predictions')
        
        document = {
            'timestamp': datetime.utcnow(),
            'url': url,
            'prediction_result': prediction_result,
            'confidence': float(confidence),
            'threat_intel_result': threat_intel_result,
            'rule_based_result': rule_based_result,
            'user_ip': user_ip
        }
        
        result = predictions.insert_one(document)
        logger.info(f"Prediction logged: {result.inserted_id}")
        return True
    except Exception as e:
        logger.error(f"Error logging prediction: {e}")
        return False


def get_phishing_domains() -> set:
    """
    Get all phishing domains from MongoDB
    
    Returns:
        set: Set of phishing domains
    """
    try:
        client = get_mongodb_client()
        domains_collection = client.get_collection('phishing_domains')
        
        domains = set()
        for doc in domains_collection.find({}, {'domain': 1}):
            if 'domain' in doc:
                domains.add(doc['domain'].lower())
        
        logger.info(f"Loaded {len(domains)} phishing domains from MongoDB")
        return domains
    except Exception as e:
        logger.error(f"Error fetching phishing domains: {e}")
        return set()


def add_phishing_domain(domain: str) -> bool:
    """
    Add a domain to the phishing blacklist
    
    Args:
        domain (str): Domain to add
        
    Returns:
        bool: True if added successfully
    """
    try:
        client = get_mongodb_client()
        domains_collection = client.get_collection('phishing_domains')
        
        result = domains_collection.update_one(
            {'domain': domain.lower()},
            {
                '$set': {
                    'domain': domain.lower(),
                    'added_date': datetime.utcnow(),
                    'status': 'active'
                }
            },
            upsert=True
        )
        
        logger.info(f"Domain added to blacklist: {domain}")
        return True
    except Exception as e:
        logger.error(f"Error adding domain: {e}")
        return False


def remove_phishing_domain(domain: str) -> bool:
    """
    Remove a domain from the phishing blacklist
    
    Args:
        domain (str): Domain to remove
        
    Returns:
        bool: True if removed successfully
    """
    try:
        client = get_mongodb_client()
        domains_collection = client.get_collection('phishing_domains')
        
        result = domains_collection.delete_one({'domain': domain.lower()})
        
        if result.deleted_count > 0:
            logger.info(f"Domain removed from blacklist: {domain}")
            return True
        else:
            logger.warning(f"Domain not found: {domain}")
            return False
    except Exception as e:
        logger.error(f"Error removing domain: {e}")
        return False


def get_prediction_stats(limit_days: int = 30) -> dict:
    """
    Get prediction statistics from the past N days
    
    Args:
        limit_days (int): Number of days to analyze
        
    Returns:
        dict: Statistics including total, phishing, and legitimate counts
    """
    try:
        from datetime import timedelta
        
        client = get_mongodb_client()
        predictions = client.get_collection('predictions')
        
        cutoff_date = datetime.utcnow() - timedelta(days=limit_days)
        
        # Count by prediction result
        stats = predictions.aggregate([
            {
                '$match': {
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': '$prediction_result',
                    'count': {'$sum': 1},
                    'avg_confidence': {'$avg': '$confidence'}
                }
            }
        ])
        
        result = {'total': 0, 'phishing': 0, 'legitimate': 0, 'avg_confidence': 0}
        
        for stat in stats:
            prediction_type = stat['_id']
            count = stat['count']
            result['total'] += count
            result[prediction_type] = count
            result['avg_confidence'] = stat['avg_confidence']
        
        return result
    except Exception as e:
        logger.error(f"Error getting prediction stats: {e}")
        return {'total': 0, 'phishing': 0, 'legitimate': 0}
