# Step 6: Status

## Objective
Implement a simplified version of `git status` for GitLite:
- Shows files that are **staged** (added to the index for the next commit).
- Shows files that are **modified** (changed in the working directory but not staged).
- Helps the user understand the current state of the repository before committing.

## Key concepts
- **Index / Staging Area**: stores file hashes of files staged for commit.
- **Staged files**: files added to the index and ready to be committed.
- **Modified files**: files that have been changed in the working directory but are not staged.
- **Working Directory**: the files currently on disk in the project folder.

> Example usage

```python
# After adding files with add()
status()
```

- Output will list staged and modified files.
- If no files are staged, "No files staged." is shown.
- If no files are modified, the modified section may be empty.

## Notes
- The function handles cases where the index file is missing or empty.
- Status helps to prevent committing unintended changes.
- Staged files correspond to blobs stored in .mygit/objects.