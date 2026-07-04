"""
Threat Intelligence Module for Phishing Detection

This module provides threat intelligence capabilities by maintaining
a blacklist of known phishing domains and checking URLs against it.
Now integrated with MongoDB Atlas for scalable blacklist management.
"""

from urllib.parse import urlparse
from typing import Dict, Union
import logging
import os

# Try to import MongoDB, fall back to in-memory storage if not available
try:
    from db.mongodb_client import get_phishing_domains, add_phishing_domain, remove_phishing_domain
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    # Fallback: in-memory blacklist
    PHISHING_DOMAINS = {
        "paypal-secure-login.com",
        "bankofamerica-login.net",
        "amazon-security-alert.org",
        "microsoft-support-help.com",
        "google-account-recovery.net",
        "facebook-security-check.org",
        "apple-id-verification.com",
        "netflix-account-update.net",
        "linkedin-password-reset.org",
        "twitter-suspension-alert.com",
        "chase-bank-verify.com",
        "wellsfargo-secure.net",
        "ebay-account-protection.org",
        "instagram-support-help.com",
        "yahoo-mail-recovery.net",
        "outlook-security-alert.org",
        "dropbox-file-share.com",
        "github-account-verify.net",
        "slack-workspace-update.org",
        "zoom-meeting-security.com"
    }

logger = logging.getLogger(__name__)

# Cache for phishing domains to reduce database queries
_domains_cache = None
_cache_initialized = False


def _get_cached_domains() -> set:
    """
    Get cached phishing domains, loading from MongoDB if available
    
    Returns:
        set: Set of phishing domains
    """
    global _domains_cache, _cache_initialized
    
    if _cache_initialized and _domains_cache is not None:
        return _domains_cache
    
    if MONGODB_AVAILABLE:
        try:
            _domains_cache = get_phishing_domains()
            _cache_initialized = True
            logger.debug(f"Loaded {len(_domains_cache)} domains from MongoDB")
            return _domains_cache
        except Exception as e:
            logger.warning(f"Failed to load domains from MongoDB: {e}. Using fallback.")
    
    # Fallback to in-memory list
    _domains_cache = PHISHING_DOMAINS.copy() if not MONGODB_AVAILABLE else set()
    _cache_initialized = True
    return _domains_cache


def extract_domain(url: str) -> str:
    """
    Extract the domain (hostname) from a URL.

    Args:
        url (str): The URL to parse

    Returns:
        str: The domain/hostname, or empty string if invalid
    """
    try:
        # Ensure URL has a scheme for proper parsing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed = urlparse(url)
        return parsed.hostname or ""
    except Exception:
        return ""


def check_threat_intelligence(url: str) -> Dict[str, Union[bool, float, str]]:
    """
    Check if a URL's domain is in the threat intelligence blacklist.

    Args:
        url (str): The URL to check

    Returns:
        Dict containing:
        - blacklisted (bool): True if domain is in blacklist
        - score (float): 1.0 if blacklisted, 0.0 otherwise
        - reason (str): Reason message if blacklisted, empty otherwise
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")

    domain = extract_domain(url.strip())

    if not domain:
        return {
            "blacklisted": False,
            "score": 0.0,
            "reason": ""
        }

    # Get cached domains
    phishing_domains = _get_cached_domains()

    # Case-insensitive check
    is_blacklisted = domain.lower() in phishing_domains

    return {
        "blacklisted": is_blacklisted,
        "score": 1.0 if is_blacklisted else 0.0,
        "reason": "Domain found in threat intelligence database" if is_blacklisted else ""
    }


def add_to_blacklist(domain: str) -> bool:
    """
    Add a domain to the blacklist (for administrative purposes).
    Updates both MongoDB and local cache.

    Args:
        domain (str): Domain to add

    Returns:
        bool: True if added, False if already exists
    """
    domain = domain.lower().strip()
    
    if not domain:
        return False
    
    domains = _get_cached_domains()
    
    if domain in domains:
        logger.debug(f"Domain already in blacklist: {domain}")
        return False
    
    # Add to MongoDB if available
    if MONGODB_AVAILABLE:
        try:
            result = add_phishing_domain(domain)
            if result:
                domains.add(domain)
                logger.info(f"Domain added to blacklist (MongoDB): {domain}")
                return True
        except Exception as e:
            logger.warning(f"Failed to add domain to MongoDB: {e}")
    
    # Fallback: add to in-memory list
    domains.add(domain)
    logger.info(f"Domain added to blacklist (memory): {domain}")
    return True


def remove_from_blacklist(domain: str) -> bool:
    """
    Remove a domain from the blacklist (for administrative purposes).
    Updates both MongoDB and local cache.

    Args:
        domain (str): Domain to remove

    Returns:
        bool: True if removed, False if not found
    """
    domain = domain.lower().strip()
    
    domains = _get_cached_domains()
    
    if domain not in domains:
        logger.debug(f"Domain not found in blacklist: {domain}")
        return False
    
    # Remove from MongoDB if available
    if MONGODB_AVAILABLE:
        try:
            result = remove_phishing_domain(domain)
            if result:
                domains.discard(domain)
                logger.info(f"Domain removed from blacklist (MongoDB): {domain}")
                return True
        except Exception as e:
            logger.warning(f"Failed to remove domain from MongoDB: {e}")
    
    # Fallback: remove from in-memory list
    domains.discard(domain)
    logger.info(f"Domain removed from blacklist (memory): {domain}")
    return True


def get_blacklist_size() -> int:
    """
    Get the number of domains in the blacklist.

    Returns:
        int: Number of blacklisted domains
    """
    domains = _get_cached_domains()
    return len(domains)


def is_domain_blacklisted(domain: str) -> bool:
    """
    Check if a specific domain is blacklisted.

    Args:
        domain (str): Domain to check

    Returns:
        bool: True if blacklisted
    """
    domains = _get_cached_domains()
    return domain.lower().strip() in domains


def refresh_cache() -> bool:
    """
    Refresh the domains cache from MongoDB.
    Useful when external updates have been made to the blacklist.

    Returns:
        bool: True if refreshed successfully
    """
    global _domains_cache, _cache_initialized
    
    _domains_cache = None
    _cache_initialized = False
    
    try:
        _get_cached_domains()
        logger.info("Domains cache refreshed")
        return True
    except Exception as e:
        logger.error(f"Failed to refresh cache: {e}")
        return False