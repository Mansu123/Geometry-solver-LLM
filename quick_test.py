

"""
Quick test script to verify setup
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    try:
        import datasets
        print("✓ datasets")
    except ImportError:
        print("✗ datasets - run: pip install datasets")
        return False
    
    try:
        import requests
        print("✓ requests")
    except ImportError:
        print("✗ requests - run: pip install requests")
        return False
    
    try:
        import pandas
        print("✓ pandas")
    except ImportError:
        print("✗ pandas - run: pip install pandas")
        return False
    
    try:
        import numpy
        print("✓ numpy")
    except ImportError:
        print("✗ numpy - run: pip install numpy")
        return False
    
    try:
        import tqdm
        print("✓ tqdm")
    except ImportError:
        print("✗ tqdm - run: pip install tqdm")
        return False
    
    print("\n✓ All imports successful!\n")
    return True


def test_ollama():
    """Test Ollama connection"""
    print("Testing Ollama connection...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✓ Ollama is running")
            print(f"✓ Available models: {[m['name'] for m in models]}")
            return True
        else:
            print("✗ Ollama returned an error")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama")
        print("  Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_dataset():
    """Test dataset access"""
    print("\nTesting dataset access...")
    
    try:
        from datasets import load_dataset
        print("  Loading dataset (this may take a minute)...")
        ds = load_dataset("open-r1/codeforces", "default", split="train", streaming=True)
        
        # Try to get first item
        first_item = next(iter(ds))
        print(f"✓ Dataset accessible")
        print(f"  First problem ID: {first_item.get('id', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"✗ Dataset error: {e}")
        print("  You may need to login to Hugging Face:")
        print("  huggingface-cli login")
        return False


def main():
    print("="*60)
    print("CODEFORCES GEOMETRY SOLVER - SETUP TEST")
    print("="*60)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test Ollama
    if not test_ollama():
        all_passed = False
        print()
    
    # Test dataset
    if not test_dataset():
        all_passed = False
    
    print()
    print("="*60)
    
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print()
        print("You're ready to run:")
        print("  python main.py --model codellama --max-problems 5")
        print()
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("="*60)
        print()
        print("Please fix the issues above before running the main script.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())