# Contributing to AI Studio

Thank you for your interest in contributing to AI Studio! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in AI Studio a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes**:
- Trolling, insulting/derogatory comments, personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Violations of the Code of Conduct may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to: [project maintainers]

---

## How Can I Contribute?

There are many ways to contribute to AI Studio:

### 🐛 Bug Reports
Found a bug? Help us fix it by reporting it.

### 💡 Feature Requests
Have an idea? We'd love to hear it.

### 📝 Documentation
Help improve our docs, guides, or examples.

### 🔧 Code Contributions
Fix bugs, implement features, or improve performance.

### 🎨 Design
Improve UI/UX, create assets, or design new features.

### 🧪 Testing
Write tests, test beta features, or improve test coverage.

### 💬 Community Support
Help answer questions in Discussions or Issues.

### 🌍 Translations
Help translate AI Studio to other languages (future).

---

## Getting Started

### Prerequisites

Before contributing code, ensure you have:

- **Node.js** 18+ and npm 9+
- **Python** 3.11+
- **Git**
- Basic knowledge of React, TypeScript, Python, FastAPI
- Read the [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

### Fork & Clone

1. **Fork the repository** on GitHub
   ```
   Click "Fork" button at https://github.com/zusamstone/congenial-doodle
   ```

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/congenial-doodle.git
   cd congenial-doodle
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/zusamstone/congenial-doodle.git
   ```

4. **Install dependencies**:
   ```bash
   npm run install-all
   ```

5. **Create a branch**:
   ```bash
   git checkout -b feature/my-feature
   # or
   git checkout -b fix/my-bugfix
   ```

You're ready to contribute!

---

## Development Process

### 1. Pick an Issue

Browse [open issues](https://github.com/zusamstone/congenial-doodle/issues) and find something you'd like to work on.

**Good first issues**:
- Look for `good first issue` label
- Usually well-defined and scoped
- Great for new contributors

**Comment on the issue**:
```
"I'd like to work on this. I plan to..."
```

Wait for approval/feedback before starting work.

### 2. Sync with Upstream

Before starting, sync with latest changes:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### 3. Create Feature Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/issue-123
```

**Branch naming**:
- `feature/feature-name` - New features
- `fix/issue-123` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/cleanup-api` - Refactoring
- `test/add-tests` - Tests

### 4. Make Changes

**Development workflow**:

1. **Write code** following [Coding Standards](#coding-standards)

2. **Test locally**:
   ```bash
   # Backend
   cd backend
   pytest
   
   # Frontend
   cd frontend
   npm run test
   npm run build  # Ensure builds
   ```

3. **Run the app**:
   ```bash
   npm run dev
   ```

4. **Verify your changes work**

### 5. Commit Changes

Follow [Commit Message Conventions](#commit-message-conventions):

```bash
git add .
git commit -m "feat: Add dark mode toggle"
```

### 6. Push to Your Fork

```bash
git push origin feature/my-feature
```

### 7. Create Pull Request

See [Pull Request Process](#pull-request-process)

---

## Coding Standards

### Python (Backend)

**Style Guide**: PEP 8

**Formatter**: Black
```bash
cd backend
black .
```

**Linter**: Ruff
```bash
ruff check .
ruff check --fix .  # Auto-fix
```

**Type Hints**: Required for new code
```python
def process_message(message: str, max_length: int = 100) -> dict:
    """Process a message and return result."""
    return {"processed": message[:max_length]}
```

**Docstrings**: Google style
```python
def complex_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining behavior,
    edge cases, etc.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param2 is negative
    
    Example:
        >>> complex_function("test", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return len(param1) > param2
```

**Testing**: pytest
```python
# test_my_module.py
import pytest
from my_module import my_function

def test_my_function_success():
    """Test my_function with valid input"""
    result = my_function("input")
    assert result == "expected"

def test_my_function_error():
    """Test my_function raises error on invalid input"""
    with pytest.raises(ValueError):
        my_function(None)
```

### TypeScript/React (Frontend)

**Style Guide**: Airbnb JavaScript/React

**Formatter**: Prettier
```bash
cd frontend
npm run format
```

**Linter**: ESLint
```bash
npm run lint
npm run lint:fix  # Auto-fix
```

**Type Safety**: Strict TypeScript
```typescript
// Use interfaces for objects
interface User {
  id: number;
  name: string;
  email?: string;  // Optional
}

// Use type for unions/aliases
type Status = 'idle' | 'loading' | 'success' | 'error';

// Avoid 'any' - use 'unknown' if truly unknown
const data: unknown = fetchData();
if (isValidData(data)) {
  // Now TypeScript knows the type
  console.log(data.field);
}
```

**Components**: Functional components with hooks
```typescript
import React, { useState } from 'react';

interface MyComponentProps {
  title: string;
  onAction: (id: number) => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ title, onAction }) => {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(count + 1);
    onAction(count);
  };
  
  return (
    <div>
      <h2>{title}</h2>
      <button onClick={handleClick}>Count: {count}</button>
    </div>
  );
};
```

**Testing**: Jest + React Testing Library
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './MyComponent';

describe('MyComponent', () => {
  it('renders with title', () => {
    render(<MyComponent title="Test" onAction={() => {}} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
  
  it('calls onAction when clicked', () => {
    const onAction = jest.fn();
    render(<MyComponent title="Test" onAction={onAction} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalledWith(0);
  });
});
```

### General Principles

**DRY (Don't Repeat Yourself)**:
```python
# ❌ Bad
def process_user(user):
    if user['age'] >= 18:
        return True
    return False

def validate_user(user):
    if user['age'] >= 18:
        return True
    return False

# ✅ Good
def is_adult(user):
    return user['age'] >= 18

def process_user(user):
    return is_adult(user)
```

**KISS (Keep It Simple, Stupid)**:
```python
# ❌ Bad (over-engineered)
class DataProcessor:
    def __init__(self):
        self.strategies = []
    
    def register_strategy(self, strategy):
        self.strategies.append(strategy)
    
    # ... complex abstraction for simple task

# ✅ Good
def process_data(data):
    return [item.upper() for item in data]
```

**SOLID Principles** (especially Single Responsibility):
```python
# ❌ Bad (does too much)
class UserManager:
    def create_user(self, data): ...
    def send_email(self, user): ...
    def generate_pdf(self, user): ...
    def update_database(self, user): ...

# ✅ Good (single responsibility)
class UserService:
    def create_user(self, data): ...
    def update_user(self, user): ...

class EmailService:
    def send_email(self, user): ...

class PDFGenerator:
    def generate_pdf(self, user): ...
```

---

## Commit Message Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

**Required**. One of:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no code change)
- `refactor`: Code change that neither fixes bug nor adds feature
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance (deps, build, etc.)
- `ci`: CI/CD changes

### Scope

**Optional**. Component affected:

- `api`: Backend API
- `ui`: Frontend UI
- `db`: Database
- `rag`: RAG/embeddings
- `models`: Model management
- `chat`: Chat functionality
- `docs`: Documentation

### Subject

**Required**. Brief description:

- Use imperative mood ("add" not "added")
- No capital first letter
- No period at end
- Max 50 characters

### Body

**Optional**. Detailed explanation:

- Wrap at 72 characters
- Explain **what** and **why**, not **how**
- Can have multiple paragraphs

### Footer

**Optional**. References and breaking changes:

- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: describe change`

### Examples

**Simple feature**:
```
feat(chat): add message pinning functionality
```

**Bug fix with details**:
```
fix(api): resolve context limit calculation error

The token counter was not accounting for system prompt
tokens, causing premature context limit errors.

Fixes #234
```

**Breaking change**:
```
feat(api): change embedding API response format

Return embeddings as separate object instead of inline.
This improves API consistency and reduces response size.

BREAKING CHANGE: Embedding responses now use {embedding: [...]}
instead of direct array. Update clients accordingly.

Closes #456
```

**Documentation**:
```
docs: update RAG setup guide with new chunking options
```

**Refactoring**:
```
refactor(db): simplify query builder logic

Extract common query patterns into helper functions.
No functional changes.
```

---

## Pull Request Process

### Before Submitting

**Checklist**:
- [ ] Code follows style guidelines (linted and formatted)
- [ ] Tests pass (`pytest` and `npm run test`)
- [ ] New tests added for new features
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow conventions
- [ ] Branch is up-to-date with main
- [ ] No merge conflicts

**Run checks**:
```bash
# Backend
cd backend
black .
ruff check .
pytest

# Frontend
cd frontend
npm run lint:fix
npm run test
npm run build
```

### Creating the PR

1. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```

2. **Go to GitHub** and click "Compare & pull request"

3. **Fill in the template**:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #123
Relates to #456

## How Has This Been Tested?
Describe the tests you ran and how to reproduce.

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged
```

4. **Submit PR**

### Review Process

**What happens next**:

1. **Automated checks** run (linting, tests, build)
2. **Maintainer review** (usually within 3-5 days)
3. **Feedback** may be provided
4. **Revisions** requested if needed
5. **Approval** once ready
6. **Merge** by maintainer

**Addressing feedback**:

```bash
# Make requested changes
git add .
git commit -m "fix: address review feedback"
git push origin feature/my-feature
# PR automatically updates
```

**If main updated during review**:

```bash
git checkout main
git pull upstream main
git checkout feature/my-feature
git merge main
# Resolve conflicts if any
git push origin feature/my-feature
```

### After Merge

**Clean up**:
```bash
git checkout main
git pull upstream main
git branch -d feature/my-feature  # Delete local branch
git push origin --delete feature/my-feature  # Delete remote branch
```

**Celebrate! 🎉** Your contribution is now part of AI Studio!

---

## Issue Reporting

### Before Reporting

**Search first**:
- Check [existing issues](https://github.com/zusamstone/congenial-doodle/issues)
- Your issue may already be reported or fixed

**Gather information**:
- OS and version (Windows 11, macOS 14, Ubuntu 22.04, etc.)
- AI Studio version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/logs if applicable

### Bug Report Template

```markdown
**Describe the bug**
Clear and concise description.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 11]
 - AI Studio Version: [e.g. 0.1.0]
 - Python Version: [e.g. 3.11.5]
 - Node Version: [e.g. 18.16.0]

**Logs**
Paste relevant logs from `data/logs/ai_studio.log`

**Additional context**
Any other relevant information.
```

### Issue Labels

Issues are tagged with labels:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `wontfix`: This will not be worked on
- `duplicate`: This issue already exists
- `invalid`: This doesn't seem right

---

## Feature Requests

### Before Requesting

**Check first**:
- Search [existing issues](https://github.com/zusamstone/congenial-doodle/issues)
- Check [ROADMAP.md](../ROADMAP.md) for planned features

**Consider**:
- Does it fit AI Studio's goals?
- Would others benefit from this?
- Are there alternative approaches?

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem. Ex. I'm frustrated when [...]

**Describe the solution you'd like**
Clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Use Cases**
Describe how you (and others) would use this feature.

**Additional context**
Any other context, mockups, examples, etc.

**Would you be willing to implement this?**
Yes/No/Maybe with help
```

### Feature Discussion

- Feature requests are discussed in the issue
- Maintainers may ask questions
- Community can provide feedback
- Decision made on inclusion
- If approved, added to ROADMAP.md

---

## Documentation

### Types of Documentation

**Code Documentation**:
- Inline comments for complex logic
- Docstrings for functions/classes
- Type hints

**User Documentation**:
- User guides (USER_GUIDE.md)
- Tutorials
- FAQs
- Troubleshooting

**Developer Documentation**:
- API docs (API.md)
- Developer guide (DEVELOPER_GUIDE.md)
- Architecture docs (ARCHITECTURE.md)

**Project Documentation**:
- README.md
- CONTRIBUTING.md (this file)
- ROADMAP.md
- CHANGELOG.md

### Documentation Standards

**Markdown**:
- Use ATX-style headers (`# Header`)
- Code blocks with language: ` ```python `
- Relative links for internal docs
- Tables for structured data

**Screenshots**:
- PNG format
- Annotate important areas
- Keep file size reasonable (< 500KB)
- Store in `docs/images/`

**Examples**:
- Include runnable examples
- Show both code and output
- Cover common use cases
- Note prerequisites

### Contributing to Docs

**Small fixes**:
- Fix typos, broken links, etc.
- Can PR directly

**Major changes**:
- Open issue first to discuss
- Ensure consistency with existing docs
- Update multiple docs if needed

---

## Community

### Communication Channels

**GitHub Issues**:
- Bug reports
- Feature requests
- Technical discussions

**GitHub Discussions**:
- General questions
- Ideas and brainstorming
- Show and tell

**Pull Requests**:
- Code review discussions
- Implementation feedback

### Getting Help

**For users**:
- Check [USER_GUIDE.md](USER_GUIDE.md)
- Search existing issues
- Ask in Discussions

**For developers**:
- Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- Review [ARCHITECTURE.md](../ARCHITECTURE.md)
- Ask in Discussions or relevant issue

### Recognition

**Contributors**:
- Listed in Contributors section (GitHub auto-generates)
- Mentioned in CHANGELOG.md for significant contributions
- Acknowledgment in release notes

**Types of contributions recognized**:
- Code
- Documentation
- Bug reports
- Feature ideas
- Community support
- Testing

---

## Additional Resources

- [Developer Guide](DEVELOPER_GUIDE.md) - Technical development guide
- [User Guide](USER_GUIDE.md) - End-user documentation
- [API Reference](API.md) - Backend API documentation
- [Architecture](../ARCHITECTURE.md) - System architecture
- [Roadmap](../ROADMAP.md) - Future plans

---

## License

By contributing to AI Studio, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AI Studio! Every contribution, no matter how small, is valued and appreciated. Together, we're building the best local-first AI chat application! 🚀**
