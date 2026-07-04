import re
import os
import sys
from urllib.parse import urlparse
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.threat_intel import check_threat_intelligence
from services.domain_age import check_domain_age
from services.keyword_detector import check_suspicious_keywords


class URLFeatureExtractor:
    """
    Extract phishing detection features from URLs.
    """

    def extract_features(self, url: str) -> List[int]:
        """
        Extract phishing detection features from a URL, in the exact order used for training:
          1. URL length
          2. Domain length
          3. Number of special characters
          4. HTTPS flag (1 if HTTPS, else 0)
          5. Number of hyphens
          6. Number of dots
          7. Numeric character count
          8. Presence of '@' symbol (1 or 0)

        Args:
            url: URL string to analyze.

        Returns:
            List[int]: Feature vector in order.
        """
        if not isinstance(url, str):
            raise TypeError("url must be a string")

        normalized = url.strip()
        full_length = len(normalized)

        parsed = urlparse(normalized if "://" in normalized else "http://" + normalized)
        hostname = parsed.hostname or ""
        domain_length = len(hostname)

        lower_url = normalized.lower()
        https_flag = 1 if parsed.scheme == "https" else 0

        special_chars = re.findall(r"[!#$%^&*(),:;<>|`~\"'{}[\]\\\/]", normalized)  # common non-alnum punctuation
        num_special = len(special_chars)

        num_hyphens = normalized.count("-")
        num_dots = normalized.count(".")
        num_numeric = sum(ch.isdigit() for ch in normalized)
        at_flag = 1 if "@" in normalized else 0

        return [
            full_length,
            domain_length,
            num_special,
            https_flag,
            num_hyphens,
            num_dots,
            num_numeric,
            at_flag,
        ]


def check_url_rules(url: str) -> dict:
    """Rule-based phishing risk scoring for a single URL."""
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    normalized = url.strip()
    parsed = urlparse(normalized if "://" in normalized else "http://" + normalized)
    hostname = parsed.hostname or ""
    lower_url = normalized.lower()

    reasons = []
    score = 0.0

    # Threat intelligence check - highest priority
    threat_result = check_threat_intelligence(normalized)
    if threat_result["blacklisted"]:
        reasons.append("domain_found_in_threat_database")
        score += threat_result["score"] * 0.8  # Scale to 0.8 for consistency

    # Domain age check - second priority
    domain_age_result = check_domain_age(normalized)
    if domain_age_result["risky"]:
        if domain_age_result["age_days"] < 7:
            reasons.append("domain_created_less_than_1_week")
            score += domain_age_result["score"] * 0.6  # 0.54
        elif domain_age_result["age_days"] < 30:
            reasons.append("domain_created_less_than_1_month")
            score += domain_age_result["score"] * 0.5  # 0.375
        elif domain_age_result["age_days"] < 180:
            reasons.append("domain_created_less_than_6_months")
            score += domain_age_result["score"] * 0.3  # 0.15
    
    # Keyword-based detection - third priority
    keyword_result = check_suspicious_keywords(normalized)
    if keyword_result["has_suspicious_keywords"]:
        # Add matched keywords to reasons
        for keyword in keyword_result["matched_keywords"]:
            reasons.append(f"suspicious_keyword_{keyword}")
        # Weight: high=0.5, medium=0.3, low=0.15
        if keyword_result["risk_level"] == "high":
            score += keyword_result["score"] * 0.5
        elif keyword_result["risk_level"] == "medium":
            score += keyword_result["score"] * 0.3
        elif keyword_result["risk_level"] == "low":
            score += keyword_result["score"] * 0.15
    
    # High risk rules
    if _contains_ip_address(hostname):
        reasons.append("contains_ip_address")
        score += 0.35

    if "@" in normalized:
        reasons.append("contains_at_symbol")
        score += 0.35

    # Medium risk rules
    hyphen_count = normalized.count("-")
    if hyphen_count > 3:
        reasons.append("too_many_hyphens")
        score += 0.2

    if parsed.scheme != "https":
        reasons.append("missing_https")
        score += 0.2

    if len(normalized) > 100:
        reasons.append("very_long_url")
        score += 0.2

    return {
        "score": min(score, 1.0),
        "reasons": reasons,
    }


def _contains_ip_address(hostname: str) -> bool:
    """Detect whether the hostname is an IP address."""
    if not hostname:
        return False

    ipv4_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    ipv6_pattern = re.compile(r"^\[?[0-9a-fA-F:]+\]?$")
    return bool(ipv4_pattern.match(hostname)) or bool(ipv6_pattern.match(hostname))


# Example usage
if __name__ == "__main__":
    extractor = URLFeatureExtractor()
    sample = "https://www.paypa1.com/user-info@verify"
    print(extractor.extract_features(sample))
    print(check_url_rules(sample))
    # Output: [length, domain_length, special_chars, https, hyphens, dots, numeric_chars, at_flag]