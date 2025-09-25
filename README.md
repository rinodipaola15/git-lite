# GitLite

A minimal Git-like version control system for learning purposes.

This project is designed to help understand the internal mechanics of version control systems like Git.  
It is developed step by step, focusing on learning how files, commits, branches, and history management work.

## Project structure

- `mygit.py` : main Python script that implements the repository commands
- `.mygit/` : hidden folder created by `init()`, stores repository data
  - `objects/` : stores file contents (blobs) and commits
  - `refs/` : stores branch references
  - `HEAD` : points to the current branch
- `docs/` : step-by-step documentation for each feature, in Markdown
- `README.md` : this file

## Getting started

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run the initialization command:

```bash
python mygit.py
