"""
Prompt management service.
"""

import yaml
import os
from typing import Dict, Any, List, Optional


class PromptService:
    """Service for managing AI prompts."""
    
    def __init__(self, config_path: str = "configs/prompts.yaml"):
        """
        Initialize the prompt service.
        
        Args:
            config_path: Path to prompts configuration file
        """
        self.config_path = config_path
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompts from YAML configuration file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Prompt config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_prompt(self, prompt_name: str, include_examples: bool = True) -> str:
        """
        Get a specific prompt by name.
        
        Args:
            prompt_name: Name of the prompt
            include_examples: Whether to include examples in the prompt
            
        Returns:
            Formatted prompt string
        """
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
    
    def get_prompt_info(self, prompt_name: str) -> Dict[str, Any]:
        """
        Get metadata about a prompt.
        
        Args:
            prompt_name: Name of the prompt
            
        Returns:
            Prompt metadata dictionary
        """
        if prompt_name not in self.prompts['prompts']:
            raise KeyError(f"Prompt '{prompt_name}' not found")
        
        return self.prompts['prompts'][prompt_name]
    
    def list_prompts(self) -> List[str]:
        """
        List all available prompts.
        
        Returns:
            List of prompt names
        """
        return list(self.prompts['prompts'].keys())
    
    def add_prompt(self, prompt_name: str, prompt_config: Dict[str, Any]) -> None:
        """
        Add a new prompt to the configuration.
        
        Args:
            prompt_name: Name of the new prompt
            prompt_config: Prompt configuration dictionary
        """
        self.prompts['prompts'][prompt_name] = prompt_config
        self._save_prompts()
    
    def update_prompt(self, prompt_name: str, prompt_config: Dict[str, Any]) -> None:
        """
        Update an existing prompt.
        
        Args:
            prompt_name: Name of the prompt to update
            prompt_config: Updated prompt configuration
        """
        if prompt_name not in self.prompts['prompts']:
            raise KeyError(f"Prompt '{prompt_name}' not found")
        
        self.prompts['prompts'][prompt_name].update(prompt_config)
        self._save_prompts()
    
    def delete_prompt(self, prompt_name: str) -> None:
        """
        Delete a prompt from the configuration.
        
        Args:
            prompt_name: Name of the prompt to delete
        """
        if prompt_name not in self.prompts['prompts']:
            raise KeyError(f"Prompt '{prompt_name}' not found")
        
        del self.prompts['prompts'][prompt_name]
        self._save_prompts()
    
    def _save_prompts(self) -> None:
        """Save prompts back to the configuration file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.prompts, f, default_flow_style=False, indent=2)
    
    def reload_prompts(self) -> None:
        """Reload prompts from the configuration file."""
        self.prompts = self._load_prompts()
    
    def validate_prompt(self, prompt_name: str) -> bool:
        """
        Validate that a prompt has all required fields.
        
        Args:
            prompt_name: Name of the prompt to validate
            
        Returns:
            True if valid, False otherwise
        """
        if prompt_name not in self.prompts['prompts']:
            return False
        
        prompt_config = self.prompts['prompts'][prompt_name]
        required_fields = ['system']
        
        return all(field in prompt_config for field in required_fields)
