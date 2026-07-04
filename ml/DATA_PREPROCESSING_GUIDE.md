# 📊 Data Preprocessing Guide

Complete guide for loading, cleaning, and preprocessing phishing detection datasets.

## Overview

The data preprocessing module provides:
- **DataLoader class** - Load and preprocess CSV datasets
- **Sample dataset** - Example phishing data (25 URLs)
- **Example script** - Interactive demonstrations
- **Reusable code** - Easy integration with ML pipeline

---

## Quick Start

### 1. Basic Usage

```python
from ml.data_loader import DataLoader

# Initialize loader
loader = DataLoader('datasets/sample_phishing_data.csv')

# Load data
loader.load_data()

# Clean data
loader.clean_data(drop_duplicates=True, handle_missing='mean')

# Separate features and labels
X, y = loader.separate_features_and_labels(label_column='label')

# Get summary
loader.print_summary()
```

### 2. Run Example Script

```bash
python ml/preprocess_example.py
```

Interactive menu with 7 examples:
1. Basic Data Loading
2. Data Cleaning
3. Feature Separation
4. Complete Pipeline
5. Data Analysis
6. Custom Preprocessing
7. Run All Examples

---

## DataLoader Class

### Initialization

```python
loader = DataLoader(filepath)
```

**Parameters:**
- `filepath` (str): Path to CSV file

**Example:**
```python
loader = DataLoader('datasets/phishing_data.csv')
```

---

## Methods

### 1. `load_data()`

Load dataset from CSV file.

```python
dataframe = loader.load_data()
```

**Returns:** `pd.DataFrame`

**Output:**
```
✓ Dataset loaded: datasets/sample_phishing_data.csv
  Shape: 25 rows × 9 columns
```

---

### 2. `display_info()`

Display detailed information about raw dataset.

Shows:
- Column names and types
- Missing values count
- First few rows
- Basic statistics

```python
loader.display_info()
```

**Example Output:**
```
============================================================
DATASET INFORMATION
============================================================

Shape: 25 rows, 9 columns

Column Names and Types:
  url                        : object
  domain_length             : int64
  special_chars             : int64
  ...

Missing Values:
  No missing values found ✓

First Few Rows:
         url  domain_length  special_chars  https  ...
0  https://www.google.com            11           3      1
1  https://www.facebook.com           14           2      1
...
```

---

### 3. `clean_data()`

Clean and preprocess the dataset.

```python
cleaned = loader.clean_data(
    drop_duplicates=True,
    handle_missing='mean',
    label_column='label'
)
```

**Parameters:**
- `drop_duplicates` (bool): Remove duplicate rows (default: True)
- `handle_missing` (str): Strategy for missing values
  - `'mean'`: Fill numeric columns with mean (default)
  - `'median'`: Fill numeric columns with median
  - `'drop'`: Drop rows with any missing values
  - `'forward'`: Use forward fill strategy
- `label_column` (str): Name of label column (default: 'label')

**Returns:** `pd.DataFrame`

**Example Output:**
```
============================================================
CLEANING DATA
============================================================
✓ Removed 0 duplicate rows
✓ No missing values found

Final shape: 25 rows × 9 columns
```

---

### 4. `separate_features_and_labels()`

Separate features (X) and labels (y) from dataset.

```python
X, y = loader.separate_features_and_labels(
    label_column='label',
    drop_columns=['url', 'id']
)
```

**Parameters:**
- `label_column` (str): Column containing labels (default: 'label')
- `drop_columns` (list): Additional columns to exclude from features

**Returns:** `Tuple[pd.DataFrame, pd.Series]`
- X: Features DataFrame
- y: Labels Series

**Example Output:**
```
============================================================
SEPARATING FEATURES AND LABELS
============================================================
✓ Dropped columns: ['url']

Features (X):
  Shape: (25, 8)
  Columns (8): ['domain_length', 'special_chars', 'https', ...]

Labels (y):
  Shape: (25,)
  Values: [0 1]
  Distribution:
    Safe (0):        15 ( 60.00%)
    Phishing (1):    10 ( 40.00%)
```

---

### 5. `get_dataset_summary()`

Get dictionary with dataset statistics.

```python
summary = loader.get_dataset_summary()
```

**Returns:** `dict`

**Keys:**
- `total_samples`: Number of samples
- `total_features`: Number of features
- `feature_names`: List of feature names
- `label_distribution`: Count per class
- `missing_values`: Total missing values
- `duplicate_rows`: Number of duplicates
- `numeric_features`: List of numeric column names
- `categorical_features`: List of categorical column names

**Example:**
```python
summary = loader.get_dataset_summary()
print(summary['total_samples'])        # 25
print(summary['label_distribution'])   # {0: 15, 1: 10}
print(summary['numeric_features'])     # ['domain_length', 'special_chars', ...]
```

---

### 6. `print_summary()`

Print formatted dataset summary.

```python
loader.print_summary()
```

**Example Output:**
```
============================================================
DATASET SUMMARY
============================================================

Sample Size:        25
Total Features:     8
Missing Values:     0
Duplicate Rows:     0

Numeric Features (8):
  - domain_length
  - special_chars
  - https
  - hyphens
  - dots
  - numeric_chars
  - @ symbol

Categorical Features (0):

Class Distribution:
  Safe       (0): 15 ( 60.00%) ███████████████
  Phishing   (1): 10 ( 40.00%) ██████████
```

---

### 7. `save_processed_data()`

Save features and labels to CSV files.

```python
loader.save_processed_data(
    X_path='data/X_processed.csv',
    y_path='data/y_processed.csv'
)
```

**Parameters:**
- `X_path` (str): Path to save features
- `y_path` (str): Path to save labels

**Creates:**
- CSV file with all features
- CSV file with all labels

---

## Complete Workflow Example

### Step-by-Step

```python
from ml.data_loader import DataLoader

# 1. Initialize
loader = DataLoader('datasets/phishing_data.csv')

# 2. Load raw data
loader.load_data()

# 3. Inspect raw data
loader.display_info()

# 4. Clean data
loader.clean_data(
    drop_duplicates=True,
    handle_missing='mean',
    label_column='label'
)

# 5. Separate features and labels
X, y = loader.separate_features_and_labels(
    label_column='label',
    drop_columns=['url', 'id']
)

# 6. Get summary
loader.print_summary()

# 7. Ready for ML!
print(f"Features shape: {X.shape}")
print(f"Labels shape: {y.shape}")
```

---

## Dataset Format

### Required CSV Format

```csv
url,feature1,feature2,...,label
https://example.com,10,5,...,0
https://phishing.com,20,8,...,1
```

### Column Requirements

- **Label Column**
  - Name: `label` (by default)
  - Values: 0 (Safe) or 1 (Phishing)
  - Type: Integer

- **Feature Columns**
  - Can be numeric or categorical
  - Missing values handled automatically
  - Non-label columns become features

### Sample Data

File: `datasets/sample_phishing_data.csv`

```csv
url,domain_length,special_chars,https,hyphens,dots,numeric_chars,@ symbol,label
https://www.google.com,11,3,1,0,2,0,0,0
https://paypa1-verify.com,18,2,1,0,2,1,0,1
```

---

## Missing Values Handling

### Strategy Comparison

| Strategy | Numeric | Categorical | When to Use |
|----------|---------|-------------|------------|
| `'mean'` | Mean | Mode | Default, most common |
| `'median'` | Median | Mode | Outliers present |
| `'drop'` | Drop row | Drop row | Few missing values |
| `'forward'` | Forward fill | Forward fill | Time series data |

### Example

```python
# Mean strategy (numeric: mean, categorical: mode)
loader.clean_data(handle_missing='mean')

# Median strategy
loader.clean_data(handle_missing='median')

# Drop rows with any missing values
loader.clean_data(handle_missing='drop')

# Forward fill
loader.clean_data(handle_missing='forward')
```

---

## Data Types Handling

### Numeric Features
- Int64, Float64
- Automatically detected
- Fillna uses mean/median

### Categorical Features
- Object (string) type
- Automatically detected
- Fillna uses mode (most common)

### Example

```python
X = loader.X

# Get numeric features
numeric = X.select_dtypes(include=['int64', 'float64']).columns
print(numeric)

# Get categorical features
categorical = X.select_dtypes(include=['object']).columns
print(categorical)
```

---

## Column Dropping

### Default Behavior
- Only label column dropped
- All other columns become features

### Custom Columns to Drop

```python
X, y = loader.separate_features_and_labels(
    label_column='label',
    drop_columns=['url', 'id', 'timestamp']  # Additional columns to exclude
)
```

### Example

```python
# Drop 'url' from features
X, y = loader.separate_features_and_labels(drop_columns=['url'])

# Access remaining features
print(X.columns)  # ['domain_length', 'special_chars', ...]
```

---

## Data Statistics

### Get Numeric Summary

```python
# Numeric statistics
stats = X.describe()
print(stats)
```

**Shows:**
- Count, mean, std deviation
- Min, 25%, 50%, 75%, max

### Get Class Distribution

```python
# Label counts
print(y.value_counts())

# Label proportions
print(y.value_counts(normalize=True))

# As dictionary
summary = loader.get_dataset_summary()
print(summary['label_distribution'])
```

---

## Integration with ML

### With scikit-learn

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load and preprocess
loader = DataLoader('datasets/phishing_data.csv')
loader.load_data()
loader.clean_data()
X, y = loader.separate_features_and_labels()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
print(f"Accuracy: {model.score(X_test, y_test)}")
```

### With Custom Model

```python
# Your custom preprocessing function
def my_preprocessing(X):
    # Do something special
    return X_processed

# Use DataLoader to load & clean
loader = DataLoader('datasets/phishing_data.csv')
loader.load_data()
loader.clean_data()
X, y = loader.separate_features_and_labels()

# Apply custom preprocessing
X = my_preprocessing(X)

# Train your model
# ...
```

---

## Error Handling

### Common Errors

#### File Not Found
```python
try:
    loader.load_data()
except FileNotFoundError as e:
    print(f"Error: {e}")
```

#### Label Column Missing
```python
try:
    loader.separate_features_and_labels(label_column='target')
except ValueError as e:
    print(f"Error: {e}")
```

#### No Data Loaded
```python
loader = DataLoader('file.csv')
# Forgot to call load_data()
try:
    loader.clean_data()
except ValueError:
    print("Call load_data() first")
```

---

## Best Practices

### ✓ Do

```python
# 1. Load first
loader.load_data()

# 2. Inspect before cleaning
loader.display_info()

# 3. Clean appropriately
loader.clean_data()

# 4. Separate features properly
X, y = loader.separate_features_and_labels(
    drop_columns=['id', 'timestamp']
)

# 5. Check summary
loader.print_summary()

# 6. Verify shapes
assert X.shape[0] == y.shape[0]
```

### ✗ Don't

```python
# Skip inspection
# Don't blindly clean without checking data

# Use wrong strategy
# Don't use 'drop' if many missing values

# Forget to drop ID columns
# Don't include ID/timestamp in features

# Ignore class imbalance
# Don't ignore if classes are imbalanced
```

---

## Example Datasets

### Using Sample Data

```bash
# Already included
datasets/sample_phishing_data.csv
```

### Using Your Data

1. Place CSV in `datasets/` folder
2. Ensure has `label` column (0/1)
3. Load with DataLoader:

```python
loader = DataLoader('datasets/your_data.csv')
loader.load_data()
# ... rest of pipeline
```

### Public Datasets

- **PhishTank**: https://phishtank.org/
- **UCI ML**: https://archive.ics.uci.edu/
- **Kaggle**: https://www.kaggle.com/ (search "phishing")

---

## Performance Tips

### Large Datasets

```python
# For large CSVs, read in chunks
loader = DataLoader('large_file.csv')
# DataLoader handles efficiently

# Consider dropping unnecessary columns early
X, y = loader.separate_features_and_labels(
    drop_columns=['url', 'timestamp', 'id']  # Reduce memory
)
```

### Memory Issues

```python
# Reduce feature precision if needed
X = X.astype('float32')  # Instead of float64

# Save processed data
loader.save_processed_data()

# Load processed data
X = pd.read_csv('data/X_processed.csv')
y = pd.read_csv('data/y_processed.csv')
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| FileNotFoundError | Ensure CSV path is correct |
| Label column missing | Add `label` column or specify name |
| Wrong data types | Ensure proper CSV formatting |
| Memory error | Use smaller dataset or reduce precision |
| NaN values remain | Try different handle_missing strategy |

---

## Code Examples

### Example 1: Simple Loading
```python
from ml.data_loader import DataLoader

loader = DataLoader('data.csv')
loader.load_data()
loader.display_info()
```

### Example 2: Complete Pipeline
```python
loader = DataLoader('data.csv')
loader.load_data()
loader.clean_data()
X, y = loader.separate_features_and_labels()
loader.print_summary()
```

### Example 3: Custom Configuration
```python
loader = DataLoader('data.csv')
loader.load_data()
loader.clean_data(
    drop_duplicates=True,
    handle_missing='median',
    label_column='target'
)
X, y = loader.separate_features_and_labels(
    label_column='target',
    drop_columns=['id', 'url', 'timestamp']
)
```

---

## Summary

The DataLoader provides:

✅ **Easy data loading** - One line to load CSV
✅ **Automatic cleaning** - Handle missing values
✅ **Feature separation** - X and y ready for ML
✅ **Reusable code** - Use across projects
✅ **Good practices** - Professional grade
✅ **Clear output** - Informative messages

---

**Ready to preprocess your data?**

→ Start with: `python ml/preprocess_example.py`
