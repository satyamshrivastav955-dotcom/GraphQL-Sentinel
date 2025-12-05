from sklearn.model_selection import train_test_split
import pandas as pd

def split_data(df, target_col='label', test_size=0.2, val_size=0.1, random_state=42):
    """
    Splits dataframe into train, val, test.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # First split: Train + Val vs Test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Second split: Train vs Val
    # Adjust val_size to be relative to the original dataset
    relative_val_size = val_size / (1 - test_size)
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=relative_val_size, random_state=random_state, stratify=y_train_val
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test
