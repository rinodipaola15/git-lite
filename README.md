# GitLite

## 🗂️ Overview

A minimal Git-like version control system for learning purposes.

This project is designed to help understand the **core internal mechanics** of version control systems like Git — how files are tracked, staged, committed, branched, and merged.  
It is built **step by step**, focusing on clarity and conceptual learning rather than performance or completeness.

---

## 🧩 Project structure

project/
│
├── mygit.py # Main Python script implementing all GitLite commands
├── docs/ # Step-by-step explanations of each feature
├── README.md # Project documentation (this file)
└── .mygit/ # Hidden folder automatically created by init()
├── objects/ # Stores file contents (blobs) and commits
├── refs/ # Contains branch references (e.g. master, dev)
└── HEAD # Points to the current branch or commit

## 🚀 Getting started

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run the initialization command:

```bash
python mygit.py
```

By default, it will:
- Initialize a new .mygit/ repository
- Create and stage example files
- Perform a first commit
- Create a new branch (dev)
- Switch branches
- Display repository status and commit history.


---

## 🧠 Core Concepts

GitLite mimics Git’s main internal components:

| Concept | Description |
|----------|-------------|
| **Blob** | A file snapshot stored as a hashed object in `.mygit/objects/`. |
| **Index** | The staging area, containing file hashes ready to be committed. |
| **Commit** | A snapshot of the project at a given moment, storing a tree, parent, timestamp, and message. |
| **Branch** | A movable pointer to a specific commit (e.g. `refs/master`). |
| **HEAD** | Reference to the current branch or commit. |
| **Fast-forward merge** | A simple merge where the target branch moves its pointer forward to the latest commit. |

## ⚙️ Implemented Commands

| Command | Description |
|----------|-------------|
| `init()` | Initializes a new repository structure. |
| `add()` | Stages files by hashing and saving them as blob objects. |
| `commit()` | Creates a new commit object and updates the current branch. |
| `log()` | Prints the commit history (from latest to oldest). |
| `branch()` | Creates new branches. |
| `checkout()` | Switches between branches. |
| `status()` | Shows staged and modified files. |
| `merge()` | Performs a fast-forward merge when possible. |

## 🧪 Example Flow

```python
# Initialize a new repo
init()

# Add and commit files
add("file1.txt")
add("file2.txt")
commit(["file1.txt", "file2.txt"], "Initial commit")

# Create and switch to a new branch
create_branch("dev")
checkout("dev")

# Modify files, stage, and commit again
add("file1.txt")
commit(["file1.txt"], "Update file1 on dev branch")

# Merge dev into master
checkout("master")
merge("dev")

# View commit history and status
log()
status()
```

## 🧭 Next Steps

GitLite currently supports the **core workflow** of Git (init → add → commit → branch → merge).  
Planned or possible extensions include:

- 🧱 **Non–fast-forward merge** (handling divergent histories)
- ⏪ **Reset / Revert** (undo commits)
- 💾 **Stash** (temporary storage for uncommitted changes)
- 🏷️ **Tag** (marking important commits)
- 🌐 **Remote / Push / Pull** (multi-repository synchronization)
- 🔍 **Diff** (compare file states)

## 👤 Author

Developed by **Rino Di Paola**  
Created as an educational project to explore how Git works under the hood.
