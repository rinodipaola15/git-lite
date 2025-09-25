import os

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
