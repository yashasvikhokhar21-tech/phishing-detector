"""
Example script demonstrating how to use the phishing detector
without running the web server
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from features.url_features import URLFeatureExtractor


def main():
    """Demonstrate feature extraction"""
    print("\n" + "="*60)
    print("PHISHING DETECTOR - FEATURE EXTRACTION EXAMPLE")
    print("="*60)
    
    extractor = URLFeatureExtractor()
    
    # Test URLs
    test_urls = {
        "Legitimate": [
            "https://www.google.com",
            "https://www.github.com",
            "https://www.wikipedia.org"
        ],
        "Suspicious": [
            "http://gogle.com",
            "https://g00gle-secure.xyz",
            "http://paypa1-verify.com"
        ]
    }
    
    for category, urls in test_urls.items():
        print(f"\n{category} URLs:")
        print("-" * 60)
        
        for url in urls:
            features = extractor.extract_features(url)
            
            print(f"\nURL: {url}")
            print(f"  1. URL Length:           {features[0]}")
            print(f"  2. Dots Count:           {features[1]}")
            print(f"  3. Hyphens in Domain:    {features[2]}")
            print(f"  4. @ Symbol Present:     {'Yes' if features[3] else 'No'}")
            print(f"  5. HTTPS Protocol:       {'Yes' if features[4] else 'No'}")
            print(f"  6. Domain Length:        {features[5]}")
            print(f"  7. Numeric Ratio:        {features[6]:.4f}")
            print(f"  8. Special Characters:   {features[7]}")
            print(f"  Features Array: {features}")
    
    print("\n" + "="*60)
    print("\nTo use the full system:")
    print("1. Train the model: python ml/train_model.py")
    print("2. Run the web app: python app/app.py")
    print("3. Open: http://localhost:5000")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
