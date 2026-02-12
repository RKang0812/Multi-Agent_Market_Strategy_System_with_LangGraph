"""
Helper utility functions
"""

from typing import Dict, Any
import json


def format_json_output(data: Any, indent: int = 2) -> str:
    """
    Format data as pretty JSON
    
    Args:
        data: Data to format
        indent: Indentation spaces
        
    Returns:
        Formatted JSON string
    """
    if hasattr(data, 'dict'):
        # Pydantic model
        data = data.dict()
    return json.dumps(data, indent=indent, ensure_ascii=False)


def safe_get(dictionary: Dict, *keys, default=None) -> Any:
    """
    Safely get nested dictionary value
    
    Args:
        dictionary: Dictionary to access
        *keys: Nested keys
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, default)
        else:
            return default
    return result


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_input(company_domain: str, industry: str, project_description: str) -> tuple[bool, str]:
    """
    Validate user input
    
    Args:
        company_domain: Company domain
        industry: Industry
        project_description: Project description
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not company_domain or not company_domain.strip():
        return False, "Company domain is required"
    
    if not industry or not industry.strip():
        return False, "Industry is required"
    
    if not project_description or not project_description.strip():
        return False, "Project description is required"
    
    if len(project_description) < 50:
        return False, "Project description should be at least 50 characters"
    
    return True, ""
