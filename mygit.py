import os
import hashlib
import zlib


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

if __name__ == "__main__":
    # Run the initialization only when executing the script directly
    init()


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
