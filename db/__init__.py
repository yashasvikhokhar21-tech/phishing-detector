"""Database module for MongoDB integration"""

from .mongodb_client import (
    MongoDBClient,
    get_mongodb_client,
    log_prediction,
    get_phishing_domains,
    add_phishing_domain,
    remove_phishing_domain,
    get_prediction_stats
)

__all__ = [
    'MongoDBClient',
    'get_mongodb_client',
    'log_prediction',
    'get_phishing_domains',
    'add_phishing_domain',
    'remove_phishing_domain',
    'get_prediction_stats'
]
