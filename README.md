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
