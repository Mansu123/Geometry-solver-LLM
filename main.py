

"""
Main entry point for Codeforces Geometry Solver
"""

import argparse
import sys
from evaluator import Evaluator
import config


def main():
    parser = argparse.ArgumentParser(
        description='Solve Codeforces geometry problems using Ollama',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default model (llama3.2) on all geometry problems
  python main.py
  
  # Run with specific model
  python main.py --model codellama
  
  # Run on first 10 problems only
  python main.py --max-problems 10
  
  # Use different Ollama server
  python main.py --ollama-url http://localhost:11434
  
Available Ollama models for coding:
  - codellama (recommended for coding)
  - llama3.2
  - deepseek-coder
  - phi3
  - mistral
  
Make sure Ollama is running: ollama serve
Pull a model if needed: ollama pull codellama
        """
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default=config.DEFAULT_MODEL,
        help=f'Ollama model to use (default: {config.DEFAULT_MODEL})'
    )
    
    parser.add_argument(
        '--max-problems',
        type=int,
        default=None,
        help='Maximum number of problems to evaluate (default: all)'
    )
    
    parser.add_argument(
        '--ollama-url',
        type=str,
        default=config.OLLAMA_BASE_URL,
        help=f'Ollama server URL (default: {config.OLLAMA_BASE_URL})'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=config.EXECUTION_TIMEOUT,
        help=f'Execution timeout in seconds (default: {config.EXECUTION_TIMEOUT})'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available Ollama models and exit'
    )
    
    args = parser.parse_args()
    
    # Update config with command line arguments
    config.DEFAULT_MODEL = args.model
    config.OLLAMA_BASE_URL = args.ollama_url
    config.EXECUTION_TIMEOUT = args.timeout
    
    # List models if requested
    if args.list_models:
        from model_interface import OllamaInterface
        interface = OllamaInterface()
        if interface.check_connection():
            print("\nTo use a model, run:")
            print("  python main.py --model <model_name>")
        return
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║     CODEFORCES GEOMETRY PROBLEM SOLVER (OLLAMA)          ║
╚═══════════════════════════════════════════════════════════╝

Configuration:
  • Model: {args.model}
  • Ollama URL: {args.ollama_url}
  • Max problems: {args.max_problems if args.max_problems else 'All'}
  • Timeout: {args.timeout}s
  • Target tag: {config.TARGET_TAG}

""")
    
    # Create evaluator and run
    try:
        evaluator = Evaluator(model_name=args.model)
        success = evaluator.evaluate_all_problems(max_problems=args.max_problems)
        
        if success:
            print("\n✓ Evaluation completed successfully!")
            sys.exit(0)
        else:
            print("\n✗ Evaluation failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
