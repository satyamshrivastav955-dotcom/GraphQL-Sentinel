import argparse
import json
import random
import time
import uuid
import os
from datetime import datetime, timedelta
import pandas as pd

# Constants
BENIGN_RATIO = 0.8
ATTACK_TYPES = ['deep_nesting', 'circular_introspection', 'batching', 'alias_overload']

# Templates
BENIGN_TEMPLATES = [
    "query { user(id: \"$ID\") { name email } }",
    "query { posts(limit: 10) { id title content author { name } } }",
    "mutation { updateProfile(name: \"$NAME\") { id name } }",
    "query { search(term: \"$TERM\") { ... on User { name } ... on Post { title } } }",
    "query { me { id preferences { theme notifications } } }"
]

def generate_benign_query():
    template = random.choice(BENIGN_TEMPLATES)
    # Simple replacement for variety
    template = template.replace("$ID", str(uuid.uuid4()))
    template = template.replace("$NAME", f"User_{random.randint(1, 1000)}")
    template = template.replace("$TERM", f"Search_{random.randint(1, 100)}")
    return template

def generate_deep_nesting(depth=20):
    query = "user { " * depth + "name" + " }" * depth
    return "query { " + query + " }"

def generate_circular_introspection():
    return """
    query IntrospectionQuery {
      __schema {
        types {
          fields {
            type {
              fields {
                type {
                  fields {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """

def generate_batching(count=15):
    queries = []
    for i in range(count):
        queries.append(f"q{i}: user(id: \"{i}\") {{ name }}")
    return "query { " + " ".join(queries) + " }"

def generate_alias_overload(count=50):
    fields = []
    for i in range(count):
        fields.append(f"alias_{i}: fieldName")
    return "query { " + " ".join(fields) + " }"

def generate_attack_query(attack_type):
    if attack_type == 'deep_nesting':
        return generate_deep_nesting(random.randint(15, 50))
    elif attack_type == 'circular_introspection':
        return generate_circular_introspection()
    elif attack_type == 'batching':
        return generate_batching(random.randint(10, 30))
    elif attack_type == 'alias_overload':
        return generate_alias_overload(random.randint(30, 100))
    return generate_benign_query()

def generate_dataset(n, seed, output_dir):
    random.seed(seed)
    data = []
    
    start_time = datetime.now() - timedelta(days=7)
    
    print(f"Generating {n} queries...")
    
    for i in range(n):
        is_attack = random.random() > BENIGN_RATIO
        
        if is_attack:
            attack_type = random.choice(ATTACK_TYPES)
            query = generate_attack_query(attack_type)
            label = 1
            category = attack_type
        else:
            query = generate_benign_query()
            label = 0
            category = "benign"
            
        timestamp = start_time + timedelta(seconds=i*0.5) # roughly 2 queries per second avg
        
        record = {
            "timestamp": timestamp.isoformat(),
            "client_id": f"client_{random.randint(1, 100)}",
            "ip": f"192.168.1.{random.randint(1, 255)}",
            "user_agent": "Mozilla/5.0 (Synthetic)",
            "query": query,
            "label": label,
            "category": category
        }
        data.append(record)
        
        if (i + 1) % 10000 == 0:
            print(f"Generated {i + 1} queries")

    # Save to Parquet
    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(data)
    output_path = os.path.join(output_dir, "synthetic_data.parquet")
    df.to_parquet(output_path)
    print(f"Saved dataset to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic GraphQL query dataset")
    parser.add_argument("--n", type=int, default=10000, help="Number of queries to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output-dir", type=str, default="ml/data/synthetic_1M", help="Output directory")
    
    args = parser.parse_args()
    generate_dataset(args.n, args.seed, args.output_dir)
