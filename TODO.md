# TODO - Implementation Checklist

## Immediate Tasks

- [ ] Run `convert_yaml.py` to convert YAML files to JSON (requires PyYAML: `pip install pyyaml`)
- [ ] Make bootstrap.sh executable: `chmod +x bootstrap.sh`
- [ ] Update README.md with your GitHub username
- [ ] Initialize git repository

## Core Implementation

- [ ] Implement Textual TUI in `hooks/pre_gen_project.py`
- [ ] Complete `install.py` with domain selection
- [ ] Create CLAUDE.md.j2 template
- [ ] Add conditional directories (commands/, staging/)
- [ ] Implement learning capture commands

## Nice to Have

- [ ] Add tests
- [ ] Create example generated repositories
- [ ] Add GitHub Actions CI/CD
- [ ] Create demo GIF for README

## Commands to Run

```bash
# Install dependencies
pip install pyyaml

# Convert YAML to JSON
python3 convert_yaml.py

# Make scripts executable
chmod +x bootstrap.sh

# Initialize git
git init
git add -A
git commit -m "Initial commit"
```
