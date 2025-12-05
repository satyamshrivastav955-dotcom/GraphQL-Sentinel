import pandas as pd
import os

file_path = "ml/data/real_world/NL2GQL_Testset_V20.1.xlsx"
try:
    df = pd.read_excel(file_path)
    print("--- COLUMNS ---")
    for col in df.columns:
        print(f"'{col}'")
    print("\n--- FIRST ROW SAMPLE ---")
    first_row = df.iloc[0]
    for col in df.columns:
        val = str(first_row[col])[:100] # First 100 chars
        print(f"{col}: {val}")
except Exception as e:
    print("Error:", e)
