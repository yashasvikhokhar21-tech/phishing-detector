"""
Test and validate the keyword-based phishing detection module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.keyword_detector import (
    check_suspicious_keywords,
    extract_keywords,
    add_suspicious_keyword,
    remove_suspicious_keyword,
    get_suspicious_keywords_list,
    get_keyword_count,
    SUSPICIOUS_KEYWORDS
)


def test_extract_keywords():
    """Test keyword extraction from URLs."""
    print("\n=== Testing Keyword Extraction ===")
    
    test_cases = [
        ("https://verify-account.paypal.com", ["verify", "account", "paypal"]),
        ("https://bank-login.example.com", ["bank", "login", "example"]),
        ("https://www.google.com", ["www", "google"]),
        ("", []),
    ]
    
    for url, expected_keywords in test_cases:
        keywords = extract_keywords(url)
        print(f"URL: {url}")
        print(f"  Extracted: {keywords}")
        print(f"  Expected to contain: {expected_keywords}")
        print()


def test_keyword_detection():
    """Test suspicious keyword detection."""
    print("\n=== Testing Keyword Detection ===")
    
    test_urls = [
        "https://verify-paypal-account.com",
        "https://secure-bank-login.example.com",
        "https://confirm-identity-check.net",
        "https://www.google.com",
        "https://apple-store.com",
        "https://update-payment-method.bank.com",
        "",
    ]
    
    for url in test_urls:
        result = check_suspicious_keywords(url)
        print(f"URL: {url}")
        print(f"  Has suspicious keywords: {result['has_suspicious_keywords']}")
        print(f"  Risk score: {result['score']:.3f}")
        print(f"  Risk level: {result['risk_level']}")
        if result['matched_keywords']:
            print(f"  Matched keywords: {result['matched_keywords']}")
        print()


def test_risk_scoring():
    """Test risk score calculation."""
    print("\n=== Testing Risk Score Calculation ===")
    
    test_urls = [
        ("https://login.com", "Single keyword"),
        ("https://verify-login-secure.com", "Multiple keywords"),
        ("https://confirm-identity-verify.com", "High-risk keywords"),
        ("https://www.example.com", "No suspicious keywords"),
    ]
    
    for url, description in test_urls:
        result = check_suspicious_keywords(url)
        print(f"{description}: {url}")
        print(f"  Score: {result['score']:.3f} ({result['risk_level'].upper()})")
        if result['matched_keywords']:
            print(f"  Keywords: {', '.join(result['matched_keywords'])}")
        print()


def test_keyword_management():
    """Test adding and removing keywords."""
    print("\n=== Testing Keyword Management ===")
    
    initial_count = get_keyword_count()
    print(f"Initial keyword count: {initial_count}")
    
    # Test adding a keyword
    success = add_suspicious_keyword("test-malware", 0.9)
    print(f"\nAdded 'test-malware' with score 0.9: {success}")
    print(f"New keyword count: {get_keyword_count()}")
    
    # Test duplicate add
    success = add_suspicious_keyword("test-malware", 0.8)
    print(f"Added 'test-malware' again: {success}")
    
    # Test invalid score
    success = add_suspicious_keyword("bad-score", 1.5)
    print(f"Added invalid score (1.5): {success}")
    
    # Test removing a keyword
    success = remove_suspicious_keyword("test-malware")
    print(f"\nRemoved 'test-malware': {success}")
    print(f"Final keyword count: {get_keyword_count()}")
    
    # Test remove non-existent
    success = remove_suspicious_keyword("non-existent-keyword")
    print(f"Removed non-existent keyword: {success}")


def test_high_risk_combinations():
    """Test combinations of high-risk keywords."""
    print("\n=== Testing High-Risk Keyword Combinations ===")
    
    test_cases = [
        ("https://verify-secure-login.com", "Two high-risk keywords"),
        ("https://urgent-action-required-bank.com", "phrase-like keywords"),
        ("https://confirm-identity-paypal.com", "Identity + service name"),
        ("https://verify.google.com/confirm", "Domain + verification keywords"),
    ]
    
    for url, description in test_cases:
        result = check_suspicious_keywords(url)
        print(f"{description}")
        print(f"  URL: {url}")
        print(f"  Score: {result['score']:.3f} ({result['risk_level'].upper()})")
        print(f"  Keywords: {result['matched_keywords']}")
        print()


def test_integration_with_features():
    """Test integration with URL feature extraction."""
    print("\n=== Testing Integration with Features ===")
    
    try:
        from features.url_features import check_url_rules
        
        test_urls = [
            "https://secure-paypal-login.com",
            "https://verify-bank-account.net",
            "https://www.google.com",
            "https://urgent-action-required-amazon.com",
        ]
        
        for url in test_urls:
            result = check_url_rules(url)
            print(f"URL: {url}")
            print(f"  Overall score: {result['score']:.3f}")
            
            # Count keyword reasons
            keyword_reasons = [r for r in result['reasons'] if 'suspicious_keyword' in r]
            if keyword_reasons:
                print(f"  Keyword detections: {len(keyword_reasons)}")
                for reason in keyword_reasons[:3]:  # Show first 3
                    keyword = reason.replace('suspicious_keyword_', '')
                    print(f"    - {keyword}")
            
            print()
    except Exception as e:
        print(f"Error testing integration: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("KEYWORD-BASED PHISHING DETECTION TEST SUITE")
    print("=" * 60)
    
    try:
        test_extract_keywords()
        test_keyword_detection()
        test_risk_scoring()
        test_keyword_management()
        test_high_risk_combinations()
        test_integration_with_features()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
