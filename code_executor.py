

"""
Code executor module for safely running generated code against test cases
"""

import subprocess
import tempfile
import os
import time
from typing import Dict, Optional, Tuple
import config


class CodeExecutor:
    def __init__(self, timeout: int = config.EXECUTION_TIMEOUT):
        self.timeout = timeout
    
    def execute_code(self, code: str, test_input: str) -> Dict:
        """
        Execute Python code with given input
        Returns dict with: success, output, error, time_taken
        """
        result = {
            'success': False,
            'output': '',
            'error': '',
            'time_taken': 0.0,
            'timeout': False
        }
        
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            code_file = f.name
        
        try:
            start_time = time.time()
            
            # Execute code with input
            process = subprocess.Popen(
                ['python3', code_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(
                    input=test_input,
                    timeout=self.timeout
                )
                
                end_time = time.time()
                result['time_taken'] = end_time - start_time
                
                if process.returncode == 0:
                    result['success'] = True
                    result['output'] = stdout.strip()
                else:
                    result['error'] = stderr.strip()
                    
            except subprocess.TimeoutExpired:
                process.kill()
                result['timeout'] = True
                result['error'] = f"Execution timeout ({self.timeout}s)"
                
        except Exception as e:
            result['error'] = f"Execution error: {str(e)}"
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(code_file)
            except:
                pass
        
        return result
    
    def normalize_output(self, output: str) -> str:
        """Normalize output for comparison"""
        # Strip whitespace from each line and remove empty lines
        lines = [line.strip() for line in output.strip().split('\n')]
        lines = [line for line in lines if line]
        return '\n'.join(lines)
    
    def compare_outputs(self, actual: str, expected: str) -> bool:
        """Compare actual output with expected output"""
        actual_norm = self.normalize_output(actual)
        expected_norm = self.normalize_output(expected)
        
        return actual_norm == expected_norm
    
    def run_test_case(self, code: str, test_case: Dict) -> Dict:
        """Run a single test case and return detailed results"""
        test_input = test_case['input']
        expected_output = test_case['output']
        
        # Execute code
        exec_result = self.execute_code(code, test_input)
        
        # Compare outputs
        passed = False
        if exec_result['success']:
            passed = self.compare_outputs(exec_result['output'], expected_output)
        
        return {
            'passed': passed,
            'expected': expected_output,
            'actual': exec_result['output'],
            'error': exec_result['error'],
            'time_taken': exec_result['time_taken'],
            'timeout': exec_result['timeout']
        }
    
    def run_all_tests(self, code: str, test_cases: list) -> Dict:
        """Run all test cases and return aggregated results"""
        if not test_cases:
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'accuracy': 0.0,
                'details': []
            }
        
        results = {
            'total': len(test_cases),
            'passed': 0,
            'failed': 0,
            'accuracy': 0.0,
            'details': []
        }
        
        for idx, test_case in enumerate(test_cases, 1):
            test_result = self.run_test_case(code, test_case)
            
            if test_result['passed']:
                results['passed'] += 1
                print(f"    Test {idx}: ✓ PASS ({test_result['time_taken']:.3f}s)")
            else:
                results['failed'] += 1
                if test_result['timeout']:
                    print(f"    Test {idx}: ✗ TIMEOUT")
                elif test_result['error']:
                    print(f"    Test {idx}: ✗ ERROR - {test_result['error'][:50]}")
                else:
                    print(f"    Test {idx}: ✗ WRONG ANSWER")
            
            results['details'].append({
                'test_number': idx,
                'test_type': test_case.get('type', 'unknown'),
                **test_result
            })
        
        results['accuracy'] = (results['passed'] / results['total']) * 100
        
        return results


if __name__ == "__main__":
    # Test the executor
    executor = CodeExecutor()
    
    # Simple test
    test_code = """
a, b = map(int, input().split())
print(a + b)
"""
    
    test_case = {
        'input': '3 5',
        'output': '8'
    }
    
    result = executor.run_test_case(test_code, test_case)
    print(f"Test passed: {result['passed']}")
    print(f"Expected: {result['expected']}")
    print(f"Actual: {result['actual']}")