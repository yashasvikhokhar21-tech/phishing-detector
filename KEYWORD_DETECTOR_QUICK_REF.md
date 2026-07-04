# Keyword Detector - Quick Reference

## Basic Usage

```python
from services.keyword_detector import check_suspicious_keywords

result = check_suspicious_keywords("https://verify-paypal-login.com")
print(result["score"])              # Risk score (0.0-1.0)
print(result["risk_level"])         # "high", "medium", "low", "none"
print(result["matched_keywords"])   # ["verify", "paypal", "login"]
```

## Risk Levels

| Risk Level | Score Range | Description |
|-----------|------------|-------------|
| High | 0.7-1.0 | Strong phishing indicators |
| Medium | 0.5-0.69 | Moderate concern |
| Low | 0.3-0.49 | Minor concern |
| None | 0.0-0.29 | No suspicious keywords |

## Common Phishing Keywords

| Category | Keywords | Risk |
|----------|----------|------|
| Auth | verify, login, signin, confirm | 0.6-0.7 |
| Banking | bank, credit, payment, urgent | 0.7-0.9 |
| Data | password, identity, SSN | 0.6-0.9 |
| Service | paypal, apple, amazon, google | 0.5-0.6 |
| Action | update, action-required, activate | 0.5-0.8 |

## API Functions

| Function | Purpose |
|----------|---------|
| `check_suspicious_keywords(url)` | Detect keywords |
| `extract_keywords(url)` | Get words from URL |
| `add_suspicious_keyword(keyword, score)` | Add custom keyword |
| `remove_suspicious_keyword(keyword)` | Remove keyword |
| `get_suspicious_keywords_list()` | View all keywords |
| `get_keyword_count()` | Count total keywords |

## Integration with Hybrid System

Keyword detection is automatically integrated:

1. **In URL Rules** (`check_url_rules()`)
   - High risk: +0.5× score weight
   - Medium risk: +0.3× score weight
   - Low risk: +0.15× score weight

2. **In Flask API** (`/predict`, `/batch-predict`)
   - Keywords included in response reasons
   - Matched keywords listed in results

3. **In Frontend**
   - Risk explanation cards show keyword matches
   - Color-coded by risk level

## Test & Validate

```bash
# Run keyword detector tests
python test_keyword_detector.py

# Validate setup includes keyword testing
python validate_setup.py
```

## Example Results

### Phishing URL
```
URL: https://verify-secure-bank-login.com
Keywords: ["verify", "secure", "bank", "login"]
Score: 0.72 (HIGH RISK)
```

### Safe URL
```
URL: https://www.google.com
Keywords: []
Score: 0.0 (NONE)
```

### Mixed Signals
```
URL: https://apple-news.com
Keywords: ["apple"]
Score: 0.35 (LOW RISK)
```

## Configuration

### Add Organization Keywords
```python
from services.keyword_detector import add_suspicious_keyword

add_suspicious_keyword("mybank-confirm", 0.85)
add_suspicious_keyword("myservice-verify", 0.75)
```

### Remove Keywords
```python
from services.keyword_detector import remove_suspicious_keyword

remove_suspicious_keyword("verify")  # No longer detect "verify"
```

## Performance

- Extraction: ~0.1ms
- Detection: ~0.5ms
- Total per URL: <1ms
- Memory: ~10KB

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Keywords not detected | Verify URL format; check keywords list |
| Too many false positives | Review keyword scores; adjust thresholds |
| Missing keywords | Use `add_suspicious_keyword()` to extend |

## Files

- `services/keyword_detector.py` - Main module
- `test_keyword_detector.py` - Test suite
- `KEYWORD_DETECTOR.md` - Full documentation

## Related

- [Domain Age Checker](DOMAIN_AGE_CHECKER.md)
- [Threat Intelligence](services/threat_intel.py)
- [URL Features](features/url_features.py)
