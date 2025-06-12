# Example: Migrating from Team Wiki/Google Docs

This example shows how to migrate conventions from unstructured team documentation to the cookiecutter-ai-conventions format.

## Original Team Wiki Content

```
ACME Corp Development Standards
Last Updated: 2024-01-15

1. Python Development
   - Use Python 3.11+
   - Follow PEP 8 with 100 char line limit
   - Use type hints for all functions
   - Docstrings required for public functions
   - Use Black for formatting
   - Use Ruff for linting

2. Database Guidelines
   - All tables must have created_at and updated_at
   - Use UUIDs for primary keys
   - Name foreign keys as {table}_{column}_fkey
   - Migrations must be reversible
   - No direct SQL in application code

3. API Standards
   - All APIs must be versioned (/api/v1/)
   - Use camelCase for JSON fields
   - Include request ID in headers
   - Rate limit all public endpoints
   - Return 429 for rate limit exceeded

4. Security Requirements
   - No secrets in code
   - Use environment variables
   - Rotate API keys quarterly
   - Log security events
   - OWASP Top 10 compliance

5. Code Review Process
   - At least 2 approvals required
   - Must pass all CI checks
   - Security review for auth changes
   - Performance review for DB changes
```

## Migrated Structure

### 1. global.md
```markdown
# ACME Corp Global Standards

## Development Philosophy
- Prioritize code security and maintainability
- Follow established style guides for each language
- Maintain backward compatibility
- Document all architectural decisions

## Security First
- No secrets in code - use environment variables
- Follow OWASP Top 10 guidelines
- Log all security-relevant events
- Rotate credentials quarterly

## Code Review Requirements
- Minimum 2 approvals for all PRs
- All CI checks must pass
- Security review required for authentication changes
- Performance review required for database changes
```

### 2. domains/python/core.md
```markdown
# Python Development Standards

## When This Applies
- Working with .py files
- Creating Python modules or packages
- Keywords: Python, function, class, import

## Conventions

### Language Requirements
- Use Python 3.11 or higher
- Include type hints for all function signatures
- Write docstrings for all public functions and classes

### Code Style
- Follow PEP 8 with 100 character line limit
- Use Black for automatic formatting
- Use Ruff for linting
- Configure both in pyproject.toml

### Function Design
```python
def calculate_total(
    items: list[OrderItem],
    discount: Decimal = Decimal("0")
) -> Decimal:
    """Calculate order total with optional discount.
    
    Args:
        items: List of order items
        discount: Discount percentage (0-100)
        
    Returns:
        Total amount after discount
    """
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * (1 - discount / 100)
```

### Import Organization
- Standard library imports first
- Third-party imports second  
- Local application imports last
- Alphabetical order within groups
```

### 3. domains/database/core.md
```markdown
# Database Development

## When This Applies
- Creating or modifying database schemas
- Writing migrations
- Keywords: table, migration, SQL, database, query

## Conventions

### Table Design
- All tables must include:
  - `id` (UUID primary key)
  - `created_at` (timestamp with timezone)
  - `updated_at` (timestamp with timezone)

### Naming Conventions
- Table names: plural, snake_case (e.g., `user_accounts`)
- Column names: snake_case
- Foreign keys: `{table}_{column}_fkey`
- Indexes: `idx_{table}_{columns}`

### Migration Requirements
- All migrations must be reversible
- Test rollback before deploying
- Include clear up and down methods
- Name format: `YYYYMMDD_HHMMSS_description.py`

### Query Patterns
- No direct SQL in application code
- Use ORM or query builder
- Parameterize all queries
- Add query comments for complex operations

Example migration:
```python
def upgrade():
    op.create_table(
        'user_accounts',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_user_accounts_email', 'user_accounts', ['email'])

def downgrade():
    op.drop_index('idx_user_accounts_email')
    op.drop_table('user_accounts')
```
```

### 4. domains/api/core.md
```markdown
# API Development Standards

## When This Applies
- Creating REST API endpoints
- Modifying API responses
- Keywords: API, endpoint, REST, HTTP, route

## Conventions

### API Structure
- Version all APIs: `/api/v1/resource`
- Use RESTful resource naming
- Support standard HTTP methods
- Include API version in headers

### Response Format
- Use camelCase for all JSON fields
- Include request ID in response headers
- Consistent error response structure:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "field": "email",
      "reason": "Invalid format"
    }
  },
  "requestId": "req_123abc"
}
```

### Rate Limiting
- Implement rate limiting on all public endpoints
- Return 429 status for exceeded limits
- Include rate limit headers:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

### API Documentation
- Document with OpenAPI 3.0
- Include examples for all endpoints
- Specify authentication requirements
- List all possible error codes
```

### 5. domains/security/core.md
```markdown
# Security Standards

## When This Applies
- Handling sensitive data
- Authentication/authorization code
- Keywords: password, token, auth, secure, encrypt

## Conventions

### Credential Management
- Never commit secrets to version control
- Use environment variables for all credentials
- Rotate API keys quarterly
- Use key management service in production

### Authentication
- Use bcrypt for password hashing
- Implement proper session management
- Enable MFA for privileged accounts
- Log all authentication events

### Data Protection
- Encrypt sensitive data at rest
- Use TLS for all communications
- Implement input validation
- Sanitize all user inputs

### Security Logging
- Log all security events:
  - Failed login attempts
  - Permission changes
  - Data access to sensitive resources
- Include timestamp, user, IP, and action
- Forward logs to SIEM system
```

## Migration Steps

1. **Analyze** your existing documentation to identify distinct domains
2. **Group** related conventions together
3. **Convert** passive descriptions to active voice commands
4. **Add** triggering contexts for each domain
5. **Test** with your team to ensure nothing was missed

## Benefits After Migration

- ✅ AI assistants understand context better
- ✅ Conventions are easier to update and maintain
- ✅ New team members onboard faster
- ✅ Consistent format across all tools
- ✅ Version controlled with change history