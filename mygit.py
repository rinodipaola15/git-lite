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


if __name__ == "__main__":
    # Step 1: Initialize the repository
    init()

    # Step 2: Example files to add (create them if they don't exist)
    test_files = ["file1.txt", "file2.txt"]

    for file in test_files:
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write(f"Contents of {file}")

    # Step 3: Stage files using add()
    for file in test_files:
        add(file)

    # Step 4: Show current index content
    index_path = ".mygit/index"
    if os.path.exists(index_path):
        print("\nCurrent staged files (index):")
        with open(index_path, "r") as f:
            print(f.read())

        # Step 5: Read staged file hashes for commit
        files_hashes = []
        with open(index_path, "r") as f:
            for line in f:
                sha1, path = line.strip().split(" ", 1)
                files_hashes.append(sha1)

        # Step 6: Create the commit
        commit_hash = commit(files_hashes, "Initial commit")

        # Step 7: Clear the index after commit
        os.remove(index_path)
        print("Index cleared after commit.")

        # Step 8: View commit history
        print("\n=== Commit History ===")
        log()
    