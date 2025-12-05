import re
import os
import pandas as pd
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_query(query: str) -> str:
    """
    Cleans a GraphQL query by removing comments and excessive whitespace.
    """
    if not query:
        return ""
    
    # Remove comments
    query = re.sub(r'#.*', '', query)
    
    # Replace newlines and multiple spaces with a single space
    query = re.sub(r'\s+', ' ', query)
    
    return query.strip()

def normalize_query(query: str) -> str:
    """
    Normalizes a query for consistent parsing/hashing.
    """
    return clean_query(query)

def process_data(input_dir: str, output_dir: str):
    """
    Reads CSV files from input_dir, cleans queries, and saves to output_dir as Parquet.
    """
    if not os.path.exists(input_dir):
        logger.error(f"Input directory {input_dir} does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.endswith('.csv') or f.endswith('.xlsx')]
    
    if not files:
        logger.warning(f"No CSV or Excel files found in {input_dir}")
        return

    for file in files:
        input_path = os.path.join(input_dir, file)
        logger.info(f"Processing {input_path}...")
        
        try:
            if file.endswith('.csv'):
                df = pd.read_csv(input_path)
            else:
                df = pd.read_excel(input_path)
            
            # Map columns if needed (specific for NL2GQL dataset)
            if 'GT_GQL' in df.columns and 'query' not in df.columns:
                df.rename(columns={'GT_GQL': 'query'}, inplace=True)
                
            # Add missing columns with defaults
            if 'timestamp' not in df.columns:
                df['timestamp'] = datetime.now().isoformat()
            if 'client_id' not in df.columns:
                df['client_id'] = 'unknown'
            if 'ip' not in df.columns:
                df['ip'] = '127.0.0.1'
            if 'user_agent' not in df.columns:
                df['user_agent'] = 'batch_import'
            
            # Validate columns
            required_cols = ['timestamp', 'client_id', 'ip', 'user_agent', 'query']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                logger.warning(f"Skipping {file}: Missing columns {missing_cols}")
                continue
                
            # Clean queries
            df['cleaned_query'] = df['query'].apply(clean_query)
            
            # Save to Parquet
            output_filename = os.path.splitext(file)[0] + '.parquet'
            output_path = os.path.join(output_dir, output_filename)
            
            df.to_parquet(output_path, index=False)
            logger.info(f"Saved processed data to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to process {file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess real-world GraphQL logs")
    parser.add_argument("--input-dir", default="ml/data/real_world", help="Directory containing raw CSV logs")
    parser.add_argument("--output-dir", default="ml/data/processed", help="Directory to save processed Parquet files")
    
    args = parser.parse_args()
    process_data(args.input_dir, args.output_dir)
