# Updating from Upstream

To get the latest improvements from the {{ cookiecutter.project_name }} template:

```bash
git fetch upstream
git merge upstream/main --allow-unrelated-histories
```

This will merge in:
- New domains added to community-domains/
- Bug fixes to install.py
- Framework improvements
- Documentation updates

## What's Safe to Customize

Your customizations in these areas are preserved during updates:
- `domains/` - Your selected and custom domains
- `projects/` - Your project-specific conventions
- `staging/` - Your captured learnings
- `global.md` - Your universal rules

## Handling Conflicts

If you've modified files that are also updated upstream:
1. Git will mark conflicts in the files
2. Review and resolve conflicts manually
3. Keep your customizations where appropriate
4. Test that everything still works

## After Updating

1. Re-run the installer to see new domains:
   ```bash
   ./install.py
   ```

2. Check the README for any new features or changes

3. Test your setup to ensure everything works correctly

## Version Compatibility

This project uses semantic versioning. Updates should be backwards compatible within major versions.
