from sklearn.preprocessing import LabelEncoder
import joblib
import os

class FeatureEncoder:
    def __init__(self):
        self.label_encoders = {}

    def fit_transform(self, df, columns):
        for col in columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
        return df

    def transform(self, df, columns):
        for col in columns:
            if col in self.label_encoders:
                le = self.label_encoders[col]
                # Handle unseen labels by assigning a default or skipping
                # For simplicity here, we might just use the same encoder
                # In production, handle unseen carefully
                pass 
        return df

    def save(self, path):
        joblib.dump(self.label_encoders, path)

    def load(self, path):
        self.label_encoders = joblib.load(path)
