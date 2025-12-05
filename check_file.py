import os

def check_file():
    path = "backend/core/security_engine/scorer.py"
    print(f"--- CONTENT OF {path} ---")
    with open(path, 'r') as f:
        content = f.read()
        print(content)
    print("--- END OF FILE ---")
    
    if "HEURISTIC BOOSTS" in content:
        print("\nSUCCESS: File contains the fix (HEURISTIC BOOSTS).")
    else:
        print("\nFAILURE: File DOES NOT contain the fix.")

if __name__ == "__main__":
    check_file()
