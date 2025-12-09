

"""
Configuration file for Codeforces Geometry Solver
"""

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL
DEFAULT_MODEL = "llama3.2"  # Change to your preferred model

# Dataset Configuration
DATASET_NAME = "open-r1/codeforces"
DATASET_CONFIG = "default"
TARGET_TAG = "geometry"

# Execution Configuration
EXECUTION_TIMEOUT = 10  # Seconds per test case
MAX_OUTPUT_LENGTH = 10000  # Maximum output length in characters

# Logging Configuration
LOG_FILE = "results.log"
RESULTS_CSV = "geometry_results.csv"

# Prompt Template
PROBLEM_PROMPT_TEMPLATE = """You are an expert competitive programmer. Solve the following Codeforces problem.

Problem: {title}

Description:
{description}

Input Format:
{input_format}

Output Format:
{output_format}

{note}

Examples:
{examples}

Please provide only the Python code solution. Do not include explanations, just the code that reads from stdin and writes to stdout.
Start your response with ```python and end with ```.
"""

# Code extraction pattern
CODE_BLOCK_PATTERN = r"```python\n(.*?)```"