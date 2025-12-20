# Codeforces Geometry Problem Solver with Ollama

An automated system that uses local LLMs (via Ollama) to solve geometry problems from the Codeforces dataset. Optimized for Mac M1 GPU.

## 🎯 Features

- ✅ Filters geometry problems from open-r1/codeforces dataset
- ✅ Generates solutions using any Ollama model
- ✅ Executes code against test cases
- ✅ Comprehensive logging and statistics
- ✅ Mac M1 GPU optimized
- ✅ Works with any Ollama model


## System Workflow
## 📈 SYSTEM WORKFLOW DIAGRAM
```
┌─────────────────────────────────────────────────┐
│ 1. DATASET LOADING                              │
│    - Load Codeforces problems                   │
│    - Filter for "geometry" tag                  │
│    - Extract 5 problems                         │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│ 2. PROBLEM PROCESSING (for each problem)       │
│    - Format problem details                     │
│    - Create prompt template                     │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│ 3. CODE GENERATION                              │
│    - Send prompt to Ollama                      │
│    - CodeLlama generates Python code            │
│    - Extract code from markdown                 │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│ 4. CODE EXECUTION                               │
│    - Create temp .py file                       │
│    - Run with test inputs                       │
│    - Capture output                             │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│ 5. OUTPUT COMPARISON                            │
│    - Normalize outputs (strip whitespace)       │
│    - Compare actual vs expected                 │
│    - Record PASS/FAIL                           │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│ 6. RESULTS AGGREGATION                          │
│    - Calculate accuracy per problem             │
│    - Calculate overall statistics               │
│    - Save to JSON and CSV              

## 📋 Prerequisites

- **Python 3.8+**
- **Ollama** installed and running
- **Mac M1** (or any system with Ollama support)

## 🚀 Installation

### 1. Install Ollama

```bash
# Install Ollama on Mac
brew install ollama

# Start Ollama service
ollama serve


 
```
# run it in a terminal keep it open and open new terminal then run below code

### 2. Pull a Model

```bash
# Recommended for coding tasks
ollama pull codellama

# Or use other models
ollama pull llama3.2
ollama pull deepseek-coder
ollama pull phi3
```

### 3. Setup Python Environment

```bash
# Clone or navigate to project directory
cd codeforces_geometry_solver

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install --break-system-packages -r requirements.txt

# Or if you're using venv:
pip install -r requirements.txt
```

## 📦 Project Structure

```
codeforces_geometry_solver/
│
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── dataset_loader.py      # Dataset loading and filtering
├── model_interface.py     # Ollama API integration
├── code_executor.py       # Safe code execution
├── evaluator.py          # Testing and evaluation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎮 Usage

### Basic Usage

```bash
# Run with default settings (llama3.2, all geometry problems)
python main.py

# Use specific model
python main.py --model codellama

# Limit number of problems
python main.py --model codellama --max-problems 10

#or try this
python main.py --model codellama:latest --max-problems 5

# Use custom Ollama server
python main.py --ollama-url http://192.168.1.100:11434
```

### Command Line Options

```bash
python main.py --help

Options:
  --model MODEL           Ollama model to use (default: llama3.2)
  --max-problems N        Maximum number of problems to evaluate
  --ollama-url URL        Ollama server URL (default: http://localhost:11434)
  --timeout SECONDS       Execution timeout per test (default: 10)
  --list-models          List available Ollama models
```

### Examples

```bash
# Evaluate first 5 problems with CodeLlama
python main.py --model codellama --max-problems 5

# Use DeepSeek Coder for better code generation
python main.py --model deepseek-coder

# Quick test with 3 problems
python main.py --max-problems 3

# List available models
python main.py --list-models
```

## 📊 Output

The script generates several output files:

1. **results_YYYYMMDD_HHMMSS.json** - Detailed results including generated code
2. **geometry_results.csv** - Summary CSV for easy analysis
3. **Console output** - Real-time progress and statistics

### Sample Output

```
[1/15] Problem: 1/A
Title: Theatre Square
Tags: ['geometry', 'math']
  Generating solution with codellama... ✓
  Testing with 3 test cases...
    Test 1: ✓ PASS (0.023s)
    Test 2: ✓ PASS (0.019s)
    Test 3: ✓ PASS (0.021s)
  Result: 3/3 tests passed (100.0%)
------------------------------------------------------------

EVALUATION SUMMARY
====================================================================
Total problems evaluated: 15
Code generated successfully: 15/15

Total test cases: 45
Tests passed: 38/45
Overall accuracy: 84.44%

Problems solved perfectly: 12/15
Average accuracy per problem: 84.44%
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Model settings
DEFAULT_MODEL = "codellama"  # Change default model
OLLAMA_BASE_URL = "http://localhost:11434"

# Execution settings
EXECUTION_TIMEOUT = 10  # Seconds per test case
MAX_OUTPUT_LENGTH = 10000

# Dataset settings
TARGET_TAG = "geometry"  # Change to filter other tags
```

## 🔧 Troubleshooting

### Ollama not connecting

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Model not found

```bash
# List available models
ollama list

# Pull missing model
ollama pull codellama
```

### Python package issues

```bash
# Mac M1 specific fix
pip install --break-system-packages datasets ollama pandas numpy tqdm

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dataset loading issues

```bash
# Login to Hugging Face (if needed)
huggingface-cli login

# Or set token in code
# from huggingface_hub import login
# login(token="your_token_here")
```

## 🧪 Testing Individual Components

### Test Dataset Loader

```bash
python dataset_loader.py
```

### Test Ollama Interface

```bash
python model_interface.py
```

### Test Code Executor

```bash
python code_executor.py
```

### Test Evaluator

```bash
python evaluator.py
```

## 🎯 Recommended Models

For coding tasks, these models work best:

1. **codellama** - Meta's specialized coding model (recommended)
2. **deepseek-coder** - Excellent for complex problems
3. **llama3.2** - Good general purpose model
4. **phi3** - Fast and efficient for simpler problems

```bash
# Pull recommended models
ollama pull codellama
ollama pull deepseek-coder
```

## 📈 Performance Tips

### Mac M1 Optimization

Ollama automatically uses the Metal framework for GPU acceleration on M1. No additional configuration needed!

### Speed up evaluation

```bash
# Use smaller, faster models for initial testing
python main.py --model phi3 --max-problems 5

# Use larger models for better accuracy
python main.py --model codellama --max-problems 50
```

### Reduce timeout for faster iteration

```bash
python main.py --timeout 5 --max-problems 10
```

## 🐛 Debugging

Enable verbose output by modifying code:

```python
# In model_interface.py
def generate_solution_streaming(self, problem_details: dict):
    # Use this for real-time model output
    pass
```

## 📝 License

This project uses the open-r1/codeforces dataset. Please respect Codeforces' terms of use.

## 🤝 Contributing

Feel free to submit issues or pull requests!

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Codeforces](https://codeforces.com/)
- [open-r1 Dataset](https://huggingface.co/datasets/open-r1/codeforces)

## ⚡ Quick Start Checklist

- [ ] Install Ollama: `brew install ollama`
- [ ] Start Ollama: `ollama serve`
- [ ] Pull a model: `ollama pull codellama`
- [ ] Install Python packages: `pip install -r requirements.txt`
- [ ] Run evaluation: `python main.py --max-problems 5`
- [ ] Check results: `cat geometry_results.csv`

## 💡 Tips

- Start with `--max-problems 5` to test your setup
- Use `codellama` or `deepseek-coder` for best coding results
- Check the JSON output for detailed error analysis
- The script automatically uses Mac M1 GPU through Ollama's Metal backend



