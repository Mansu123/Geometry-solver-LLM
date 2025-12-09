

"""
Model interface module for interacting with Ollama
"""

import requests
import json
import re
from typing import Optional
import config


class OllamaInterface:
    def __init__(self, model_name: str = config.DEFAULT_MODEL, base_url: str = config.OLLAMA_BASE_URL):
        self.model_name = model_name
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Connected to Ollama at {self.base_url}")
                models = response.json().get('models', [])
                print(f"✓ Available models: {[m['name'] for m in models]}")
                return True
            else:
                print(f"✗ Failed to connect to Ollama (status {response.status_code})")
                return False
        except Exception as e:
            print(f"✗ Cannot connect to Ollama: {e}")
            print("Make sure Ollama is running: 'ollama serve'")
            return False
    
    def check_model(self) -> bool:
        """Check if the specified model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if self.model_name in model_names:
                    print(f"✓ Model '{self.model_name}' is available")
                    return True
                else:
                    print(f"✗ Model '{self.model_name}' not found")
                    print(f"Available models: {model_names}")
                    print(f"To pull model: 'ollama pull {self.model_name}'")
                    return False
        except Exception as e:
            print(f"Error checking model: {e}")
            return False
    
    def generate_solution(self, problem_details: dict) -> Optional[str]:
        """Generate code solution for a given problem"""
        try:
            # Format the prompt
            prompt = config.PROBLEM_PROMPT_TEMPLATE.format(**problem_details)
            
            # Prepare request
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 2048
                }
            }
            
            print(f"  Generating solution with {self.model_name}...", end=" ", flush=True)
            
            # Make request
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=120  # 2 minutes timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '')
                print("✓")
                
                # Extract code from response
                code = self.extract_code(generated_text)
                return code
            else:
                print(f"✗ (status {response.status_code})")
                return None
                
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def extract_code(self, text: str) -> Optional[str]:
        """Extract Python code from markdown code blocks"""
        # Try to find code in ```python blocks
        pattern = re.compile(config.CODE_BLOCK_PATTERN, re.DOTALL)
        matches = pattern.findall(text)
        
        if matches:
            # Return the first code block found
            return matches[0].strip()
        
        # If no code block found, try to find code between ``` markers
        pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
        matches = pattern.findall(text)
        
        if matches:
            return matches[0].strip()
        
        # If still no code found, return the whole text
        # (model might have returned raw code)
        return text.strip()
    
    def generate_solution_streaming(self, problem_details: dict):
        """Generate solution with streaming (for debugging)"""
        prompt = config.PROBLEM_PROMPT_TEMPLATE.format(**problem_details)
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True
        }
        
        print("Generating solution (streaming)...")
        
        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                stream=True,
                timeout=120
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            text = chunk['response']
                            print(text, end='', flush=True)
                            full_response += text
                    except json.JSONDecodeError:
                        continue
            
            print("\n")
            return self.extract_code(full_response)
            
        except Exception as e:
            print(f"Error during streaming: {e}")
            return None


if __name__ == "__main__":
    # Test the interface
    interface = OllamaInterface()
    
    if interface.check_connection():
        interface.check_model()
        
        # Test with a simple problem
        test_problem = {
            'title': 'A+B Problem',
            'description': 'Calculate the sum of two integers.',
            'input_format': 'Two integers a and b',
            'output_format': 'Single integer - the sum',
            'note': '',
            'examples': 'Input: 1 2\nOutput: 3'
        }
        
        code = interface.generate_solution(test_problem)
        if code:
            print("\nGenerated code:")
            print(code)