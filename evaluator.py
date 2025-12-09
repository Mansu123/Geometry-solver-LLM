
"""
Evaluator module to test generated solutions and compute statistics
"""

import json
import csv
from datetime import datetime
from typing import List, Dict
import config
from dataset_loader import DatasetLoader
from model_interface import OllamaInterface
from code_executor import CodeExecutor


class Evaluator:
    def __init__(self, model_name: str = config.DEFAULT_MODEL):
        self.loader = DatasetLoader()
        self.model = OllamaInterface(model_name)
        self.executor = CodeExecutor()
        self.results = []
    
    def evaluate_all_problems(self, max_problems: int = None):
        """Evaluate all geometry problems"""
        print("="*60)
        print("CODEFORCES GEOMETRY SOLVER EVALUATION")
        print("="*60)
        
        # Check Ollama connection
        if not self.model.check_connection():
            return False
        
        if not self.model.check_model():
            return False
        
        # Load dataset
        if not self.loader.load_dataset():
            return False
        
        # Filter geometry problems
        problems = self.loader.filter_geometry_problems()
        
        if not problems:
            print("No geometry problems found!")
            return False
        
        # Limit number of problems if specified
        if max_problems:
            problems = problems[:max_problems]
            print(f"\nEvaluating first {max_problems} problems...")
        
        print("\n" + "="*60)
        print("STARTING EVALUATION")
        print("="*60 + "\n")
        
        # Evaluate each problem
        for idx, problem in enumerate(problems, 1):
            print(f"\n[{idx}/{len(problems)}] Problem: {problem.get('id', 'Unknown')}")
            print(f"Title: {problem.get('title', 'Untitled')}")
            print(f"Tags: {problem.get('tags', [])}")
            
            result = self.evaluate_problem(problem)
            self.results.append(result)
            
            # Print summary for this problem
            if result['code_generated']:
                print(f"  Result: {result['tests_passed']}/{result['total_tests']} tests passed "
                      f"({result['accuracy']:.1f}%)")
            else:
                print(f"  Result: Failed to generate code")
            
            print("-"*60)
        
        # Print final summary
        self.print_summary()
        
        # Save results
        self.save_results()
        
        return True
    
    def evaluate_problem(self, problem: Dict) -> Dict:
        """Evaluate a single problem"""
        result = {
            'problem_id': problem.get('id', 'Unknown'),
            'title': problem.get('title', 'Untitled'),
            'tags': problem.get('tags', []),
            'code_generated': False,
            'code': '',
            'total_tests': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'accuracy': 0.0,
            'error': '',
            'timestamp': datetime.now().isoformat()
        }
        
        # Get problem details
        details = self.loader.get_problem_details(problem)
        
        # Generate solution
        code = self.model.generate_solution(details)
        
        if not code:
            result['error'] = 'Failed to generate code'
            return result
        
        result['code_generated'] = True
        result['code'] = code
        
        # Get test cases
        test_cases = self.loader.get_test_cases(problem)
        
        if not test_cases:
            result['error'] = 'No test cases available'
            return result
        
        print(f"  Testing with {len(test_cases)} test cases...")
        
        # Run tests
        test_results = self.executor.run_all_tests(code, test_cases)
        
        result['total_tests'] = test_results['total']
        result['tests_passed'] = test_results['passed']
        result['tests_failed'] = test_results['failed']
        result['accuracy'] = test_results['accuracy']
        result['test_details'] = test_results['details']
        
        return result
    
    def print_summary(self):
        """Print evaluation summary"""
        print("\n" + "="*60)
        print("EVALUATION SUMMARY")
        print("="*60)
        
        total_problems = len(self.results)
        problems_with_code = sum(1 for r in self.results if r['code_generated'])
        
        total_tests = sum(r['total_tests'] for r in self.results)
        total_passed = sum(r['tests_passed'] for r in self.results)
        
        print(f"\nTotal problems evaluated: {total_problems}")
        print(f"Code generated successfully: {problems_with_code}/{total_problems}")
        print(f"\nTotal test cases: {total_tests}")
        print(f"Tests passed: {total_passed}/{total_tests}")
        
        if total_tests > 0:
            overall_accuracy = (total_passed / total_tests) * 100
            print(f"Overall accuracy: {overall_accuracy:.2f}%")
        
        # Problems with 100% accuracy
        perfect_problems = sum(1 for r in self.results if r['accuracy'] == 100.0 and r['total_tests'] > 0)
        print(f"\nProblems solved perfectly: {perfect_problems}/{total_problems}")
        
        # Average accuracy
        if problems_with_code > 0:
            avg_accuracy = sum(r['accuracy'] for r in self.results if r['code_generated']) / problems_with_code
            print(f"Average accuracy per problem: {avg_accuracy:.2f}%")
        
        print("\n" + "="*60)
    
    def save_results(self):
        """Save results to files"""
        # Save detailed JSON
        json_file = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed results saved to: {json_file}")
        
        # Save CSV summary
        csv_file = config.RESULTS_CSV
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'problem_id', 'title', 'code_generated', 'total_tests',
                'tests_passed', 'tests_failed', 'accuracy'
            ])
            writer.writeheader()
            for r in self.results:
                writer.writerow({
                    'problem_id': r['problem_id'],
                    'title': r['title'],
                    'code_generated': r['code_generated'],
                    'total_tests': r['total_tests'],
                    'tests_passed': r['tests_passed'],
                    'tests_failed': r['tests_failed'],
                    'accuracy': r['accuracy']
                })
        print(f"Summary saved to: {csv_file}")
    
    def save_failed_cases(self):
        """Save problems where solution failed"""
        failed = [r for r in self.results if r['accuracy'] < 100.0 or not r['code_generated']]
        
        if failed:
            failed_file = f"failed_problems_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(failed_file, 'w') as f:
                json.dump(failed, f, indent=2)
            print(f"Failed problems saved to: {failed_file}")


if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.evaluate_all_problems(max_problems=5)  # Test with first 5 problems