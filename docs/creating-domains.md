# Creating Your Own Convention Domain

So you've been using the community domains, but now you want to create conventions specific to your team's needs. Let's build one together.

## What We're Building

We'll create a React conventions domain that enforces your team's component patterns.

## Step 1: Understand the Anatomy

Every domain has:
```
domains/react/
├── core.md          # Essential patterns (always loaded)
├── components.md    # Component patterns
├── testing.md       # Testing conventions
└── hooks.md         # Custom hooks patterns
```

## Step 2: Start with Core Patterns

Create `domains/react/core.md`:

```markdown
# React Core Conventions

## Component Structure

Components follow this pattern:

\```typescript
// UserProfile.tsx
import { FC, useState, useEffect } from 'react';
import { useUser } from '@/hooks/useUser';
import { Card } from '@/components/ui/Card';
import type { User } from '@/types';

interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

export const UserProfile: FC<UserProfileProps> = ({ userId, onUpdate }) => {
  const { user, loading, error } = useUser(userId);
  
  if (loading) return <Card.Skeleton />;
  if (error) return <Card.Error message={error.message} />;
  
  return (
    <Card>
      <Card.Header>{user.name}</Card.Header>
      <Card.Body>{/* content */}</Card.Body>
    </Card>
  );
};
\```

Key patterns:
1. Named exports (not default)
2. Props interface defined above component
3. Hooks at the top
4. Early returns for states
5. Descriptive variable names
```

## Step 3: Add Specific Patterns

Create `domains/react/hooks.md`:

```markdown
# Custom React Hooks

## Naming Convention

All hooks start with `use` and return an object (not array):

\```typescript
// ✅ GOOD
export const useUser = (userId: string) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  // ... logic ...
  
  return { user, loading, error, refetch };
};

// ❌ BAD
export const useUser = (userId: string) => {
  // Don't return arrays
  return [user, loading, error];
};
\```

## Data Fetching Hooks

Always include loading, error, and refetch:

\```typescript
interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export const useApi = <T>(url: string): UseApiResult<T> => {
  // Implementation
};
\```
```

## Step 4: Real-World Example

Let's say your team discovered a pattern during code review. Capture it!

Your colleague wrote:
```typescript
// They wrote this
const [name, setName] = useState('');
const [email, setEmail] = useState('');
const [phone, setPhone] = useState('');
```

You know this should be:
```typescript
// Should be this
const [formData, setFormData] = useState({
  name: '',
  email: '',
  phone: ''
});
```

Add to `domains/react/components.md`:
```markdown
## Form State Management

Group related form fields into a single state object:

\```typescript
// ✅ GOOD - Grouped state
const [formData, setFormData] = useState({
  name: '',
  email: '',
  phone: ''
});

const handleChange = (field: keyof typeof formData) => (
  e: React.ChangeEvent<HTMLInputElement>
) => {
  setFormData(prev => ({ ...prev, [field]: e.target.value }));
};

// ❌ BAD - Separate states
const [name, setName] = useState('');
const [email, setEmail] = useState('');
const [phone, setPhone] = useState('');
\```
```

## Step 5: Test Your Domain

1. Install your domain:
   ```bash
   ./install.py
   # Select 'react'
   ```

2. Ask your AI to create a React component:
   > "Create a UserList component that fetches and displays users"

3. It should follow your patterns:
   - Named export
   - Proper TypeScript interfaces
   - Your hook conventions
   - Your state management patterns

## Step 6: Share with Community

If your domain could help others:

1. Fork the repository
2. Add your domain to `community-domains/`
3. Update `registry.yaml`:
   ```yaml
   domains:
     - name: react
       description: "React component patterns with TypeScript"
       files:
         - core.md
         - components.md
         - hooks.md
         - testing.md
       maintainer: "@yourgithub"
   ```
4. Submit a pull request!

## Best Practices

### DO:
- ✅ Use real code examples from your codebase
- ✅ Show both good and bad patterns
- ✅ Explain WHY a pattern exists
- ✅ Keep examples focused and clear
- ✅ Update based on team feedback

### DON'T:
- ❌ Create theoretical patterns you don't use
- ❌ Copy-paste from style guides without adapting
- ❌ Make it too prescriptive - leave room for context
- ❌ Forget to test with actual AI prompts

## Evolution Process

Your domain will evolve:

1. **Week 1-2**: Capture obvious patterns
2. **Week 3-4**: Notice edge cases, refine
3. **Month 2**: Patterns stabilize
4. **Ongoing**: Capture new patterns as they emerge

Use the learning capture system:
```bash
./commands/capture-learning.py
# Capture patterns as you discover them
# Review weekly and promote stable ones
```

## Examples of Great Domains

### `python` Domain
- Clear import conventions
- Error handling patterns
- Type hint guidelines
- Testing structure

### `git` Domain  
- Commit message formats
- Branch naming
- PR templates
- Merge strategies

### `writing` Domain
- Documentation style
- API doc format
- Comment conventions
- README structure

Study these for inspiration!

---

Ready to create your domain? Start with one core pattern and build from there. Your AI assistant will thank you!