
"""
Dataset loader module for filtering geometry problems from Codeforces dataset
"""

import json
from datasets import load_dataset
from typing import List, Dict
import config


class DatasetLoader:
    def __init__(self):
        self.dataset = None
        self.geometry_problems = []
    
    def load_dataset(self):
        """Load the Codeforces dataset"""
        print(f"Loading dataset: {config.DATASET_NAME}...")
        try:
            self.dataset = load_dataset(config.DATASET_NAME, config.DATASET_CONFIG)
            print(f"Dataset loaded successfully! Total problems: {len(self.dataset['train'])}")
            return True
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False
    
    def filter_geometry_problems(self):
        """Filter problems that have 'geometry' tag"""
        print(f"\nFiltering problems with '{config.TARGET_TAG}' tag...")
        
        if self.dataset is None:
            print("Dataset not loaded. Please load dataset first.")
            return []
        
        geometry_count = 0
        
        for problem in self.dataset['train']:
            tags = problem.get('tags', [])
            
            # Check if geometry tag exists
            if tags and config.TARGET_TAG in tags:
                self.geometry_problems.append(problem)
                geometry_count += 1
        
        print(f"Found {geometry_count} problems with '{config.TARGET_TAG}' tag")
        return self.geometry_problems
    
    def get_problem_details(self, problem: Dict) -> Dict:
        """Extract and format problem details"""
        examples_text = ""
        if problem.get('examples'):
            for idx, example in enumerate(problem['examples'], 1):
                examples_text += f"\nExample {idx}:\n"
                examples_text += f"Input:\n{example.get('input', 'N/A')}\n"
                examples_text += f"Output:\n{example.get('output', 'N/A')}\n"
        
        note_text = ""
        if problem.get('note'):
            note_text = f"\nNote:\n{problem['note']}"
        
        return {
            'id': problem.get('id', 'Unknown'),
            'title': problem.get('title', 'Untitled'),
            'description': problem.get('description', 'No description'),
            'input_format': problem.get('input_format', 'No input format specified'),
            'output_format': problem.get('output_format', 'No output format specified'),
            'note': note_text,
            'examples': examples_text,
            'examples_list': problem.get('examples', []),
            'official_tests': problem.get('official_tests', []),
            'time_limit': problem.get('time_limit', 1.0),
            'memory_limit': problem.get('memory_limit', 256),
            'tags': problem.get('tags', [])
        }
    
    def get_test_cases(self, problem: Dict) -> List[Dict]:
        """Extract test cases from problem"""
        test_cases = []
        
        # First add examples
        if problem.get('examples'):
            for example in problem['examples']:
                test_cases.append({
                    'input': example.get('input', ''),
                    'output': example.get('output', ''),
                    'type': 'example'
                })
        
        # Then add official tests if available
        if problem.get('official_tests'):
            for test in problem['official_tests']:
                test_cases.append({
                    'input': test.get('input', ''),
                    'output': test.get('output', ''),
                    'type': 'official'
                })
        
        return test_cases


if __name__ == "__main__":
    # Test the loader
    loader = DatasetLoader()
    if loader.load_dataset():
        problems = loader.filter_geometry_problems()
        print(f"\nFirst geometry problem:")
        if problems:
            details = loader.get_problem_details(problems[0])
            print(f"ID: {details['id']}")
            print(f"Title: {details['title']}")
            print(f"Tags: {details['tags']}")