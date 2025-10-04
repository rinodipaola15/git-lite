# Step 5: Branch & Checkout

## Objective
Implement simplified branch management:
- Create new branches (`git branch <name>`).
- Switch between branches (`git checkout <name>`).
- Each branch maintains its own latest commit reference.
- Update HEAD to point to the active branch.

## Key concepts
- **Branch file**: `.mygit/refs/<branch>` stores the latest commit for that branch.
- **HEAD**: points to the current branch reference, not directly to a commit.
- **Checkout**: changes the active branch by updating HEAD.
- **Parent commit**: branches start from the current commit of the active branch.

> Example usage

```python
# Create a new branch 'dev' from current commit
branch("dev")

# Switch to the 'dev' branch
checkout("dev")

# Check current HEAD
with open(".mygit/HEAD", "r") as f:
    print(f"Current HEAD: {f.read().strip()}")
```

## Notes
- Creating a branch copies the latest commit of the current branch into the new branch.
- Checkout only updates HEAD; in this simplified GitLite, it does not modify the working directory.
- Only basic branching is supported; merging and conflict resolution are not implemented yet.