# MRGit

This is my own implementation of git. Not intended to be used by anyone, not even me.

This is my exploration on how git works, and an attempt of building a very rough and basic version of git on my own.

NOTE: You may be able to use this in an existing git repo (created and managed using the actual git), and it probably works for the most part. But I cannot guarantee that it wont break your repo, so, ideally, don't do that.

## Usage

Install dependencies:

```bash
uv sync
```

Run:

```bash
./mrgit.sh --help
```

If you want access to the more lower level commands, like `write-tree` or `cat-file`, set the environment variable `MRGIT_COMPLEX_MODE` to `"true"`.

## Example Workflow

This git implementation doesn't have a staging area, so every command works over your worktree.

```bash
# Initialize the repo
./mrgit.sh init

# Configure your user
./mrgit.sh config user.name "My Name"
./mrgit.sh config user.email "my@email.com"

# Create some files
echo "File number 1" > file1.txt
mkdir my_folder
echo "File in folder" > my_folder/file2.txt

# Commit your worktree
./mrgit.sh commit -m "Initial Commit"

# Create a branch
./mrgit.sh branch feat/new-branch

# Switch to that branch
./mrgit.sh checkout feat/new-branch

# Make some changes & commit in the new branch
echo "File number 1 - Modified" > file1.txt
echo "New file in folder" > my_folder/file3.txt
./mrgit.sh commit -m "Modifications in branch"

# Checkout main
./mrgit.sh checkout main

# Add a file in main & commit
echo "The final file" > "file4.txt"
./mrgit.sh commit -m "Final commit"
```

At this point, you have two branch with different work trees, verify:

**In main:**

```bash
./mrgit.sh log
ls .
ls my-folder
cat file1.txt
```

The log should only show the initial and final commit.

The `ls` commands should show files 1, 2 and 4, since file 3 was created in the new branch.

The `cat` command should show the original contents of file 1.

**In `feat/new-branch`:**

```bash
./mrgit.sh log
ls .
ls my-folder
cat file1.txt
```

The log should only show the initial and branch modification commits.

The `ls` commands should show files 1, 2 and 3, since file 4 was created in main.

The `cat` command should show the modified contents of file 1.
