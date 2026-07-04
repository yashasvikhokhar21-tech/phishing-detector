#!/usr/bin/env python
"""Test script to validate threat intelligence module and feature extraction."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing threat intelligence module...")
    from services.threat_intel import check_threat_intelligence
    print("✓ Threat intel module imported successfully")
    
    # Test with blacklisted domain
    result = check_threat_intelligence("https://paypal-secure-login.com/login")
    assert result["blacklisted"] == True, "Should detect blacklisted domain"
    print(f"✓ Blacklist test passed: {result}")
    
    # Test with legitimate domain
    result2 = check_threat_intelligence("https://google.com")
    assert result2["blacklisted"] == False, "Should not flag legitimate domain"
    print(f"✓ Legitimate domain test passed: {result2}")
    
    print("\nTesting URL feature extraction...")
    from features.url_features import URLFeatureExtractor, check_url_rules
    print("✓ URL features module imported successfully")
    
    extractor = URLFeatureExtractor()
    features = extractor.extract_features("https://google.com")
    print(f"✓ Feature extraction works: {len(features)} features extracted")
    
    rules_result = check_url_rules("https://paypal-secure-login.com/login")
    print(f"✓ Rule-based detection works: {rules_result}")
    
    print("\n✓ All tests passed!")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

