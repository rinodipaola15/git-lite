# Step 4: Log

## Objective
Implement a simplified version of `git log`:
- Traverses the commit history of the current branch (master).
- Prints for each commit:
  - Commit hash
  - Commit timestamp
  - Commit message
- Follows the `parent` links to show commits in reverse chronological order.

## Key concepts
- **HEAD**: points to the current branch reference (e.g., `refs/master`).
- **Branch file**: stores the latest commit hash for that branch.
- **Commit object**: contains tree, parent, date, and message.
- **Parent link**: allows traversing the commit history backward.
- **Traversal**: starts from the latest commit and goes back until no parent exists.

> Example usage

```python
# Display the commit history of the current branch
log()
```

## Notes
- The log function prints commits from most recent to oldest.
- Only the current branch (master) is supported in this simplified version.
- Warnings may appear if a commit object is missing or corrupted in .mygit/objects.