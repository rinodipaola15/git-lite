# Step 3: Commit

## Objective
Implement a simplified version of `git commit`:
- Collects added file hashes (blobs).
- Creates a commit object storing:
  - tree (file hashes)
  - parent commit (if any)
  - timestamp
  - commit message
- Updates the current branch reference (refs/master).

## Key concepts
- **Commit object**: snapshot of the repository at a given point in time.
- **Tree**: a simple list of file hashes for this commit.
- **Parent**: points to the previous commit, building history.
- **Branch update**: HEAD points to the branch, branch file updated with latest commit hash.

> Example usage

```python
# Suppose you have added two files already
files_hashes = [hash_object("file1.txt"), hash_object("file2.txt")]
commit_hash = commit(files_hashes, "Initial commit")
```

## Notes
- The first commit will create the master branch automatically.
- Subsequent commits will update refs/master and chain with parent commits.