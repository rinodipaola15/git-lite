# Step 2: Add a file

## Objective
Implement a simplified version of `git add`:

- Reads one or more files from the filesystem.
- Stores each file in `.mygit/objects/` as a compressed blob.
- Generates a SHA-1 hash to uniquely identify the file content.
- Records the file path and hash in the staging area (`.mygit/index`) for the next commit.

---

## Key concepts
- **Blob**: an object that stores the content of a file.  
- **SHA-1 hash**: a unique identifier for the file content.  
- **Objects folder**: stores all blobs and commits (`.mygit/objects/`).  
- **File path**: indicates the location of the file in the project. Needed to reconstruct the project structure during commit.  
- **Staging area (index)**: keeps track of which files are staged for the next commit. Each entry is a combination of `hash` + `file path`.  

---

## How it works
1. `hash_object(file_path)`  
   - Reads the file content, computes the SHA-1 hash, compresses it, and stores it in `.mygit/objects/`.  
2. `add(file_path)`  
   - Calls `hash_object()`  
   - Adds a line to `.mygit/index` in the format:
   <sha1> <file_path>

This allows the commit function to know **which files to include** and where to place them in the project.

---

## Example snippets

### Hash and store a file as a blob
```python
sha1 = hash_object("example.txt")
```

### Example ```.mygit/index``` after adding two files
d3b07384d113edec49eaa6238ad5ff00 src/main.py
4a7d1ed414474e4033ac29ccb8653d9b tests/main.p

## Notes
- The file content is stored in .mygit/objects/ keyed by hash.
- The staging area (index) maps file paths to hashes.
- Files are not part of any commit yet; committing them will create the first snapshot.
- You can call add() multiple times to stage multiple files before committing.
