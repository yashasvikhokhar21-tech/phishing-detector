"""
URL Feature Extraction Module
This module extracts features from URLs for machine learning model
"""

import re
from urllib.parse import urlparse

class URLFeatureExtractor:
    """Extract features from URLs for phishing detection"""
    
    def __init__(self):
        """Initialize the feature extractor"""
        self.features = []
    
    def extract_features(self, url):
        """
        Extract all features from a given URL
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            list: List of 8 features for ML model
        """
        features = []

        features.append(self._get_url_length_feature(url))     # 1
        features.append(self._get_domain_length(url))          # 2
        features.append(self._get_special_chars_count(url))    # 3
        features.append(self._get_protocol_feature(url))       # 4
        features.append(self._get_hyphens_in_domain(url))      # 5
        features.append(self._get_dots_count(url))             # 6
        features.append(self._get_numeric_count(url))          # 7
        features.append(self._get_at_symbol_feature(url))      # 8
        
        return features
    
    def _get_url_length_feature(self, url):
        """Feature 1: URL length (longer URLs often phishing)"""
        return len(url)
    
    def _get_dots_count(self, url):
        """Feature 2: Count of dots in URL"""
        return url.count('.')
    
    def _get_hyphens_in_domain(self, url):
        """Feature 3: Count of hyphens in domain (phishing indicator)"""
        try:
            domain = urlparse(url).netloc
            return domain.count('-')
        except:
            return 0
    
    def _get_at_symbol_feature(self, url):
        """Feature 4: Presence of @ symbol (phishing indicator)"""
        return 1 if '@' in url else 0
    
    def _get_protocol_feature(self, url):
        """Feature 5: Protocol type (1=https, 0=http/other)"""
        try:
            protocol = urlparse(url).scheme
            return 1 if protocol == 'https' else 0
        except:
            return 0
    
    def _get_domain_length(self, url):
        """Feature 6: Length of domain"""
        try:
            domain = urlparse(url).netloc
            return len(domain)
        except:
            return 0
    
    def _get_numeric_ratio(self, url):
        """Feature 7: Ratio of numeric characters in URL"""
        try:
            numeric_count = sum(1 for c in url if c.isdigit())
            return numeric_count / len(url) if len(url) > 0 else 0
        except:
            return 0
    
    def _get_special_chars_count(self, url):
        """Feature 8: Count of special characters"""
        special_chars = [':', '/', '?', '&', '=', '#', '%']
        return sum(url.count(char) for char in special_chars)
    
    def print_features(self, url, features):
        """Print extracted features in a readable format"""
        print(f"\n--- URL Features for: {url} ---")
        print(f"1. URL Length: {features[0]}")
        print(f"2. Dots Count: {features[1]}")
        print(f"3. Hyphens in Domain: {features[2]}")
        print(f"4. Has @ Symbol: {features[3]}")
        print(f"5. HTTPS Protocol: {features[4]}")
        print(f"6. Domain Length: {features[5]}")
        print(f"7. Numeric Ratio: {features[6]:.4f}")
        print(f"8. Special Chars: {features[7]}")
        print("-" * 40)


if __name__ == "__main__":
    # Test the feature extractor
    extractor = URLFeatureExtractor()
    
    test_urls = [
        "https://www.google.com",
        "http://bit-bank-secure.xyz/verify-account",
        "https://github.com/user/repo"
    ]
    
    for url in test_urls:
        features = extractor.extract_features(url)
        extractor.print_features(url, features)
        print(f"Features as list: {features}\n")


    def _get_numeric_count(self, url):
        return sum(1 for c in url if c.isdigit())    