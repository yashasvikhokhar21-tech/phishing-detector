# Domain Age Checker - Feature Documentation

## Overview
The Domain Age Checker is a hybrid threat intelligence module that analyzes the age of domains to detect newly created, suspicious domains commonly used in phishing attacks.

## How It Works

### Risk Assessment Logic
The domain age checker assigns risk scores based on how old the domain is:

| Domain Age | Risk Score | Risk Level | Reason |
|---|---|---|---|
| < 7 days | 0.9 | Very High | Domain created less than 1 week ago |
| 7-30 days | 0.75 | High | Domain created less than 1 month ago |
| 1-6 months | 0.5 | Medium-High | Domain created less than 6 months ago |
| > 6 months | 0.0 | Low | Established domain |

### Integration into Hybrid System

The domain age checker is integrated into the URL analysis pipeline:

1. **Threat Intelligence Check** (Highest Priority)
   - Checks against known phishing domain blacklist
   - Score weight: 0.8x

2. **Domain Age Check** (Second Priority)
   - Evaluates domain creation date via WHOIS
   - Score weight: 0.3x - 0.6x (varies by age)

3. **Traditional Rule-Based Checks**
   - IP addresses, @ symbols, HTTPS status, etc.
   - Apply after intelligent checks

## Installation

### Prerequisites
```bash
pip install whois
```

### Integration
The domain age checker is automatically integrated into `features/url_features.py`:

```python
from services.domain_age import check_domain_age

# In check_url_rules():
domain_age_result = check_domain_age(url)
if domain_age_result["risky"]:
    # Adds risk score and reason
```

## API Reference

### `check_domain_age(url: str) -> Dict`

Check if a domain is suspiciously young.

**Parameters:**
```python
url: str  # URL to analyze
```

**Returns:**
```python
{
    "risky": bool,           # True if domain < 6 months old
    "score": float,          # Risk score (0.0 - 1.0)
    "age_days": int | None,  # Age in days or None
    "reason": str            # Description of the risk
}
```

**Example:**
```python
from services.domain_age import check_domain_age

result = check_domain_age("https://example-new-domain.com")
# Returns:
# {
#     "risky": True,
#     "score": 0.75,
#     "age_days": 15,
#     "reason": "Domain created less than 1 month ago"
# }
```

### `get_domain_age_days(domain: str) -> int | None`

Get the age of a domain in days.

**Parameters:**
```python
domain: str  # Domain name (e.g., "example.com")
```

**Returns:**
```python
int | None  # Age in days, or None if unable to determine
```

### `extract_domain_name(url: str) -> str`

Extract the domain name from a URL.

**Parameters:**
```python
url: str  # Full URL
```

**Returns:**
```python
str  # Domain name only
```

## Feature Characteristics

### Advantages
✓ Detects newly created phishing domains  
✓ Automatic WHOIS lookup  
✓ Weighted scoring for hybrid system  
✓ Graceful degradation if WHOIS unavailable  
✓ No external API dependencies  

### Limitations
- WHOIS data may be inaccurate or delayed
- Private/masked WHOIS records may not be readable
- Rate limiting on WHOIS queries
- Network-dependent (requires internet connection)

## Configuration

### Risk Score Weights in URL Analysis

Current configuration in `features/url_features.py`:

```python
# Domain age risk score contributions
if age < 7 days:
    score += 0.9 * 0.6  # = 0.54 max contribution
elif age < 30 days:
    score += 0.75 * 0.5  # = 0.375 max contribution
elif age < 180 days:
    score += 0.5 * 0.3  # = 0.15 max contribution
```

## Testing

Run the test suite:
```bash
python test_domain_age.py
```

This tests:
- Module imports
- Domain age checking functionality
- Integration with rule-based detection
- Both legitimate and suspicious domains

## Future Improvements

- Add WHOIS caching to improve performance
- Support for additional registrar APIs
- Machine learning on domain age patterns
- Integration with threat intelligence feeds
- Whois data validation and verification

## Troubleshooting

### "whois library not installed"
**Solution:** Install the library
```bash
pip install whois
```

### "Unable to determine domain age"
**Possible causes:**
- WHOIS server temporarily unavailable
- Private/masked domain registration
- Invalid domain name
- Network connectivity issues

**Solution:** Check domain manually at https://whois.icann.org/

### Slow performance
**Cause:** WHOIS lookups can be slow (2-10 seconds)

**Solution:** Implement caching layer or timeout mechanism
