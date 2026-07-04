# Domain Age Checker - Quick Reference

## What is it?
The Domain Age Checker detects newly created phishing domains by analyzing domain creation dates using WHOIS data.

## Risk Scoring

```
< 7 days:      0.9 (Very High Risk)  ⛔ New domain - likely phishing
7-30 days:     0.75 (High Risk)      ⚠️  Recent domain - suspicious
1-6 months:    0.5 (Medium Risk)     ⚠️  Young domain - worth scrutiny
> 6 months:    0.0 (Low Risk)        ✓  Established domain - normal
```

## Integration Points

### In Features Module
```python
from services.domain_age import check_domain_age
from features.url_features import check_url_rules

# Automatically runs in:
rules = check_url_rules("https://suspicious.com")
# Returns domain age warnings in rules['reasons']
```

### In Services Module
```python
from services import check_domain_age

result = check_domain_age("https://example.com")
# {
#     "risky": bool,
#     "score": float (0.0-1.0),
#     "age_days": int or None,
#     "reason": str
# }
```

## How It Contributes to Risk Score

The domain age score is **weighted** in the hybrid detection system:

| Age Category | Direct Score | Weight | Final Contribution |
|---|---|---|---|
| < 7 days | 0.9 | 0.6x | +0.54 |
| 7-30 days | 0.75 | 0.5x | +0.375 |
| 1-6 months | 0.5 | 0.3x | +0.15 |
| > 6 months | 0.0 | - | +0.0 |

## Requirements

```bash
pip install whois
```

## Testing

```bash
# Validate all modules
python validate_setup.py

# Test domain age checker specifically
python validate_domain_age.py

# Quick test
python test_domain_age.py
```

## Key Features

✓ **Automatic WHOIS Lookup** - No manual queries needed  
✓ **Graceful Degradation** - Works even if WHOIS unavailable  
✓ **Weighted Scoring** - Integrated into hybrid detection  
✓ **No External APIs** - Uses standard WHOIS protocol  
✓ **Performance Aware** - Caches results when possible  

## Troubleshooting

| Issue | Solution |
|---|---|
| ModuleNotFoundError: whois | `pip install whois` |
| "Unable to determine age" | Check whois.icann.org manually |
| Slow performance | WHOIS lookups can take 2-10 seconds |
| Private domain detected | Some domains use WHOIS privacy |

## Examples

### Check a Domain
```python
from services.domain_age import check_domain_age

# Suspicious new domain
result = check_domain_age("https://paypal-verify-account.com")
# Returns: risky=True, score=0.9, age_days=3

# Legitimate established domain
result = check_domain_age("https://google.com")
# Returns: risky=False, score=0.0, age_days=28156
```

### Rules Integration
```python
from features.url_features import check_url_rules

rules = check_url_rules("https://amazon-verify.com")
print(rules['score'])      # Will include domain age risk
print(rules['reasons'])    # Will show "domain_created_less_than_*"
```

## For Developers

See `DOMAIN_AGE_CHECKER.md` for:
- Full API documentation
- Configuration details
- Troubleshooting guide
- Future improvements
