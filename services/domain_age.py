"""
Domain Age Checker Module for Phishing Detection

This module checks the age of domains to detect newly created,
suspicious domains commonly used in phishing attacks.
"""

from urllib.parse import urlparse
from typing import Dict, Union
from datetime import datetime, timedelta
import logging

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False
    logging.warning("whois library not installed. Domain age checking will be disabled.")


logger = logging.getLogger(__name__)


def extract_domain_name(url: str) -> str:
    """
    Extract the domain name from a URL.

    Args:
        url (str): The URL to parse

    Returns:
        str: The domain name, or empty string if invalid
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        parsed = urlparse(url)
        return parsed.netloc or ""
    except Exception:
        return ""


def get_domain_age_days(domain: str) -> Union[int, None]:
    """
    Get the age of a domain in days since creation.

    Args:
        domain (str): The domain name to check

    Returns:
        int: Age in days, or None if unable to determine
    """
    if not WHOIS_AVAILABLE:
        return None

    try:
        domain = domain.lower().strip()
        
        # Remove 'www.' prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Query WHOIS data
        whois_data = whois.whois(domain)
        
        # Extract creation date
        creation_date = whois_data.creation_date
        
        # Handle multiple creation dates (some WHOIS return list)
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if creation_date is None:
            return None
        
        # Calculate age
        current_date = datetime.now()
        
        # Ensure creation_date is naive (no timezone)
        if creation_date.tzinfo is not None:
            creation_date = creation_date.replace(tzinfo=None)
        
        age = (current_date - creation_date).days
        return max(0, age)  # Return 0 for negative values (future dates)
    
    except Exception as e:
        logger.debug(f"Failed to check domain age for {domain}: {e}")
        return None


def check_domain_age(url: str) -> Dict[str, Union[bool, float, str, Union[int, None]]]:
    """
    Check if a domain is suspiciously young (< 6 months old).

    Args:
        url (str): The URL to check

    Returns:
        Dict containing:
        - risky (bool): True if domain is < 6 months old
        - score (float): Risk score (0.0 - 1.0)
        - age_days (int or None): Age in days
        - reason (str): Reason message if risky, empty otherwise
    """
    if not WHOIS_AVAILABLE:
        return {
            "risky": False,
            "score": 0.0,
            "age_days": None,
            "reason": ""
        }

    if not isinstance(url, str):
        raise TypeError("URL must be a string")

    domain = extract_domain_name(url.strip())
    
    if not domain:
        return {
            "risky": False,
            "score": 0.0,
            "age_days": None,
            "reason": ""
        }

    age_days = get_domain_age_days(domain)
    
    if age_days is None:
        return {
            "risky": False,
            "score": 0.0,
            "age_days": None,
            "reason": ""
        }

    # Risk levels based on age
    # < 7 days: Very high risk (0.9)
    # < 30 days: High risk (0.75)
    # < 6 months (180 days): Medium-high risk (0.5)
    # >= 6 months: Low risk (0.0)
    
    if age_days < 7:
        score = 0.9
        reason = "Domain created less than 1 week ago"
        risky = True
    elif age_days < 30:
        score = 0.75
        reason = "Domain created less than 1 month ago"
        risky = True
    elif age_days < 180:
        score = 0.5
        reason = "Domain created less than 6 months ago"
        risky = True
    else:
        score = 0.0
        reason = ""
        risky = False

    return {
        "risky": risky,
        "score": score,
        "age_days": age_days,
        "reason": reason
    }
