# 📊 Data Preprocessing - Complete Guide

A comprehensive guide to loading and preprocessing phishing detection datasets using Python.

## Overview

This guide covers:
- **Simple DataLoader** - Using only Python standard library (CSV, dict)
- **Advanced DataLoader** - Using pandas for complex operations
- **Sample Dataset** - Pre-configured CSV with 25 samples
- **Code Examples** - Ready-to-use code snippets

---

## Quick Start

### Option 1: Simple (No Dependencies)

```python
from ml.simple_loader import SimpleDataLoader

# Load CSV
loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
loader.load_csv()

# Separate features and labels
X, y = loader.separate_features_labels(label_col='label', drop_cols=['url'])

# Print summary
loader.print_summary()
```

### Option 2: Advanced (With Pandas)

```python
from ml.data_loader import DataLoader

# Load and preprocess
loader = DataLoader('datasets/sample_phishing_data.csv')
loader.load_data()
loader.clean_data(handle_missing='mean')
X, y = loader.separate_features_and_labels(drop_columns=['url'])
loader.print_summary()
```

### Run Examples

```bash
# Simple loader (no dependencies)
python ml/simple_loader.py

# Advanced loader (requires pandas)
python ml/preprocess_example.py
```

---

## Part 1: Simple DataLoader

### For beginners or minimal dependencies

**File:** `ml/simple_loader.py`

### Features

✅ No external dependencies (uses only Python standard library)
✅ Load CSV files with ease
✅ Separate features and labels
✅ Print informative summaries
✅ Works with any dataset format

### Usage

#### 1. Initialize

```python
from ml.simple_loader import SimpleDataLoader

loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
```

#### 2. Load Data

```python
data = loader.load_csv()
# Output:
# ✓ Loaded 25 rows
# ✓ Columns: ['url', 'domain_length', 'special_chars', ...]
```

#### 3. Print Info

```python
loader.print_info()
# Shows: columns, data types, first few rows
```

#### 4. Separate Features and Labels

```python
X, y = loader.separate_features_labels(
    label_col='label',      # Column with labels (0/1)
    drop_cols=['url']       # Columns to exclude from features
)

# Returns:
# X: List of dicts (each dict is a sample with features)
# y: List of labels (0 or 1)
```

#### 5. Print Summary

```python
loader.print_summary()
# Shows: feature count, label distribution, statistics

# Output:
# Total samples: 25
# Total features: 7
# 
# Label distribution:
#   Safe       (0):  13 ( 52.0%)
#   Phishing   (1):  12 ( 48.0%)
```

### Example: Complete Pipeline

```python
from ml.simple_loader import SimpleDataLoader

# Initialize
loader = SimpleDataLoader('datasets/sample_phishing_data.csv')

# Load
loader.load_csv()

# Info
loader.print_info()

# Separate
X, y = loader.separate_features_labels(
    label_col='label',
    drop_cols=['url']
)

# Summary
loader.print_summary()

# Use for ML
print(f"Features: {len(X)} samples × {len(X[0])} features")
print(f"Labels: {len(y)} samples")
```

---

## Part 2: Advanced DataLoader (Pandas)

### For advanced preprocessing needs

**File:** `ml/data_loader.py`

### Features

✅ Professional-grade data preprocessing
✅ Handle missing values automatically
✅ Remove duplicates
✅ Feature statistics and analysis
✅ Save processed data to CSV
✅ Comprehensive reporting

### Installation

```bash
pip install pandas numpy scikit-learn
```

### Usage

#### 1. Initialize

```python
from ml.data_loader import DataLoader

loader = DataLoader('datasets/sample_phishing_data.csv')
```

#### 2. Load Data

```python
df = loader.load_data()
# Output:
# ✓ Dataset loaded: datasets/sample_phishing_data.csv
#   Shape: 25 rows × 9 columns
```

#### 3. Inspect Raw Data

```python
loader.display_info()
# Shows: columns, types, missing values, statistics
```

#### 4. Clean Data

```python
cleaned = loader.clean_data(
    drop_duplicates=True,
    handle_missing='mean',      # 'mean', 'median', 'drop', 'forward'
    label_column='label'
)
# Automatically handles missing values and duplicates
```

#### 5. Separate Features and Labels

```python
X, y = loader.separate_features_and_labels(
    label_column='label',
    drop_columns=['url']
)
# X: pandas DataFrame (features)
# y: pandas Series (labels)
```

#### 6. Print Summary

```python
loader.print_summary()
# Shows: detailed statistics, distributions, feature analysis
```

#### 7. Save Processed Data

```python
loader.save_processed_data(
    X_path='data/X_processed.csv',
    y_path='data/y_processed.csv'
)
# Saves: CSV files for later use
```

### Example: Complete Pipeline

```python
from ml.data_loader import DataLoader

# Initialize
loader = DataLoader('datasets/sample_phishing_data.csv')

# Load
loader.load_data()

# Inspect
loader.display_info()

# Clean
loader.clean_data(
    drop_duplicates=True,
    handle_missing='mean',
    label_column='label'
)

# Separate
X, y = loader.separate_features_and_labels(
    label_column='label',
    drop_columns=['url']
)

# Summary
loader.print_summary()

# Save
loader.save_processed_data()
```

---

## Part 3: Sample Dataset

### File: `datasets/sample_phishing_data.csv`

#### Format

```
url,domain_length,special_chars,https,hyphens,dots,numeric_chars,@ symbol,label
https://www.google.com,11,3,1,0,2,0,0,0
https://paypa1-verify.com,18,2,1,0,2,1,0,1
```

#### Columns

- **url** (string): The URL being analyzed
- **domain_length** (int): Length of domain name
- **special_chars** (int): Count of special characters
- **https** (int): 1 if HTTPS, 0 otherwise
- **hyphens** (int): Count of hyphens in domain
- **dots** (int): Count of dots in URL
- **numeric_chars** (int): Count of numeric characters
- **@ symbol** (int): 1 if @ symbol present, 0 otherwise
- **label** (int): 0 = Safe, 1 = Phishing

#### Sample Data

25 URLs total:
- 13 legitimate (Safe)
- 12 phishing

---

## Part 4: Comparison

### Simple vs Advanced DataLoader

| Feature | Simple | Advanced |
|---------|--------|----------|
| **Dependencies** | None | pandas, numpy |
| **Complexity** | Low | Medium |
| **CSV Support** | ✅ | ✅ |
| **Missing Values** | Manual | Automatic |
| **Duplicates** | Manual | Automatic |
| **Statistics** | Basic | Advanced |
| **Scaling** | No | Yes |
| **Performance** | Fast | Optimized |
| **Use Case** | Learning | Production |

### When to Use

**Simple DataLoader:**
- Learning Python basics
- No external dependencies allowed
- Quick prototyping
- Small datasets

**Advanced DataLoader:**
- Production systems
- Large datasets
- Complex preprocessing
- Statistical analysis needed

---

## Part 5: Code Examples

### Example 1: Load from CSV

```python
from ml.simple_loader import SimpleDataLoader

loader = SimpleDataLoader('data.csv')
loader.load_csv()
```

### Example 2: Separate Features

```python
X, y = loader.separate_features_labels(
    label_col='label',
    drop_cols=['id', 'url']
)
```

### Example 3: Access Data

```python
# First sample features
print(X[0])  # {'domain_length': 11.0, 'special_chars': 3.0, ...}

# First label
print(y[0])  # 0

# All labels
print(y)  # [0, 0, 0, 1, 1, ...]

# Feature names
features = list(X[0].keys())
print(features)  # ['domain_length', 'special_chars', ...]
```

### Example 4: Statistics

```python
# Count labels
from collections import Counter
label_dist = Counter(y)
print(label_dist)  # Counter({0: 13, 1: 12})

# Class percentages
safe_pct = (label_dist[0] / len(y)) * 100
phishing_pct = (label_dist[1] / len(y)) * 100
print(f"Safe: {safe_pct:.1f}%, Phishing: {phishing_pct:.1f}%")
```

### Example 5: Feature Statistics

```python
# Average domain length
domain_lengths = [sample['domain_length'] for sample in X]
avg_length = sum(domain_lengths) / len(domain_lengths)
print(f"Average domain length: {avg_length:.1f}")

# By class
safe_lengths = [X[i]['domain_length'] for i in range(len(y)) if y[i] == 0]
phishing_lengths = [X[i]['domain_length'] for i in range(len(y)) if y[i] == 1]
print(f"Safe avg: {sum(safe_lengths)/len(safe_lengths):.1f}")
print(f"Phishing avg: {sum(phishing_lengths)/len(phishing_lengths):.1f}")
```

---

## Part 6: With Machine Learning

### Train-Test Split (Simple)

```python
from ml.simple_loader import SimpleDataLoader

loader = SimpleDataLoader('data.csv')
loader.load_csv()
X, y = loader.separate_features_labels(drop_cols=['url'])

# Manual split (80/20)
split_idx = int(len(X) * 0.8)
X_train = X[:split_idx]
y_train = y[:split_idx]
X_test = X[split_idx:]
y_test = y[split_idx:]
```

### Train-Test Split (Pandas/scikit-learn)

```python
from ml.data_loader import DataLoader
from sklearn.model_selection import train_test_split

loader = DataLoader('data.csv')
loader.load_data()
loader.clean_data()
X, y = loader.separate_features_and_labels()

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Model Training

```python
from sklearn.ensemble import RandomForestClassifier

# Create model
model = RandomForestClassifier(n_estimators=100)

# Train
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2%}")
```

---

## Part 7: Troubleshooting

### Common Issues

#### File Not Found
```python
# Problem
loader = SimpleDataLoader('wrong_path.csv')
loader.load_csv()
# Error: FileNotFoundError

# Solution
import os
print(os.path.exists('datasets/sample_phishing_data.csv'))
```

#### Wrong Column Name
```python
# Problem
X, y = loader.separate_features_labels(label_col='target')
# Error: KeyError (if column doesn't exist)

# Solution
print(loader.headers)  # Check available columns
X, y = loader.separate_features_labels(label_col='label')
```

#### Empty Data
```python
# Problem
if not loader.data:
    print("No data loaded")

# Solution
loader.load_csv()  # Make sure to call load_csv first
```

---

## Part 8: Best Practices

### ✓ Do

```python
# 1. Always load first
loader.load_csv()

# 2. Check what you have
loader.print_info()

# 3. Use meaningful variable names
X_features, y_labels = loader.separate_features_labels()

# 4. Verify shapes
print(f"Samples: {len(X_features)}, Features: {len(X_features[0])}")

# 5. Check label distribution
print(f"Labels: {Counter(y_features)}")
```

### ✗ Don't

```python
# Don't skip loading step
X, y = loader.separate_features_labels()  # Will fail!

# Don't ignore missing values
# Use clean_data() in advanced loader

# Don't include ID/URL in features
# Use drop_cols=['url', 'id']

# Don't ignore class imbalance
# Check if label distribution is skewed
```

---

## Summary

### Simple Loader
- Use: `ml/simple_loader.py`
- Run: `python ml/simple_loader.py`
- Dependencies: None
- Best for: Learning, simple datasets

### Advanced Loader
- Use: `ml/data_loader.py`
- Run: `python ml/preprocess_example.py` (with pandas installed)
- Dependencies: pandas, numpy
- Best for: Production, complex preprocessing

### Sample Data
- File: `datasets/sample_phishing_data.csv`
- Size: 25 URLs, 9 columns
- Classes: 13 safe, 12 phishing (balanced)

### Next Steps

1. ✅ Load data with SimpleDataLoader
2. ✅ Separate features and labels
3. ✅ Verify data quality
4. ✅ Train ML model
5. ✅ Evaluate performance

---

## Code Files

| File | Purpose | Dependencies |
|------|---------|--------------|
| `ml/simple_loader.py` | Simple CSV loader | None |
| `ml/data_loader.py` | Advanced preprocessing | pandas, numpy |
| `ml/preprocess_example.py` | Interactive examples | pandas |
| `datasets/sample_phishing_data.csv` | Sample dataset | None |

---

**Ready to preprocess your data? Start with `python ml/simple_loader.py`**
