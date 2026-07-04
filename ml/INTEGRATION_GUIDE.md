# 🔗 Data Preprocessing Integration Guide

Learn how to integrate the data preprocessing modules with your phishing detection model.

## Overview

This guide shows how to:
1. Load custom phishing datasets
2. Preprocess the data
3. Train models with real data
4. Evaluate model performance

---

## Step 1: Prepare Your CSV File

Your dataset should have this format:

```csv
url,domain_length,special_chars,https,hyphens,dots,numeric_chars,@ symbol,label
https://www.google.com,11,3,1,0,2,0,0,0
https://paypa1.verify-account.com,27,4,1,1,2,1,0,1
```

**Required columns:**
- `url`: The URL being analyzed (will be dropped before training)
- Feature columns: Any numeric features (8 are recommended)
- `label`: Target column (0 = safe, 1 = phishing)

**We have:** A sample dataset with 25 URLs at `datasets/sample_phishing_data.csv`

---

## Step 2: Load and Preprocess Data

### Method A: Simple Loader (No Dependencies)

```python
from ml.simple_loader import SimpleDataLoader

# 1. Create loader
loader = SimpleDataLoader('datasets/sample_phishing_data.csv')

# 2. Load CSV
loader.load_csv()

# 3. Get features and labels
X, y = loader.separate_features_labels(
    label_col='label',
    drop_cols=['url']  # Remove URL from features
)

# 4. Verify data
loader.print_summary()
print(f"Loaded {len(X)} samples with {len(X[0])} features")
```

**Run:** `python ml/simple_loader.py`

**Output:**
```
✓ Loaded 25 rows
✓ Features extracted: 25 samples × 7 features
✓ Label distribution:
    Safe (0): 13 (52.0%)
    Phishing (1): 12 (48.0%)
```

### Method B: Advanced Loader (Pandas)

```python
from ml.data_loader import DataLoader

# 1. Create loader
loader = DataLoader('datasets/sample_phishing_data.csv')

# 2. Load data
loader.load_data()

# 3. Clean (handle missing values, duplicates)
loader.clean_data(
    drop_duplicates=True,
    handle_missing='mean',  # Use mean for numeric columns
    label_column='label'
)

# 4. Get features and labels
X, y = loader.separate_features_and_labels(
    label_column='label',
    drop_columns=['url']
)

# 5. Verify data
loader.print_summary()
```

---

## Step 3: Split Data for Training

### Option A: Manual Split

```python
# 80% train, 20% test
split_idx = int(len(X) * 0.8)

X_train = X[:split_idx]
y_train = y[:split_idx]

X_test = X[split_idx:]
y_test = y[split_idx:]

print(f"Train: {len(X_train)} samples")
print(f"Test: {len(X_test)} samples")
```

### Option B: scikit-learn Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # Keep class ratio
)

print(f"Train: {len(X_train)} samples")
print(f"Test: {len(X_test)} samples")
```

---

## Step 4: Convert to scikit-learn Format

SimpleDataLoader returns lists of dicts. Convert for ML models:

```python
import pandas as pd
import numpy as np

# Convert to DataFrame
df = pd.DataFrame(X)

# Or convert to numpy array
X_array = np.array([list(sample.values()) for sample in X])
```

---

## Step 5: Train Model

### Using Random Forest (Recommended)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load and preprocess data
from ml.simple_loader import SimpleDataLoader
loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
loader.load_csv()
X, y = loader.separate_features_labels(drop_cols=['url'])

# Split data
split_idx = int(len(X) * 0.8)
X_train = X[:split_idx]
y_train = y[:split_idx]
X_test = X[split_idx:]
y_test = y[split_idx:]

# Convert to numpy array
import numpy as np
X_train_array = np.array([list(sample.values()) for sample in X_train])
X_test_array = np.array([list(sample.values()) for sample in X_test])

# Create and train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_array, y_train)

# Evaluate
y_pred = model.predict(X_test_array)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
```

---

## Step 6: Save and Use Model

```python
import pickle

# Save model
with open('ml/phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load model later
with open('ml/phishing_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Make prediction
sample_features = X_test[0]  # Get one sample
features_array = np.array([list(sample_features.values())])
prediction = loaded_model.predict(features_array)
confidence = loaded_model.predict_proba(features_array)[0][int(prediction[0])]

print(f"Prediction: {prediction[0]} (Phishing)" if prediction[0] == 1 else "Prediction: {prediction[0]} (Safe)")
print(f"Confidence: {confidence:.2%}")
```

---

## Complete Pipeline Example

```python
# ============================================================================
# COMPLETE PIPELINE: Load Data → Train Model → Evaluate
# ============================================================================

from ml.simple_loader import SimpleDataLoader
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import pickle

# STEP 1: Load and preprocess
print("Step 1: Loading data...")
loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
loader.load_csv()
X, y = loader.separate_features_labels(drop_cols=['url'])
print(f"✓ Loaded {len(X)} samples")

# STEP 2: Split data
print("\nStep 2: Splitting data...")
split_idx = int(len(X) * 0.8)
X_train = X[:split_idx]
y_train = y[:split_idx]
X_test = X[split_idx:]
y_test = y[split_idx:]
print(f"✓ Train: {len(X_train)}, Test: {len(X_test)}")

# STEP 3: Convert to numpy
print("\nStep 3: Converting to numpy format...")
X_train_array = np.array([list(sample.values()) for sample in X_train])
X_test_array = np.array([list(sample.values()) for sample in X_test])
print(f"✓ X_train shape: {X_train_array.shape}")
print(f"✓ X_test shape: {X_test_array.shape}")

# STEP 4: Train model
print("\nStep 4: Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_array, y_train)
print("✓ Model trained")

# STEP 5: Evaluate
print("\nStep 5: Evaluating performance...")
y_pred = model.predict(X_test_array)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"\n📊 Model Performance:")
print(f"   Accuracy:  {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall:    {recall:.4f}")
print(f"   F1 Score:  {f1:.4f}")

# STEP 6: Save model
print("\nStep 6: Saving model...")
with open('ml/phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✓ Model saved to ml/phishing_model.pkl")

# STEP 7: Test prediction
print("\nStep 7: Testing prediction...")
test_sample = X_test[0]
test_features = np.array([list(test_sample.values())])
pred = model.predict(test_features)
confidence = model.predict_proba(test_features)[0][int(pred[0])]
label_name = "Phishing" if pred[0] == 1 else "Safe"
true_label_name = "Phishing" if y_test[0] == 1 else "Safe"

print(f"   True label: {true_label_name}")
print(f"   Predicted: {label_name}")
print(f"   Confidence: {confidence:.2%}")

print("\n✅ Pipeline complete!")
```

---

## Integrating with Existing train_model.py

Modify [ml/train_model.py](../ml/train_model.py) to use your CSV data:

```python
# OLD CODE: Uses hardcoded sample data
def create_sample_dataset():
    # ... hardcoded data ...

# NEW CODE: Load from CSV
from ml.simple_loader import SimpleDataLoader

def load_dataset_from_csv(filepath='datasets/sample_phishing_data.csv'):
    """Load dataset from CSV using SimpleDataLoader"""
    loader = SimpleDataLoader(filepath)
    loader.load_csv()
    X, y = loader.separate_features_labels(drop_cols=['url'])
    return X, y

# Use it
X, y = load_dataset_from_csv('path/to/your/data.csv')
```

---

## Working with Different Dataset Formats

### Scenario: Dataset without URL column

```python
loader = SimpleDataLoader('data.csv')
loader.load_csv()
X, y = loader.separate_features_labels(
    label_col='label'
    # drop_cols is optional
)
```

### Scenario: Different label column name

```python
X, y = loader.separate_features_labels(
    label_col='target',  # ← Change this
    drop_cols=['id', 'url']
)
```

### Scenario: Multiple columns to drop

```python
X, y = loader.separate_features_labels(
    label_col='label',
    drop_cols=['id', 'url', 'timestamp', 'source']
)
```

---

## Performance Optimization

### For Small Datasets (< 1000 samples)

```python
# SimpleDataLoader is fine
loader = SimpleDataLoader('data.csv')
# ... rest of pipeline
```

### For Large Datasets (> 10000 samples)

```python
# Use DataLoader with pandas for better performance
from ml.data_loader import DataLoader

loader = DataLoader('data.csv')
loader.load_data()
loader.clean_data()
X, y = loader.separate_features_and_labels()

# Then convert to numpy
import numpy as np
X_array = X.values  # pandas to numpy
y_array = y.values
```

---

## Error Handling

```python
import os
from ml.simple_loader import SimpleDataLoader

filepath = 'datasets/sample_phishing_data.csv'

# Check file exists
if not os.path.exists(filepath):
    print(f"❌ File not found: {filepath}")
    exit(1)

try:
    loader = SimpleDataLoader(filepath)
    loader.load_csv()
    X, y = loader.separate_features_labels(drop_cols=['url'])
    
    if not X or not y:
        print("❌ Failed to load data")
        exit(1)
    
    print(f"✅ Loaded {len(X)} samples")

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
```

---

## Next Steps

1. **Prepare data:** Create/prepare your CSV file with features and labels
2. **Load data:** Use SimpleDataLoader or DataLoader
3. **Verify data:** Check shapes, class balance, missing values
4. **Train model:** Use the complete pipeline example
5. **Evaluate:** Check accuracy, precision, recall, F1
6. **Deploy:** Save model and use in Flask app or batch predictions

---

## See Also

- [Data Preprocessing Guide](ml/DATA_PREPROCESSING_GUIDE.md) - Detailed API documentation
- [Quick Reference](QUICK_REFERENCE.md) - Command cheat sheet
- [Setup Guide](SETUP_GUIDE.md) - Initial setup instructions
- [README](README.md) - Full project documentation
