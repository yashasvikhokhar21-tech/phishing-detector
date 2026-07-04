"""
Data Loader and Preprocessing Module
Handles CSV dataset loading, cleaning, and feature engineering for phishing detection
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
import os


class DataLoader:
    """Load and preprocess phishing detection datasets"""
    
    def __init__(self, filepath: str):
        """
        Initialize the data loader
        
        Args:
            filepath (str): Path to CSV file containing the dataset
        """
        self.filepath = filepath
        self.raw_data = None
        self.cleaned_data = None
        self.X = None
        self.y = None
        self.feature_columns = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load dataset from CSV file
        
        Returns:
            pd.DataFrame: Raw dataset
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Dataset file not found: {self.filepath}")
        
        try:
            self.raw_data = pd.read_csv(self.filepath)
            print(f"✓ Dataset loaded: {self.filepath}")
            print(f"  Shape: {self.raw_data.shape[0]} rows × {self.raw_data.shape[1]} columns")
            return self.raw_data
        except Exception as e:
            print(f"✗ Error loading dataset: {e}")
            raise
    
    def display_info(self) -> None:
        """Display basic information about the dataset"""
        if self.raw_data is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*60)
        print("DATASET INFORMATION")
        print("="*60)
        
        print(f"\nShape: {self.raw_data.shape[0]} rows, {self.raw_data.shape[1]} columns")
        
        print("\nColumn Names and Types:")
        print("-" * 60)
        for col, dtype in self.raw_data.dtypes.items():
            print(f"  {col:30s} : {dtype}")
        
        print("\nMissing Values:")
        print("-" * 60)
        missing = self.raw_data.isnull().sum()
        if missing.sum() == 0:
            print("  No missing values found ✓")
        else:
            for col, count in missing[missing > 0].items():
                percentage = (count / len(self.raw_data)) * 100
                print(f"  {col:30s} : {count:5d} ({percentage:5.2f}%)")
        
        print("\nFirst Few Rows:")
        print("-" * 60)
        print(self.raw_data.head())
        
        print("\nBasic Statistics:")
        print("-" * 60)
        print(self.raw_data.describe())
        print("="*60 + "\n")
    
    def clean_data(self, 
                   drop_duplicates: bool = True,
                   handle_missing: str = 'mean',
                   label_column: str = 'label') -> pd.DataFrame:
        """
        Clean and preprocess the dataset
        
        Args:
            drop_duplicates (bool): Remove duplicate rows
            handle_missing (str): Strategy for missing values
                - 'mean': Fill numeric with mean
                - 'median': Fill numeric with median
                - 'drop': Drop rows with missing values
                - 'forward': Forward fill
            label_column (str): Name of the label column
            
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Create a copy to avoid modifying original
        self.cleaned_data = self.raw_data.copy()
        
        print("\n" + "="*60)
        print("CLEANING DATA")
        print("="*60)
        
        # Check for label column
        if label_column not in self.cleaned_data.columns:
            raise ValueError(f"Label column '{label_column}' not found in dataset")
        
        # Store original shape
        original_shape = self.cleaned_data.shape
        
        # 1. Remove duplicates
        if drop_duplicates:
            before = len(self.cleaned_data)
            self.cleaned_data = self.cleaned_data.drop_duplicates()
            after = len(self.cleaned_data)
            if before > after:
                print(f"✓ Removed {before - after} duplicate rows")
        
        # 2. Handle missing values
        if self.cleaned_data.isnull().sum().sum() > 0:
            print(f"\nHandling missing values with strategy: '{handle_missing}'")
            
            if handle_missing == 'drop':
                before = len(self.cleaned_data)
                self.cleaned_data = self.cleaned_data.dropna()
                print(f"✓ Dropped {before - len(self.cleaned_data)} rows with missing values")
            
            elif handle_missing == 'mean':
                numeric_cols = self.cleaned_data.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if self.cleaned_data[col].isnull().sum() > 0:
                        mean_val = self.cleaned_data[col].mean()
                        self.cleaned_data[col].fillna(mean_val, inplace=True)
                        print(f"✓ Filled {col} with mean: {mean_val:.4f}")
                
                # Handle categorical columns
                categorical_cols = self.cleaned_data.select_dtypes(include=['object']).columns
                for col in categorical_cols:
                    if col != label_column and self.cleaned_data[col].isnull().sum() > 0:
                        mode_val = self.cleaned_data[col].mode()[0]
                        self.cleaned_data[col].fillna(mode_val, inplace=True)
                        print(f"✓ Filled {col} with mode: {mode_val}")
            
            elif handle_missing == 'median':
                numeric_cols = self.cleaned_data.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if self.cleaned_data[col].isnull().sum() > 0:
                        median_val = self.cleaned_data[col].median()
                        self.cleaned_data[col].fillna(median_val, inplace=True)
                        print(f"✓ Filled {col} with median: {median_val:.4f}")
            
            elif handle_missing == 'forward':
                self.cleaned_data = self.cleaned_data.fillna(method='ffill')
                self.cleaned_data = self.cleaned_data.fillna(method='bfill')
                print(f"✓ Applied forward fill strategy")
            
            else:
                print(f"⚠ Unknown strategy: {handle_missing}")
        
        else:
            print("✓ No missing values found")
        
        print(f"\nFinal shape: {self.cleaned_data.shape[0]} rows × {self.cleaned_data.shape[1]} columns")
        print("="*60 + "\n")
        
        return self.cleaned_data
    
    def separate_features_and_labels(self, 
                                     label_column: str = 'label',
                                     drop_columns: Optional[list] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features (X) and labels (y) from dataset
        
        Args:
            label_column (str): Name of the label column
            drop_columns (list): Additional columns to drop from features
                                (e.g., ['id', 'timestamp'])
            
        Returns:
            Tuple[pd.DataFrame, pd.Series]: (Features X, Labels y)
        """
        if self.cleaned_data is None:
            raise ValueError("No cleaned data. Call clean_data() first.")
        
        if label_column not in self.cleaned_data.columns:
            raise ValueError(f"Label column '{label_column}' not found")
        
        print("\n" + "="*60)
        print("SEPARATING FEATURES AND LABELS")
        print("="*60)
        
        # Extract labels
        self.y = self.cleaned_data[label_column].copy()
        
        # Extract features
        self.X = self.cleaned_data.drop(columns=[label_column])
        
        # Drop additional columns if specified
        if drop_columns:
            columns_to_drop = [col for col in drop_columns if col in self.X.columns]
            if columns_to_drop:
                self.X = self.X.drop(columns=columns_to_drop)
                print(f"✓ Dropped columns: {columns_to_drop}")
        
        # Store feature column names
        self.feature_columns = self.X.columns.tolist()
        
        print(f"\nFeatures (X):")
        print(f"  Shape: {self.X.shape}")
        print(f"  Columns ({len(self.feature_columns)}): {self.feature_columns[:5]}...")
        
        print(f"\nLabels (y):")
        print(f"  Shape: {self.y.shape}")
        print(f"  Values: {self.y.unique()}")
        print(f"  Distribution:")
        for label_val in sorted(self.y.unique()):
            count = (self.y == label_val).sum()
            percentage = (count / len(self.y)) * 100
            label_name = "Safe" if label_val == 0 else "Phishing"
            print(f"    {label_name} ({label_val}): {count:5d} ({percentage:5.2f}%)")
        
        print("="*60 + "\n")
        
        return self.X, self.y
    
    def get_dataset_summary(self) -> dict:
        """
        Get a summary of the dataset
        
        Returns:
            dict: Dictionary containing dataset statistics
        """
        if self.X is None or self.y is None:
            raise ValueError("Dataset not properly prepared. Call separate_features_and_labels() first.")
        
        return {
            'total_samples': len(self.X),
            'total_features': len(self.feature_columns),
            'feature_names': self.feature_columns,
            'label_distribution': self.y.value_counts().to_dict(),
            'missing_values': self.X.isnull().sum().sum(),
            'duplicate_rows': self.X.duplicated().sum(),
            'numeric_features': self.X.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_features': self.X.select_dtypes(include=['object']).columns.tolist(),
        }
    
    def print_summary(self) -> None:
        """Print a nice summary of the dataset"""
        summary = self.get_dataset_summary()
        
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        
        print(f"\nSample Size:        {summary['total_samples']}")
        print(f"Total Features:     {summary['total_features']}")
        print(f"Missing Values:     {summary['missing_values']}")
        print(f"Duplicate Rows:     {summary['duplicate_rows']}")
        
        print(f"\nNumeric Features ({len(summary['numeric_features'])}):")
        for feat in summary['numeric_features'][:5]:
            print(f"  - {feat}")
        if len(summary['numeric_features']) > 5:
            print(f"  ... and {len(summary['numeric_features']) - 5} more")
        
        print(f"\nCategorical Features ({len(summary['categorical_features'])}):")
        for feat in summary['categorical_features'][:5]:
            print(f"  - {feat}")
        if len(summary['categorical_features']) > 5:
            print(f"  ... and {len(summary['categorical_features']) - 5} more")
        
        print(f"\nClass Distribution:")
        for label_val, count in sorted(summary['label_distribution'].items()):
            percentage = (count / summary['total_samples']) * 100
            label_name = "Safe" if label_val == 0 else "Phishing"
            bar = "█" * int(percentage / 2)
            print(f"  {label_name:10s} ({label_val}): {count:6d} ({percentage:5.2f}%) {bar}")
        
        print("="*60 + "\n")
    
    def save_processed_data(self, 
                           X_path: str = 'data/X_processed.csv',
                           y_path: str = 'data/y_processed.csv') -> None:
        """
        Save processed features and labels to CSV files
        
        Args:
            X_path (str): Path to save features
            y_path (str): Path to save labels
        """
        if self.X is None or self.y is None:
            raise ValueError("No processed data to save. Call separate_features_and_labels() first.")
        
        # Create data directory if needed
        os.makedirs(os.path.dirname(X_path) or '.', exist_ok=True)
        
        self.X.to_csv(X_path, index=False)
        self.y.to_csv(y_path, index=False)
        
        print(f"✓ Saved features to: {X_path}")
        print(f"✓ Saved labels to: {y_path}")


def main():
    """Example usage of DataLoader"""
    
    # Example dataset path - adjust based on your actual dataset location
    dataset_path = 'datasets/phishing_urls.csv'
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"⚠ Dataset not found at: {dataset_path}")
        print("\nTo use this script:")
        print("1. Place your CSV file at: datasets/phishing_urls.csv")
        print("2. Ensure it has a 'label' column (0=safe, 1=phishing)")
        print("3. Run this script again")
        print("\nExample CSV structure:")
        print("  url,label")
        print("  https://google.com,0")
        print("  https://phishing-site.com,1")
        return
    
    # Initialize loader
    loader = DataLoader(dataset_path)
    
    # Step 1: Load data
    loader.load_data()
    
    # Step 2: Display raw data info
    loader.display_info()
    
    # Step 3: Clean data
    loader.clean_data(drop_duplicates=True, handle_missing='mean', label_column='label')
    
    # Step 4: Separate features and labels
    X, y = loader.separate_features_and_labels(label_column='label', drop_columns=['url', 'id'])
    
    # Step 5: Print summary
    loader.print_summary()
    
    # Step 6: Optional - Save processed data
    # loader.save_processed_data()
    
    print("✓ Data preprocessing complete!")
    print(f"\nYou can now use:")
    print(f"  X = {X.shape}  (features)")
    print(f"  y = {y.shape}  (labels)")


if __name__ == "__main__":
    main()
