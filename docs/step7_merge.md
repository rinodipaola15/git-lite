# Step 7: Merge

## Objective
Implement a simplified version of `git merge`:
- Combines changes from a source branch into the current branch.
- Updates the current branch reference if the merge is a fast-forward.

## Key concepts
- **Current branch**: branch pointed by HEAD where changes will be applied.
- **Source branch**: branch whose commits we want to merge.
- **Fast-forward merge**: if the current branch has no new commits, its pointer can simply be moved to the latest commit of the source branch.
- **Commit history**: after a fast-forward merge, the current branch contains all commits from the source branch.

> Example usage

```python
# Suppose we are on 'master' and want to merge 'dev' into it
checkout("master")   # switch to master
merge("dev")         # merge dev into master
log()                # view updated commit history
```

## Notes
- Only fast-forward merges are supported in GitLite at this stage.
- If the current branch already has commits diverging from the source branch, a manual merge is not implemented yet.
- The merge updates the HEAD branch reference to the latest commit of the source branch.