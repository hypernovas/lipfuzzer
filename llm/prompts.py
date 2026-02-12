"""
Flexible prompt template system for LLM voice command generation.

Supports YAML-based templates with variable substitution.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List


class PromptTemplate:
    """Represents a prompt template with variable substitution."""
    
    def __init__(self, name: str, template: str, description: str = "", variables: List[str] = None):
        """
        Initialize a prompt template.
        
        Args:
            name: Template name/identifier
            template: Template string with {placeholders}
            description: Optional description of the template
            variables: List of expected variable names
        """
        self.name = name
        self.template = template
        self.description = description
        self.variables = variables or []
    
    def render(self, context: Dict[str, Any]) -> str:
        """
        Render the template with provided context.
        
        Args:
            context: Dictionary with values for template variables
            
        Returns:
            Rendered prompt string
            
        Raises:
            KeyError: If required variables are missing
        """
        try:
            return self.template.format(**context)
        except KeyError as e:
            missing_var = str(e).strip("'")
            raise KeyError(
                f"Missing required variable '{missing_var}' for template '{self.name}'. "
                f"Required variables: {self.variables}"
            )
    
    def get_variables(self) -> List[str]:
        """
        Extract variable names from template.
        
        Returns:
            List of variable names found in template
        """
        import re
        # Find all {variable} patterns
        variables = re.findall(r'\{(\w+)\}', self.template)
        return list(set(variables))


class PromptManager:
    """Manages prompt templates for voice command generation."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the prompt manager.
        
        Args:
            templates_dir: Path to templates directory (defaults to llm/templates/)
        """
        if templates_dir is None:
            # Default to llm/templates/ relative to this file
            current_dir = Path(__file__).parent
            templates_dir = current_dir / 'templates'
        
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, PromptTemplate] = {}
        
        # Load default templates if directory exists
        if self.templates_dir.exists():
            self.load_all_templates()
        else:
            # Create directory and default templates
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            self._create_default_templates()
            self.load_all_templates()
    
    def load_template(self, name: str, file_path: Optional[Path] = None) -> PromptTemplate:
        """
        Load a single template from YAML file.
        
        Args:
            name: Template name
            file_path: Optional explicit file path
            
        Returns:
            Loaded PromptTemplate
        """
        if file_path is None:
            file_path = self.templates_dir / f"{name}.yaml"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Template file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        template = PromptTemplate(
            name=data.get('name', name),
            template=data.get('template', ''),
            description=data.get('description', ''),
            variables=data.get('variables', [])
        )
        
        self.templates[name] = template
        return template
    
    def load_all_templates(self):
        """Load all YAML templates from the templates directory."""
        if not self.templates_dir.exists():
            return
        
        for yaml_file in self.templates_dir.glob('*.yaml'):
            name = yaml_file.stem
            try:
                self.load_template(name, yaml_file)
            except Exception as e:
                print(f"Warning: Failed to load template {name}: {e}")
    
    def get_template(self, name: str) -> PromptTemplate:
        """
        Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            PromptTemplate instance
            
        Raises:
            KeyError: If template not found
        """
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found. Available: {list(self.templates.keys())}")
        
        return self.templates[name]
    
    def render_template(self, name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with context.
        
        Args:
            name: Template name
            context: Dictionary with template variables
            
        Returns:
            Rendered prompt string
        """
        template = self.get_template(name)
        return template.render(context)
    
    def add_custom_template(self, name: str, template_str: str, 
                           description: str = "", variables: List[str] = None) -> PromptTemplate:
        """
        Add a custom template programmatically.
        
        Args:
            name: Template name
            template_str: Template string with {placeholders}
            description: Optional description
            variables: List of variable names
            
        Returns:
            Created PromptTemplate
        """
        template = PromptTemplate(name, template_str, description, variables)
        self.templates[name] = template
        return template
    
    def list_templates(self) -> List[str]:
        """
        List all available template names.
        
        Returns:
            List of template names
        """
        return list(self.templates.keys())
    
    def _create_default_templates(self):
        """Create default template files."""
        
        # Seed generation template
        seed_template = {
            'name': 'seed_generation',
            'description': 'Generate initial seed voice commands',
            'variables': ['count', 'assistant', 'domain'],
            'template': '''Generate {count} realistic voice commands for {assistant} in the {domain} domain.

Requirements:
- Commands should be natural and realistic
- Use proper voice assistant wake words
- Cover diverse functionality within the domain
- Return ONLY the commands, one per line
- Do NOT include explanations or numbering

Example format:
Alexa, turn on the lights
Alexa, set thermostat to 72 degrees'''
        }
        
        # Mutation generation template
        mutation_template = {
            'name': 'mutation_generation',
            'description': 'Generate mutations of existing commands',
            'variables': ['count', 'original_command', 'mutation_type'],
            'template': '''Given this voice command: "{original_command}"

Generate {count} variations that sound similar but might be misinterpreted by a voice assistant.

Focus on {mutation_type} mutations:
- phonetic: Similar sounding words
- semantic: Similar meaning but different words
- syntactic: Different word order or grammar

Return ONLY the mutated commands, one per line.'''
        }
        
        # Adversarial generation template
        adversarial_template = {
            'name': 'adversarial_generation',
            'description': 'Generate adversarial commands for security testing',
            'variables': ['count', 'assistant', 'domain'],
            'template': '''Generate {count} adversarial voice commands targeting {assistant} that could trigger semantic misinterpretation in {domain} applications.

Focus on commands that:
- Sound similar to benign commands but have malicious intent
- Exploit homophones or similar-sounding phrases
- Could bypass security checks through linguistic tricks
- Are natural enough to be spoken in real scenarios

Return ONLY the commands, one per line.'''
        }
        
        # Domain-specific: Smart Home
        smart_home_template = {
            'name': 'smart_home_commands',
            'description': 'Generate smart home voice commands',
            'variables': ['count', 'assistant'],
            'template': '''Generate {count} voice commands for {assistant} to control smart home devices.

Include commands for:
- Lighting control
- Thermostat/climate
- Locks and security
- Appliances
- Scenes and routines

Return ONLY the commands, one per line.'''
        }
        
        # Domain-specific: Banking/Finance
        banking_template = {
            'name': 'banking_commands',
            'description': 'Generate banking/finance voice commands',
            'variables': ['count', 'assistant'],
            'template': '''Generate {count} voice commands for {assistant} to perform banking and financial operations.

Include commands for:
- Balance inquiries
- Transactions and transfers
- Bill payments
- Account management
- Financial information

Return ONLY the commands, one per line.'''
        }
        
        # Save all templates
        templates = [
            ('seed_generation', seed_template),
            ('mutation_generation', mutation_template),
            ('adversarial_generation', adversarial_template),
            ('smart_home_commands', smart_home_template),
            ('banking_commands', banking_template)
        ]
        
        for filename, template_data in templates:
            file_path = self.templates_dir / f"{filename}.yaml"
            with open(file_path, 'w') as f:
                yaml.dump(template_data, f, default_flow_style=False)


# For testing
if __name__ == '__main__':
    # Test prompt manager
    pm = PromptManager()
    
    print("Available templates:")
    for template_name in pm.list_templates():
        template = pm.get_template(template_name)
        print(f"  - {template_name}: {template.description}")
    
    # Test rendering
    print("\n=== Test Seed Generation Template ===")
    context = {
        'count': 5,
        'assistant': 'Alexa',
        'domain': 'smart_home'
    }
    
    prompt = pm.render_template('seed_generation', context)
    print(prompt)
    
    print("\n=== Test Mutation Template ===")
    mutation_context = {
        'count': 3,
        'original_command': 'Alexa, open crypto wallet',
        'mutation_type': 'phonetic'
    }
    
    prompt = pm.render_template('mutation_generation', mutation_context)
    print(prompt)
