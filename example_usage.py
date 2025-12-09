

"""
Example usage of the Codeforces Geometry Solver
Demonstrates how to use the system programmatically
"""

from dataset_loader import DatasetLoader
from model_interface import OllamaInterface
from code_executor import CodeExecutor
from evaluator import Evaluator
import json


def example_1_basic_evaluation():
    """Example 1: Basic evaluation with default settings"""
    print("="*60)
    print("EXAMPLE 1: Basic Evaluation")
    print("="*60 + "\n")
    
    evaluator = Evaluator(model_name="codellama")
    evaluator.evaluate_all_problems(max_problems=3)


def example_2_single_problem():
    """Example 2: Evaluate a single problem step by step"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Single Problem Step-by-Step")
    print("="*60 + "\n")
    
    # Load dataset
    loader = DatasetLoader()
    if not loader.load_dataset():
        return
    
    # Get geometry problems
    problems = loader.filter_geometry_problems()
    if not problems:
        print("No geometry problems found!")
        return
    
    # Take first problem
    problem = problems[0]
    details = loader.get_problem_details(problem)
    
    print(f"Problem: {details['id']}")
    print(f"Title: {details['title']}")
    print(f"Tags: {details['tags']}")
    print()
    
    # Generate solution
    model = OllamaInterface(model_name="codellama")
    if not model.check_connection():
        return
    
    print("Generating solution...")
    code = model.generate_solution(details)
    
    if code:
        print("\nGenerated code:")
        print("-" * 40)
        print(code)
        print("-" * 40)
        
        # Get test cases
        test_cases = loader.get_test_cases(problem)
        print(f"\nFound {len(test_cases)} test cases")
        
        # Execute tests
        executor = CodeExecutor()
        results = executor.run_all_tests(code, test_cases)
        
        print(f"\nResults: {results['passed']}/{results['total']} passed")
        print(f"Accuracy: {results['accuracy']:.2f}%")
    else:
        print("Failed to generate code")


def example_3_custom_prompt():
    """Example 3: Use custom prompt template"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Prompt Template")
    print("="*60 + "\n")
    
    loader = DatasetLoader()
    if not loader.load_dataset():
        return
    
    problems = loader.filter_geometry_problems()
    if not problems:
        return
    
    problem = problems[0]
    details = loader.get_problem_details(problem)
    
    # Custom prompt emphasizing geometry
    custom_prompt = f"""You are an expert in computational geometry and competitive programming.

Problem: {details['title']}

This is a geometry problem. Consider using:
- Mathematical formulas for areas, distances, angles
- Coordinate geometry techniques
- Vector operations if applicable

Problem Description:
{details['description']}

Input Format: {details['input_format']}
Output Format: {details['output_format']}

Examples:
{details['examples']}

Provide only Python code that solves this problem. Use clear variable names.
"""
    
    model = OllamaInterface(model_name="codellama")
    
    # Use custom prompt by manually calling the API
    print("Generating with custom prompt...")
    
    payload = {
        "model": model.model_name,
        "prompt": custom_prompt,
        "stream": False
    }
    
    import requests
    response = requests.post(model.generate_url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        code = model.extract_code(result.get('response', ''))
        
        if code:
            print("\nGenerated code with custom prompt:")
            print("-" * 40)
            print(code[:500] + "..." if len(code) > 500 else code)
            print("-" * 40)


def example_4_compare_models():
    """Example 4: Compare different models on same problem"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Compare Different Models")
    print("="*60 + "\n")
    
    loader = DatasetLoader()
    if not loader.load_dataset():
        return
    
    problems = loader.filter_geometry_problems()
    if not problems:
        return
    
    problem = problems[0]
    details = loader.get_problem_details(problem)
    test_cases = loader.get_test_cases(problem)
    
    print(f"Problem: {details['title']}\n")
    
    # Test with different models
    models_to_test = ["llama3.2", "codellama", "phi3"]
    executor = CodeExecutor()
    
    results_comparison = []
    
    for model_name in models_to_test:
        print(f"\nTesting with {model_name}...")
        model = OllamaInterface(model_name=model_name)
        
        if not model.check_model():
            print(f"  Skipping (model not available)")
            continue
        
        code = model.generate_solution(details)
        
        if code:
            test_results = executor.run_all_tests(code, test_cases[:2])  # Test first 2 only
            results_comparison.append({
                'model': model_name,
                'accuracy': test_results['accuracy'],
                'passed': test_results['passed'],
                'total': test_results['total']
            })
    
    # Print comparison
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    for result in results_comparison:
        print(f"{result['model']:15} | {result['passed']}/{result['total']} passed | "
              f"Accuracy: {result['accuracy']:.1f}%")


def example_5_export_results():
    """Example 5: Export and analyze results"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Export and Analyze Results")
    print("="*60 + "\n")
    
    evaluator = Evaluator(model_name="codellama")
    
    # Run evaluation
    evaluator.evaluate_all_problems(max_problems=5)
    
    # Custom analysis
    print("\nCustom Analysis:")
    print("-" * 40)
    
    # Find problems by difficulty (based on accuracy)
    easy = [r for r in evaluator.results if r['accuracy'] >= 80]
    medium = [r for r in evaluator.results if 50 <= r['accuracy'] < 80]
    hard = [r for r in evaluator.results if r['accuracy'] < 50]
    
    print(f"Easy problems (≥80%): {len(easy)}")
    print(f"Medium problems (50-80%): {len(medium)}")
    print(f"Hard problems (<50%): {len(hard)}")
    
    # Export to custom format
    custom_export = {
        'summary': {
            'total_problems': len(evaluator.results),
            'total_tests': sum(r['total_tests'] for r in evaluator.results),
            'total_passed': sum(r['tests_passed'] for r in evaluator.results)
        },
        'by_difficulty': {
            'easy': [r['problem_id'] for r in easy],
            'medium': [r['problem_id'] for r in medium],
            'hard': [r['problem_id'] for r in hard]
        }
    }
    
    with open('custom_analysis.json', 'w') as f:
        json.dump(custom_export, f, indent=2)
    
    print("\nCustom analysis saved to: custom_analysis.json")


def main():
    """Run all examples"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║           CODEFORCES GEOMETRY SOLVER - EXAMPLES          ║
╚═══════════════════════════════════════════════════════════╝

This script demonstrates various ways to use the solver.

Choose an example to run:
1. Basic evaluation (3 problems)
2. Single problem step-by-step
3. Custom prompt template
4. Compare different models
5. Export and analyze results
6. Run all examples

""")
    
    try:
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            example_1_basic_evaluation()
        elif choice == "2":
            example_2_single_problem()
        elif choice == "3":
            example_3_custom_prompt()
        elif choice == "4":
            example_4_compare_models()
        elif choice == "5":
            example_5_export_results()
        elif choice == "6":
            example_1_basic_evaluation()
            example_2_single_problem()
            example_3_custom_prompt()
            example_4_compare_models()
            example_5_export_results()
        else:
            print("Invalid choice!")
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")


if __name__ == "__main__":
    main()