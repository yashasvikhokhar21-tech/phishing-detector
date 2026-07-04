#!/usr/bin/env python
"""Comprehensive validation of domain age checker integration."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports."""
    print("\n" + "=" * 70)
    print("IMPORT VALIDATION")
    print("=" * 70)
    
    try:
        from services.domain_age import check_domain_age, get_domain_age_days, extract_domain_name
        print("[✓] Domain age module imports successful")
        return True
    except Exception as e:
        print(f"[✗] Domain age module import failed: {e}")
        return False


def test_syntax():
    """Test Python syntax of modified files."""
    print("\n" + "=" * 70)
    print("SYNTAX VALIDATION")
    print("=" * 70)
    
    files_to_check = [
        'services/domain_age.py',
        'features/url_features.py',
        'services/__init__.py'
    ]
    
    all_valid = True
    for filepath in files_to_check:
        try:
            import py_compile
            py_compile.compile(filepath, doraise=True)
            print(f"[✓] {filepath} - syntax OK")
        except Exception as e:
            print(f"[✗] {filepath} - syntax error: {e}")
            all_valid = False
    
    return all_valid


def test_functionality():
    """Test domain age checker functionality."""
    print("\n" + "=" * 70)
    print("FUNCTIONALITY TESTS")
    print("=" * 70)
    
    try:
        from services.domain_age import check_domain_age, extract_domain_name
        
        # Test domain extraction
        domain = extract_domain_name("https://www.google.com/search")
        print(f"[✓] Domain extraction: {domain}")
        
        # Test domain age check (graceful with no WHOIS)
        result = check_domain_age("https://python.org")
        print(f"[✓] Domain age check: {result}")
        
        return True
    except Exception as e:
        print(f"[⚠] Functionality test: {e}")
        print("    (This may be normal if WHOIS library is not installed)")
        return False


def test_integration():
    """Test integration with URL features."""
    print("\n" + "=" * 70)
    print("INTEGRATION TESTS")
    print("=" * 70)
    
    try:
        from features.url_features import check_url_rules
        
        # Test URL rule checking with domain age
        result = check_url_rules("https://google.com")
        print(f"[✓] check_url_rules() works with domain age check")
        print(f"    Risk score: {result['score']:.4f}")
        print(f"    Rules triggered: {result['reasons']}")
        
        return True
    except Exception as e:
        print(f"[✗] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " DOMAIN AGE CHECKER - INTEGRATION VALIDATION ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = {
        "Imports": test_imports(),
        "Syntax": test_syntax(),
        "Functionality": test_functionality(),
        "Integration": test_integration()
    }
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:20} [{status}]")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - Domain age checker is fully integrated!")
        print("\nTo use the domain age checker:")
        print("  1. Install WHOIS library: pip install whois")
        print("  2. The checker will automatically run when analyzing URLs")
        print("  3. View DOMAIN_AGE_CHECKER.md for detailed documentation")
    else:
        print("⚠ Some tests failed or warnings detected")
        print("\nNote: Core integration works even if WHOIS is not installed")
        print("      Domain age checking will be gracefully skipped")
    
    print("=" * 70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
