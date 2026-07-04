"""
Services module for phishing detector application.
Contains threat intelligence, domain age checking, and other utility services.
"""

from .threat_intel import (
    check_threat_intelligence,
    extract_domain,
    add_to_blacklist,
    remove_from_blacklist,
    get_blacklist_size,
    is_domain_blacklisted
)

from .domain_age import (
    check_domain_age,
    get_domain_age_days,
    extract_domain_name
)

from .keyword_detector import (
    check_suspicious_keywords,
    extract_keywords,
    add_suspicious_keyword,
    remove_suspicious_keyword,
    get_suspicious_keywords_list,
    get_keyword_count
)

__all__ = [
    'check_threat_intelligence',
    'extract_domain',
    'add_to_blacklist',
    'remove_from_blacklist',
    'get_blacklist_size',
    'is_domain_blacklisted',
    'check_domain_age',
    'get_domain_age_days',
    'extract_domain_name',
    'check_suspicious_keywords',
    'extract_keywords',
    'add_suspicious_keyword',
    'remove_suspicious_keyword',
    'get_suspicious_keywords_list',
    'get_keyword_count'
]
