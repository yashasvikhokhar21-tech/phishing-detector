"""
Simple Data Loading Example - No External Dependencies Required
Demonstrates basic phishing dataset loading using native Python
"""

import csv
import os
from collections import defaultdict, Counter


class SimpleDataLoader:
    """
    Simple data loader using only Python standard library
    (No pandas/numpy required)
    """
    
    def __init__(self, filepath):
        """Initialize the loader"""
        self.filepath = filepath
        self.data = []
        self.headers = []
        self.X = []
        self.y = []
    
    def load_csv(self):
        """Load CSV file"""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            self.data = list(reader)
        
        print(f"✓ Loaded {len(self.data)} rows")
        print(f"✓ Columns: {self.headers}")
        return self.data
    
    def print_info(self):
        """Print basic information"""
        print("\n" + "="*60)
        print("DATASET INFORMATION")
        print("="*60)
        print(f"Total samples: {len(self.data)}")
        print(f"Total features: {len(self.headers)}")
        print(f"\nColumns: {', '.join(self.headers)}")
        
        print("\nFirst 3 rows:")
        print("-" * 60)
        for i, row in enumerate(self.data[:3]):
            print(f"Row {i}:")
            for col, val in row.items():
                print(f"  {col:20s}: {val}")
        
        print("="*60 + "\n")
    
    def separate_features_labels(self, label_col='label', drop_cols=None):
        """
        Separate features and labels
        
        Args:
            label_col: Column name with labels
            drop_cols: List of columns to exclude
        """
        if drop_cols is None:
            drop_cols = []
        
        print(f"\nSeparating features and labels...")
        print(f"  Label column: {label_col}")
        print(f"  Dropping columns: {drop_cols}")
        
        self.X = []
        self.y = []
        
        for row in self.data:
            # Extract label
            label = row.get(label_col)
            self.y.append(int(label) if label else None)
            
            # Extract features
            features = {}
            for col, val in row.items():
                if col != label_col and col not in drop_cols:
                    # Try to convert to number
                    try:
                        features[col] = float(val)
                    except:
                        features[col] = val
            
            self.X.append(features)
        
        print(f"✓ Features: {len(self.X)} samples × {len(self.X[0])} features")
        print(f"✓ Labels: {len(self.y)} samples")
        
        return self.X, self.y
    
    def print_summary(self):
        """Print dataset summary"""
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        
        print(f"\nTotal samples: {len(self.X)}")
        print(f"Total features: {len(self.X[0]) if self.X else 0}")
        
        if self.X:
            print(f"\nFeatures: {list(self.X[0].keys())}")
        
        if self.y:
            label_counts = Counter(self.y)
            print(f"\nLabel distribution:")
            for label in sorted(label_counts.keys()):
                count = label_counts[label]
                pct = (count / len(self.y)) * 100
                label_name = "Safe" if label == 0 else "Phishing"
                bar = "█" * int(pct / 5)
                print(f"  {label_name:10s} ({label}): {count:3d} ({pct:5.1f}%) {bar}")
        
        print("="*60 + "\n")


def example_1_basic():
    """Example 1: Basic loading"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic CSV Loading")
    print("="*70)
    
    loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
    loader.load_csv()
    loader.print_info()


def example_2_separation():
    """Example 2: Feature separation"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Feature and Label Separation")
    print("="*70)
    
    loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
    loader.load_csv()
    
    X, y = loader.separate_features_labels(
        label_col='label',
        drop_cols=['url']
    )
    
    print(f"\nFeatures (first row):")
    if X:
        for col, val in X[0].items():
            print(f"  {col}: {val}")
    
    print(f"\nLabels (first 5): {y[:5]}")


def example_3_complete():
    """Example 3: Complete pipeline"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Complete Pipeline")
    print("="*70)
    
    loader = SimpleDataLoader('datasets/sample_phishing_data.csv')
    loader.load_csv()
    loader.print_info()
    X, y = loader.separate_features_labels(label_col='label', drop_cols=['url'])
    loader.print_summary()
    
    print("✓ Data ready for machine learning!")
    return X, y


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SIMPLE DATA LOADING DEMO")
    print("="*70)
    
    try:
        # Run examples
        example_1_basic()
        example_2_separation()
        X, y = example_3_complete()
        
        print(f"\n{'='*70}")
        print("QUICK TEST WITH BASIC PYTHON")
        print(f"{'='*70}")
        
        # Show data statistics using pure Python
        print(f"\nDataset Statistics (pure Python):")
        print(f"  Total samples: {len(X)}")
        print(f"  Total features per sample: {len(X[0])}")
        print(f"  Feature names: {list(X[0].keys())}")
        print(f"  Label distribution: {Counter(y)}")
        
        # Show class balance
        safe_count = sum(1 for label in y if label == 0)
        phishing_count = sum(1 for label in y if label == 1)
        total = len(y)
        
        print(f"\nClass Balance:")
        print(f"  Safe:      {safe_count}/{total} ({safe_count*100/total:.1f}%)")
        print(f"  Phishing:  {phishing_count}/{total} ({phishing_count*100/total:.1f}%)")
        
        print(f"\n{'='*70}")
        print("✓ SUCCESS! Data loaded and analyzed")
        print(f"{'='*70}\n")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure 'datasets/sample_phishing_data.csv' exists")
