import os
import hashlib
import zlib
import time


def init():
    """
    Initialize a minimal Git-like repository in the current folder.
    
    Creates the following structure:
    .mygit/
        objects/ -> stores files and commits
        refs/ -> stores branch references
        HEAD -> points to the current branch

    Notes:
    - The HEAD file contains the reference to the current branch, initially "refs/master".
    - This function should be run only once per project, like 'git init'.
    """
    # Create the main folder .mygit and subfolders
    os.makedirs(".mygit/objects", exist_ok=True)  # stores file blobs and commit objects
    os.makedirs(".mygit/refs", exist_ok=True)     # stores branch references

    # Create HEAD file pointing to the master branch
    # HEAD tells Git which branch is currently active
    with open(".mygit/HEAD", "w") as f:
        f.write("refs/master")  # initial branch is master

    print("Repository '.mygit/' created successfully!")


def hash_object(file_path):
    """
    Add a file to the repository as a blob.
    
    Steps:
    1. Read the file content.
    2. Compute SHA-1 hash.
    3. Compress content and store in .mygit/objects/<hash>.
    """
    with open(file_path, "rb") as f:
        data = f.read()
    
    # Compute SHA-1 hash
    sha1 = hashlib.sha1(data).hexdigest()
    
    # Compress the content
    compressed = zlib.compress(data)
    
    # Save in objects folder
    obj_path = f".mygit/objects/{sha1}"
    with open(obj_path, "wb") as f:
        f.write(compressed)
    
    print(f"File '{file_path}' added with hash {sha1}")
    return sha1


def add(file_path):
    """
    Stage a file for the next commit.
    - Adds the file as a blob to .mygit/objects
    - Records its SHA-1 in the index file
    """
    sha1 = hash_object(file_path)
    
    # Append the file hash and path to the index
    os.makedirs(".mygit", exist_ok=True)
    index_path = ".mygit/index"
    with open(index_path, "a") as index:
        index.write(f"{sha1} {file_path}\n")
    
    print(f"File '{file_path}' staged for commit.")


def commit(files_hashes, message):
    """
    Create a commit object.

    files_hashes: list of SHA-1 hashes of added files (blobs)
    message: commit message
    """
    # Step 1: Create a tree object (a simple string of file hashes)
    tree_content = "\n".join(files_hashes)
    tree_hash = hashlib.sha1(tree_content.encode()).hexdigest()
    
    # Save the tree object
    with open(f".mygit/objects/{tree_hash}", "wb") as f:
        f.write(zlib.compress(tree_content.encode()))

    # Step 2: Prepare commit data
    parent_hash = None
    branch_ref = ".mygit/refs/master"
    if os.path.exists(branch_ref):
        with open(branch_ref, "r") as f:
            parent_hash = f.read().strip()
    
    commit_data = f"tree {tree_hash}\n"
    if parent_hash:
        commit_data += f"parent {parent_hash}\n"
    commit_data += f"date {int(time.time())}\nmessage {message}"

    # Step 3: Compute commit hash and save
    commit_hash = hashlib.sha1(commit_data.encode()).hexdigest()
    with open(f".mygit/objects/{commit_hash}", "wb") as f:
        f.write(zlib.compress(commit_data.encode()))

    # Step 4: Update branch reference
    with open(branch_ref, "w") as f:
        f.write(commit_hash)
    
    print(f"Commit created: {commit_hash}")
    return commit_hash


def log():
    """
    Print the commit history of the current branch (master).
    """
    # Step 1: Get current branch from HEAD
    with open(".mygit/HEAD", "r") as f:
        branch_ref = f.read().strip()  # e.g., refs/master

    branch_file = f".mygit/{branch_ref}"
    if not os.path.exists(branch_file):
        print("No commits yet.")
        return

    # Step 2: Start from last commit
    with open(branch_file, "r") as f:
        commit_hash = f.read().strip()

    # Step 3: Traverse commit chain
    while commit_hash:
        obj_path = f".mygit/objects/{commit_hash}"
        with open(obj_path, "rb") as f:
            data = zlib.decompress(f.read()).decode()

        # Parse commit fields
        lines = data.split("\n")
        commit_info = {}
        for line in lines:
            if line.startswith("tree "):
                commit_info["tree"] = line[5:]
            elif line.startswith("parent "):
                commit_info["parent"] = line[7:]
            elif line.startswith("date "):
                commit_info["date"] = line[5:]
            elif line.startswith("message "):
                commit_info["message"] = line[8:]

        # Print commit info
        print(f"Commit: {commit_hash}")
        print(f"Date: {time.ctime(int(commit_info.get('date', '0')))}")
        print(f"Message: {commit_info.get('message','')}")
        print("-" * 40)

        # Move to parent commit
        commit_hash = commit_info.get("parent")


def branch(name):
    """
    Create a new branch with the given name.
    
    - Copies the current commit hash from the active branch.
    - Saves it in .mygit/refs/<branch_name>.
    """
    # Get current branch and commit
    with open(".mygit/HEAD", "r") as f:
        current_branch_ref = f.read().strip()
    
    branch_file = f".mygit/{current_branch_ref}"
    if os.path.exists(branch_file):
        with open(branch_file, "r") as f:
            current_commit = f.read().strip()
    else:
        current_commit = None

    # Create new branch reference
    new_branch_file = f".mygit/refs/{name}"
    if os.path.exists(new_branch_file):
        print(f"Branch '{name}' already exists.")
        return
    with open(new_branch_file, "w") as f:
        if current_commit:
            f.write(current_commit)
    
    print(f"Branch '{name}' created successfully.")


def checkout(name):
    """
    Switch to the specified branch.
    
    - Updates HEAD to point to the new branch.
    - Optionally, you could update working directory to match last commit.
    """
    branch_file = f".mygit/refs/{name}"
    if not os.path.exists(branch_file):
        print(f"Branch '{name}' does not exist.")
        return
    
    # Update HEAD
    with open(".mygit/HEAD", "w") as f:
        f.write(f"refs/{name}")
    
    print(f"Switched to branch '{name}'.")


def status():
    """
    Print the repository status: staged files and modified files.
    """
    
    index_path = ".mygit/index"
    staged = {}

    # Read index if exists
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 1)
                if len(parts) != 2:
                    continue  # skip malformed lines
                sha1, path = parts
                staged[path] = sha1

    if staged:
        print("Staged files:")
        for path in staged:
            print(f"  {path}")
    else:
        print("No files staged.")

    # Detect modified files
    # (for simplicity, list files in current folder that differ from last commit)
    print("Modified files:")
    for file in os.listdir("."):
        if os.path.isfile(file) and not file.startswith("."):
            if file not in staged:
                print(f"  {file}")


def merge(source_branch):
    """
    Perform a fast-forward merge of `source_branch` into the current branch.

    Steps:
    1. Determine current branch from HEAD.
    2. Get the latest commit of both current and source branches.
    3. If current branch is behind, move its pointer to source branch commit (fast-forward).
    4. If current branch has commits ahead, report that merge is not fast-forward (conflict situation).
    """
    # 1. Get current branch
    with open(".mygit/HEAD", "r") as f:
        current_branch_ref = f.read().strip()  # e.g., "refs/master"
    current_branch_file = f".mygit/{current_branch_ref}"

    # 2. Source branch file
    source_branch_file = f".mygit/refs/{source_branch}"
    if not os.path.exists(source_branch_file):
        print(f"Source branch '{source_branch}' does not exist.")
        return

    # 3. Get latest commits
    current_commit = None
    if os.path.exists(current_branch_file):
        with open(current_branch_file, "r") as f:
            current_commit = f.read().strip()

    with open(source_branch_file, "r") as f:
        source_commit = f.read().strip()

    # 4. Check fast-forward
    if current_commit == source_commit:
        print(f"Branches already identical. Nothing to merge.")
        return
    elif current_commit is None:
        # Current branch has no commits -> just fast-forward
        with open(current_branch_file, "w") as f:
            f.write(source_commit)
        print(f"Fast-forward merge done: {source_branch} -> {current_branch_ref}")
        return
    else:
        # For simplicity, assume we can only fast-forward if current_commit is ancestor
        # Here we skip ancestry check and just report conflict
        print(f"Cannot fast-forward merge: current branch has commits ahead.")
        print(f"Advanced merge with conflicts not implemented yet.")
        return


if __name__ == "__main__":
    import shutil

    # --- Clean start ---
    if os.path.exists(".mygit"):
        shutil.rmtree(".mygit")
    for f in ["file1.txt", "file2.txt"]:
        if os.path.exists(f):
            os.remove(f)
    print("Clean environment ready.\n")

    # --- Step 1: Initialize repository ---
    init()

    # --- Step 2: Create example files ---
    test_files = ["file1.txt", "file2.txt"]
    for file in test_files:
        with open(file, "w") as f:
            f.write(f"Contents of {file}")

    # --- Step 3: Stage and commit files on master ---
    for file in test_files:
        add(file)

    files_hashes = []
    with open(".mygit/index", "r") as f:
        for line in f:
            sha1, path = line.strip().split(" ", 1)
            files_hashes.append(sha1)
    commit(files_hashes, "Initial commit on master")
    os.remove(".mygit/index")

    # --- Step 4: Show status and log ---
    print("\n=== Repository Status ===")
    status()
    print("\n=== Commit History ===")
    log()

    # --- Step 5: Create a new branch 'dev' and switch ---
    branch_name = "dev"
    with open(f".mygit/refs/{branch_name}", "w") as f:
        with open(".mygit/refs/master", "r") as master_ref:
            f.write(master_ref.read().strip())
    checkout(branch_name)

    # --- Step 6: Make changes on 'dev' ---
    with open("file1.txt", "a") as f:
        f.write("\nChanges on dev branch")
    add("file1.txt")
    files_hashes = []
    with open(".mygit/index", "r") as f:
        for line in f:
            sha1, path = line.strip().split(" ", 1)
            files_hashes.append(sha1)
    commit(files_hashes, "Update file1.txt on dev branch")
    os.remove(".mygit/index")

    # --- Step 7: Show status and log on 'dev' ---
    print("\n=== Repository Status on 'dev' ===")
    status()
    print("\n=== Commit History on 'dev' ===")
    log()

    # --- Step 8: Switch back to master ---
    checkout("master")

    # --- Step 9: Merge dev into master ---
    print("\nAttempting fast-forward merge 'dev' -> 'master'...\n")
    merge("dev")

    # --- Step 10: Final status and log of master ---
    print("\n=== Final Repository Status on 'master' ===")
    status()
    print("\n=== Final Commit History on 'master' ===")
    log()
