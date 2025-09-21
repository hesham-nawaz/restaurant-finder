"""
Gemini API client for AI-powered restaurant recommendations.
"""

import yaml
import os
from typing import Dict, Any, Optional


class GeminiClient:
    """Client for interacting with Google's Gemini AI API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompts from YAML configuration file."""
        config_path = "configs/prompts.yaml"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Prompt config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_prompt(self, prompt_name: str, include_examples: bool = True) -> str:
        """Get a specific prompt by name."""
        if prompt_name not in self.prompts['prompts']:
            raise KeyError(f"Prompt '{prompt_name}' not found")
        
        prompt_config = self.prompts['prompts'][prompt_name]
        system_prompt = prompt_config['system']
        
        if include_examples and 'examples' in prompt_config:
            examples_text = "\n\nExamples:\n"
            for example in prompt_config['examples']:
                examples_text += f"Input: {example['input']}\n"
                examples_text += f"Output: {example['output']}\n\n"
            system_prompt += examples_text
        
        return system_prompt
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text response
        """
        # TODO: Implement actual Gemini API call
        # For now, return a placeholder response
        return f"Gemini response to: {prompt[:50]}..."
    
    def request_reformatter(self, user_request: str) -> Dict[str, Any]:
        """
        Reformats a plaintext user request into a structured dictionary.
        
        Args:
            user_request: User's natural language request
            
        Returns:
            Structured dictionary with parsed request parameters
        """
        prompt = self.get_prompt('request_reformatter')
        full_prompt = f"{prompt}\n\nUser request: {user_request}"
        
        response = self.generate_text(full_prompt)
        
        # TODO: Parse the response into a proper dictionary
        # For now, return a placeholder structure
        return {
            "location": "Los Angeles, CA",
            "geographic_distance": None,
            "time_distance": "20 minutes",
            "cuisine": "Chinese",
            "price": "cheap",
            "rating": None,
            "reviews": None,
            "hours": None
        }
