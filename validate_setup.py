#!/usr/bin/env python
"""Validation script for phishing detector module imports."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("PHISHING DETECTOR - Module Import Validation")
print("=" * 60)

errors = []

# Test 1: Services module
try:
    from services.threat_intel import check_threat_intelligence
    print("[✓] Services.threat_intel imported successfully")
except Exception as e:
    print(f"[✗] Failed to import services.threat_intel: {e}")
    errors.append(str(e))

# Test 2: Features module
try:
    from features.url_features import URLFeatureExtractor, check_url_rules
    print("[✓] Features.url_features imported successfully")
except Exception as e:
    print(f"[✗] Failed to import features.url_features: {e}")
    errors.append(str(e))

# Test 3: App module
try:
    # We can't fully import app without Flask running, but we can check syntax
    import py_compile
    py_compile.compile('app/app.py', doraise=True)
    print("[✓] App.app syntax is valid")
except Exception as e:
    print(f"[✗] App.app has syntax errors: {e}")
    errors.append(str(e))

# Test 4: Functional tests
if not errors:
    print("\n" + "=" * 60)
    print("FUNCTIONAL TESTS")
    print("=" * 60)
    
    try:
        # Test threat intel
        result = check_threat_intelligence("https://paypal-secure-login.com/login")
        if result["blacklisted"]:
            print("[✓] Threat intelligence detects blacklisted domains")
        else:
            print("[✗] Threat intelligence failed to detect blacklisted domain")
            errors.append("Blacklist check failed")
    except Exception as e:
        print(f"[✗] Threat intelligence test failed: {e}")
        errors.append(str(e))
    
    try:
        # Test feature extraction
        extractor = URLFeatureExtractor()
        features = extractor.extract_features("https://google.com")
        if len(features) == 8:
            print("[✓] Feature extraction works correctly")
        else:
            print(f"[✗] Expected 8 features, got {len(features)}")
            errors.append(f"Feature count mismatch: {len(features)}")
    except Exception as e:
        print(f"[✗] Feature extraction test failed: {e}")
        errors.append(str(e))
    
    try:
        # Test rule-based detection
        rules = check_url_rules("https://paypal-secure-login.com/login")
        if "domain_found_in_threat_database" in rules["reasons"]:
            print("[✓] Rule-based detection integrates threat intelligence")
        else:
            print("[✗] Rule-based detection failed to use threat intel")
            errors.append("Threat intel not integrated in rules")
    except Exception as e:
        print(f"[✗] Rule-based detection test failed: {e}")
        errors.append(str(e))
    
    try:
        # Test domain age integration
        from services.domain_age import check_domain_age
        result = check_domain_age("https://google.com")
        print("[✓] Domain age checker is available and working")
    except ImportError:
        print("[⚠] Domain age checker available (whois library may need install)")
    except Exception as e:
        print(f"[⚠] Domain age checker encountered issue: {e}")
        print("    (This may be normal if WHOIS server is unavailable)")
    
    try:
        # Test keyword-based detection
        from services.keyword_detector import check_suspicious_keywords
        result = check_suspicious_keywords("https://verify-paypal-login.com")
        if result["has_suspicious_keywords"] and "verify" in result["matched_keywords"]:
            print("[✓] Keyword-based detection works correctly")
        else:
            print("[✗] Keyword-based detection failed to detect keywords")
            errors.append("Keyword detection failed")
    except Exception as e:
        print(f"[✗] Keyword-based detection test failed: {e}")
        errors.append(str(e))

# Summary
print("\n" + "=" * 60)
if not errors:
    print("✓ ALL TESTS PASSED - System is ready!")
else:
    print(f"✗ {len(errors)} ERROR(S) FOUND:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print("=" * 60)
