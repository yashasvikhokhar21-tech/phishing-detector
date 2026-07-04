"""
Data Preprocessing Tutorial and Example
Demonstrates how to use the DataLoader class for phishing dataset preparation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.data_loader import DataLoader
import pandas as pd


def example_1_basic_loading():
    """Example 1: Basic data loading and inspection"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Data Loading and Inspection")
    print("="*70)
    
    # Load the sample dataset
    loader = DataLoader('datasets/sample_phishing_data.csv')
    loader.load_data()
    loader.display_info()


def example_2_cleaning():
    """Example 2: Data cleaning with different strategies"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Data Cleaning")
    print("="*70)
    
    loader = DataLoader('datasets/sample_phishing_data.csv')
    loader.load_data()
    
    print("\n--- Strategy: Handle missing with mean ---")
    loader.clean_data(drop_duplicates=True, handle_missing='mean', label_column='label')
    
    # Show cleaned data
    print("✓ Data cleaned successfully")
    print(f"\nCleaned dataset shape: {loader.cleaned_data.shape}")


def example_3_feature_separation():
    """Example 3: Separate features and labels"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Feature and Label Separation")
    print("="*70)
    
    loader = DataLoader('datasets/sample_phishing_data.csv')
    loader.load_data()
    loader.clean_data(label_column='label')
    
    # Separate features and labels, exclude the 'url' column
    X, y = loader.separate_features_and_labels(
        label_column='label',
        drop_columns=['url']  # Don't include URL in features
    )
    
    print(f"\n✓ Separation complete!")
    print(f"\nFeatures shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    
    # Show sample data
    print("\n--- First 5 rows of features (X) ---")
    print(X.head())
    
    print("\n--- First 5 labels (y) ---")
    print(y.head())


def example_4_complete_pipeline():
    """Example 4: Complete preprocessing pipeline"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Complete Preprocessing Pipeline")
    print("="*70)
    
    # Initialize loader with dataset
    dataset_path = 'datasets/sample_phishing_data.csv'
    loader = DataLoader(dataset_path)
    
    # Step 1: Load raw data
    print("\n[Step 1] Loading data...")
    loader.load_data()
    
    # Step 2: Inspect raw data
    print("\n[Step 2] Inspecting raw data...")
    loader.display_info()
    
    # Step 3: Clean data
    print("\n[Step 3] Cleaning data...")
    loader.clean_data(
        drop_duplicates=True,
        handle_missing='mean',
        label_column='label'
    )
    
    # Step 4: Separate features and labels
    print("\n[Step 4] Separating features and labels...")
    X, y = loader.separate_features_and_labels(
        label_column='label',
        drop_columns=['url']
    )
    
    # Step 5: Print summary
    print("\n[Step 5] Dataset Summary")
    loader.print_summary()
    
    print("✓ Complete preprocessing pipeline executed successfully!")
    
    return loader, X, y


def example_5_analysis():
    """Example 5: Data analysis and statistics"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Data Analysis and Statistics")
    print("="*70)
    
    loader, X, y = example_4_complete_pipeline()
    
    print("\n--- Feature Statistics ---")
    print(X.describe())
    
    print("\n--- Data Types ---")
    print(X.dtypes)
    
    print("\n--- Feature Correlation ---")
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    corr_matrix = X[numeric_features].corr()
    print(corr_matrix)
    
    print("\n--- Label Balance ---")
    label_counts = y.value_counts()
    print(f"Safe (0):      {label_counts.get(0, 0)} samples")
    print(f"Phishing (1):  {label_counts.get(1, 0)} samples")
    
    if len(y) > 0:
        safe_pct = (label_counts.get(0, 0) / len(y)) * 100
        phishing_pct = (label_counts.get(1, 0) / len(y)) * 100
        print(f"\nBalance: {safe_pct:.1f}% safe, {phishing_pct:.1f}% phishing")


def example_6_custom_preprocessing():
    """Example 6: Custom preprocessing with specific requirements"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Custom Preprocessing")
    print("="*70)
    
    loader = DataLoader('datasets/sample_phishing_data.csv')
    loader.load_data()
    
    # Clean with specific strategy
    print("\nCleaning with custom strategy:")
    print("  - Drop duplicates: Yes")
    print("  - Handle missing: median")
    print("  - Label column: label")
    
    loader.clean_data(
        drop_duplicates=True,
        handle_missing='median',
        label_column='label'
    )
    
    # Separate with specific columns to drop
    print("\nSeparating features:")
    print("  - Dropping columns: ['url']")
    
    X, y = loader.separate_features_and_labels(
        label_column='label',
        drop_columns=['url']
    )
    
    print(f"\n✓ Custom preprocessing complete")
    print(f"  Features: {X.shape}")
    print(f"  Labels: {y.shape}")


def show_menu():
    """Display example menu"""
    print("\n" + "="*70)
    print("DATA PREPROCESSING EXAMPLES")
    print("="*70)
    print("\n1. Basic Data Loading")
    print("2. Data Cleaning")
    print("3. Feature Separation")
    print("4. Complete Pipeline")
    print("5. Data Analysis")
    print("6. Custom Preprocessing")
    print("7. Run All Examples")
    print("0. Exit")
    print("-" * 70)


def main():
    """Run selected examples"""
    
    # Check if dataset exists
    if not os.path.exists('datasets/sample_phishing_data.csv'):
        print("✗ Sample dataset not found!")
        print("Please ensure 'datasets/sample_phishing_data.csv' exists")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("\nSelect example (0-7): ").strip()
            
            if choice == '1':
                example_1_basic_loading()
            elif choice == '2':
                example_2_cleaning()
            elif choice == '3':
                example_3_feature_separation()
            elif choice == '4':
                example_4_complete_pipeline()
            elif choice == '5':
                example_5_analysis()
            elif choice == '6':
                example_6_custom_preprocessing()
            elif choice == '7':
                example_1_basic_loading()
                example_2_cleaning()
                example_3_feature_separation()
                example_4_complete_pipeline()
                example_5_analysis()
                example_6_custom_preprocessing()
            elif choice == '0':
                print("\nExiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Run quick demo if no interactive choice
    print("\n" + "="*70)
    print("🔄 QUICK DEMO: Complete Preprocessing Pipeline")
    print("="*70)
    
    try:
        loader, X, y = example_4_complete_pipeline()
        
        print("\n" + "="*70)
        print("READY TO USE")
        print("="*70)
        print("\nYour dataset is ready!")
        print(f"Features (X): {X.shape[0]} samples × {X.shape[1]} features")
        print(f"Labels (y):   {y.shape[0]} samples")
        print("\nYou can now use X and y for machine learning:")
        print("  - Train test split")
        print("  - Model training")
        print("  - Cross-validation")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error running demo: {e}")
        import traceback
        traceback.print_exc()
