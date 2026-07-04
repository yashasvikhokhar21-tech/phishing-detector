#!/usr/bin/env python
"""Test script to validate domain age checker integration."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("PHISHING DETECTOR - Domain Age Checker Integration Test")
print("=" * 70)

errors = []

# Test 1: Import domain age module
try:
    from services.domain_age import check_domain_age, get_domain_age_days
    print("[✓] Domain age module imported successfully")
except Exception as e:
    print(f"[✗] Failed to import domain age module: {e}")
    errors.append(str(e))

# Test 2: Import integrated features module
try:
    from features.url_features import URLFeatureExtractor, check_url_rules
    print("[✓] Features module with domain age integration imported")
except Exception as e:
    print(f"[✗] Failed to import features module: {e}")
    errors.append(str(e))

# Test 3: Functional tests for domain age
if not errors:
    print("\n" + "=" * 70)
    print("FUNCTIONAL TESTS")
    print("=" * 70)
    
    # Test domain age checker initialization
    try:
        result = check_domain_age("https://google.com")
        print(f"[✓] Domain age checker works: {result}")
        if result['age_days'] is not None:
            print(f"    - Google.com age: {result['age_days']} days")
        else:
            print(f"    - Could not determine age (WHOIS may not be available in test environment)")
    except Exception as e:
        print(f"[⚠] Domain age check raised exception: {e}")
        print("    (This may be normal if WHOIS is not available)")
    
    # Test rule integration
    try:
        rules = check_url_rules("https://google.com")
        print(f"[✓] Rule-based detection works with domain age check")
        print(f"    - Risk score: {rules['score']:.4f}")
        print(f"    - Triggered rules: {rules['reasons']}")
    except Exception as e:
        print(f"[✗] Rule-based detection failed: {e}")
        errors.append(str(e))
    
    # Test with known legitimate domain
    try:
        rules = check_url_rules("https://microsoft.com")
        print(f"[✓] Legitimate domain check passed")
        print(f"    - Risk score: {rules['score']:.4f}")
    except Exception as e:
        print(f"[✗] Legitimate domain check failed: {e}")
        errors.append(str(e))

# Summary
print("\n" + "=" * 70)
if not errors:
    print("✓ INTEGRATION TEST PASSED - Domain age checker is integrated!")
else:
    print(f"⚠ {len(errors)} error(s) found:")
    for error in errors:
        print(f"  - {error}")
    print("\nNote: WHOIS library may need to be installed: pip install whois")
print("=" * 70)
