"""
Keyword-Based Phishing Detection Module

This module detects suspicious keywords commonly found in phishing URLs
to identify potential phishing attempts.
"""

from typing import Dict, List, Union
import re


# Suspicious keywords commonly found in phishing URLs
SUSPICIOUS_KEYWORDS = {
    # Authentication/Verification related
    "login": 0.6,
    "signin": 0.6,
    "sign-in": 0.6,
    "logon": 0.6,
    "authenticate": 0.5,
    "auth": 0.5,
    "verify": 0.7,
    "confirmation": 0.5,
    "confirm": 0.5,
    "validate": 0.5,
    
    # Security/Account related
    "secure": 0.5,
    "security": 0.5,
    "account": 0.4,
    "profile": 0.3,
    "update": 0.4,
    "upgrade": 0.4,
    "activate": 0.6,
    "reactivate": 0.7,
    "restore": 0.5,
    "recovery": 0.5,
    
    # Financial/Banking
    "bank": 0.8,
    "banking": 0.8,
    "credit": 0.7,
    "payment": 0.4,
    "pay": 0.4,
    "transfer": 0.4,
    "limited": 0.5,
    "urgent": 0.6,
    "action-required": 0.8,
    "suspended": 0.8,
    "locked": 0.7,
    "blocked": 0.7,
    
    # User data related
    "password": 0.6,
    "passwd": 0.6,
    "pin": 0.5,
    "social-security": 0.9,
    "ssn": 0.9,
    "personal": 0.4,
    "identity": 0.6,
    "info": 0.3,
    "notification": 0.3,
    "alert": 0.4,
    
    # Popular service names (often spoofed)
    "apple": 0.5,
    "google": 0.5,
    "facebook": 0.5,
    "microsoft": 0.5,
    "amazon": 0.5,
    "paypal": 0.6,
    "ebay": 0.5,
    "netflix": 0.4,
    "instagram": 0.4,
    "twitter": 0.4,
    
    # Suspicious patterns
    "urgent-action": 0.8,
    "click-here": 0.7,
    "verify-now": 0.8,
    "confirm-identity": 0.9,
    "update-payment": 0.8,
    "unusual-activity": 0.7,
    "suspicious-activity": 0.7,
}


def extract_keywords(url: str) -> List[str]:
    """
    Extract words from a URL for keyword analysis.

    Args:
        url (str): The URL to analyze

    Returns:
        List[str]: List of extracted words
    """
    if not url:
        return []
    
    # Convert to lowercase
    url_lower = url.lower()
    
    # Replace common URL delimiters with spaces
    url_cleaned = re.sub(r'[-_./:%?&=]', ' ', url_lower)
    
    # Extract words (alphanumeric sequences)
    words = re.findall(r'\b[a-z0-9]{2,}\b', url_cleaned)
    
    return words


def check_suspicious_keywords(url: str) -> Dict[str, Union[float, List[str], str]]:
    """
    Check if a URL contains suspicious keywords commonly used in phishing.

    Args:
        url (str): The URL to analyze

    Returns:
        Dict containing:
        - has_suspicious_keywords (bool): True if suspicious keywords found
        - score (float): Risk score (0.0 - 1.0)
        - matched_keywords (list): Keywords found in URL
        - risk_level (str): "high", "medium", "low", or "none"
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    
    if not url:
        return {
            "has_suspicious_keywords": False,
            "score": 0.0,
            "matched_keywords": [],
            "risk_level": "none"
        }

    # Extract words from URL
    words = extract_keywords(url.strip())
    
    if not words:
        return {
            "has_suspicious_keywords": False,
            "score": 0.0,
            "matched_keywords": [],
            "risk_level": "none"
        }

    # Check for suspicious keywords
    matched_keywords = []
    keyword_scores = []
    
    for word in words:
        if word in SUSPICIOUS_KEYWORDS:
            matched_keywords.append(word)
            keyword_scores.append(SUSPICIOUS_KEYWORDS[word])
    
    if not matched_keywords:
        return {
            "has_suspicious_keywords": False,
            "score": 0.0,
            "matched_keywords": [],
            "risk_level": "none"
        }

    # Calculate combined score
    # Use average of matched keyword scores, boosted by number of matches
    avg_score = sum(keyword_scores) / len(keyword_scores)
    match_boost = min(len(matched_keywords) * 0.1, 0.3)  # Max boost of 0.3
    final_score = min(avg_score + match_boost, 1.0)

    # Determine risk level
    if final_score >= 0.7:
        risk_level = "high"
    elif final_score >= 0.5:
        risk_level = "medium"
    elif final_score >= 0.3:
        risk_level = "low"
    else:
        risk_level = "none"

    return {
        "has_suspicious_keywords": True,
        "score": final_score,
        "matched_keywords": matched_keywords,
        "risk_level": risk_level
    }


def get_suspicious_keywords_list() -> Dict[str, float]:
    """
    Get the full list of suspicious keywords and their scores.

    Returns:
        Dict: Keywords and their individual risk scores
    """
    return SUSPICIOUS_KEYWORDS.copy()


def add_suspicious_keyword(keyword: str, score: float = 0.5) -> bool:
    """
    Add a new suspicious keyword to the detection list.

    Args:
        keyword (str): The keyword to add
        score (float): Risk score (0.0 - 1.0)

    Returns:
        bool: True if added, False if already exists
    """
    keyword = keyword.lower().strip()
    
    if keyword and keyword not in SUSPICIOUS_KEYWORDS:
        if 0.0 <= score <= 1.0:
            SUSPICIOUS_KEYWORDS[keyword] = score
            return True
    
    return False


def remove_suspicious_keyword(keyword: str) -> bool:
    """
    Remove a suspicious keyword from the detection list.

    Args:
        keyword (str): The keyword to remove

    Returns:
        bool: True if removed, False if not found
    """
    keyword = keyword.lower().strip()
    
    if keyword in SUSPICIOUS_KEYWORDS:
        del SUSPICIOUS_KEYWORDS[keyword]
        return True
    
    return False


def get_keyword_count() -> int:
    """
    Get the number of suspicious keywords in the database.

    Returns:
        int: Number of keywords
    """
    return len(SUSPICIOUS_KEYWORDS)
