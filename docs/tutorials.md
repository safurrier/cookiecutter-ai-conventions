# Step-by-Step Tutorials

## Your First Convention: Stop Inline Imports

Let's fix the most annoying AI habit - inline imports.

### 1. Generate Your Conventions Repository

```bash
uvx cookiecutter gh:safurrier/cookiecutter-ai-conventions
```

When prompted:
- Project name: `my-conventions` (or your preference)
- Select domains: Choose `python` and `git` to start
- Enable learning capture: `yes` (recommended)

### 2. Add Your First Convention

```bash
cd my-conventions
echo "## Import Style

Always put imports at the top of the file, never inline.
Group imports: standard library, third-party, local.

GOOD:
\`\`\`python
import os
import sys
from typing import Optional

import requests
import pandas as pd

from myapp import utils
\`\`\`

BAD:
\`\`\`python
def process_data():
    import pandas as pd  # Never do this
\`\`\`
" >> domains/python/core.md
```

### 3. Install and Test

```bash
./install.py  # Installs to ~/.claude/CLAUDE.md
```

Now ask Claude to write a function that reads a CSV file. It should automatically put the pandas import at the top!

---

## Team Onboarding: Share Your Conventions

Got a new team member? Get them up to speed in minutes.

### 1. Push Your Conventions to Git

```bash
git init
git add -A
git commit -m "feat: initial team conventions"
git remote add origin https://github.com/yourteam/conventions.git
git push -u origin main
```

### 2. New Team Member Setup

Send them one command:
```bash
# They run:
uvx cookiecutter gh:yourteam/conventions
cd team-conventions
./install.py
```

### 3. They're Ready!

Your new team member's AI now knows:
- Your commit message format
- Your code style preferences
- Your testing patterns
- Your documentation standards

No more onboarding documents that nobody reads!

---

## Evolving Conventions: Capture as You Code

You just discovered a pattern. Don't let it slip away!

### Scenario: Your Team's API Error Format

You're reviewing code and notice the AI suggested a generic error response. Your team has a specific format.

### 1. Capture the Learning

```bash
./commands/capture-learning.py

📚 Capture Development Learnings
================================

Learning title: Use standard API error response format
Context: Code review on user service PR
Problem: AI suggested returning {'error': message} for API errors
Solution: Always use our standard format: {
  'error': {
    'code': 'ERROR_CODE',
    'message': 'Human readable message',
    'details': {} // optional
  }
}
Domain: python
Promote to: api_patterns.md
```

### 2. Review and Promote

After a week, review your learnings:
```bash
./commands/review-learnings.py

📚 Staged Learnings Review
==========================
Total learnings: 3

PYTHON (3 learnings):
  - "Use standard API error response format" ✓ READY
  - "Prefer explicit type hints for function returns" (3 days old)
  - "Use dependency injection for external services" (1 day old)
```

### 3. Promote Stable Patterns

Edit `domains/python/api_patterns.md` and add your learning:
```markdown
## API Error Responses

Always return errors in our standard format:
```python
{
    'error': {
        'code': 'USER_NOT_FOUND',
        'message': 'The requested user does not exist',
        'details': {'user_id': user_id}
    }
}
```
```

Now your entire team's AI assistants know the pattern!

---

## Custom Domain: Create Conventions for Your Stack

Your team uses a specific tech stack. Create a custom domain for it.

### Example: FastAPI Conventions

### 1. Create the Domain Structure

```bash
mkdir -p domains/fastapi
```

### 2. Define Your Patterns

Create `domains/fastapi/core.md`:
```markdown
# FastAPI Conventions

## Dependency Injection

Always use FastAPI's dependency injection for:
- Database sessions
- Authentication
- External services

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User

@router.get("/items")
async def get_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    return db.query(Item).offset(skip).limit(limit).all()
```

## Response Models

Always use Pydantic models for responses:

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == item_id).first()
```
```

### 3. Add to Registry

Edit `domains/registry.md`:
```markdown
## Custom Domains

### fastapi
FastAPI-specific patterns and best practices for building APIs.
```

### 4. Reinstall

```bash
./install.py
# Select your new 'fastapi' domain
```

Your AI now knows FastAPI patterns!

---

## Debugging: When Conventions Aren't Loading

### Check Installation

```bash
# Verify CLAUDE.md exists
cat ~/.claude/CLAUDE.md

# Should show your domains
```

### Test with a Simple Prompt

Ask your AI:
> "What are my coding conventions?"

It should list your installed domains.

### Force Reload

Some AI tools cache contexts. Try:
1. Restart your AI tool
2. Open a new conversation
3. Explicitly mention you want to follow your conventions

### Still Not Working?

Check our [troubleshooting guide](troubleshooting.md) or open an issue.