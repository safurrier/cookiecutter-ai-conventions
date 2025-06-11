{%- if "writing" in cookiecutter.default_domains.split(',') -%}
# Documentation Conventions Prompt

When writing documentation for this project:

## Documentation Principles
1. Start with the problem, not the solution
2. Show examples before explaining theory
3. Use active voice
4. Progressive disclosure - simple first, complex later

## Code Documentation

### Docstrings
```python
def process_data(data: List[Dict], validate: bool = True) -> ProcessedData:
    """Process raw data into structured format.
    
    Takes raw data dictionaries and converts them into ProcessedData
    objects, optionally validating the input.
    
    Args:
        data: List of raw data dictionaries to process
        validate: Whether to validate input data (default: True)
        
    Returns:
        ProcessedData object containing the structured data
        
    Raises:
        ValidationError: If validate=True and data is invalid
        
    Example:
        >>> raw_data = [{"id": 1, "value": "test"}]
        >>> result = process_data(raw_data)
        >>> print(result.count)
        1
    """
```

## README Structure
1. One-line description
2. Problem statement
3. Quick start example
4. Installation
5. Usage examples
6. API reference (if applicable)
7. Contributing guidelines

## Writing Style
- Clear and concise
- Avoid jargon without explanation
- Include code examples
- Link to detailed docs for complex topics
{%- endif -%}