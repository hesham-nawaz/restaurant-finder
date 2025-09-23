"""
Gemini API client for AI-powered restaurant recommendations.
"""

import yaml
import os
import json
from google import genai
from typing import Dict, Any, Optional
from ..models.restaurant_query import SimpleRestaurantQuery



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
        
        # Initialize the new Google Gen AI client
        self.client = genai.Client(api_key=self.api_key)
    
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
    
    def generate_text(self, prompt: str, temperature: float = 0) -> str:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            temperature: Controls randomness (0.0 to 1.0)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        
        try:
            # Use the new SDK with simplified Pydantic model for API compatibility
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": SimpleRestaurantQuery,
                    "temperature": temperature
                }
            )
            
            # Return the generated text
            return response.text
            
        except Exception as e:
            raise Exception(f"Failed to generate text with Gemini API: {str(e)}")