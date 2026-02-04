# Overview
Small utility to compress pdfs created by iPhone's using the Notes App "Scan Document"

# Setup
Tested with Python 3.1x

```bash
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements
```

# Run
```bash
python compress.py
```

This will prompt for a file or default to ```input.pdf``` and create a file with ```_compressed``` appended to it.

# Sample run:
## Default input
```bash
Enter file name or hit enter to default to [input.pdf]:
Processing [input.pdf] with original size of  26 MB
Saved: input_compressed.pdf with new size of 1 MB  which is  92.52 % smaller
```

## When output already exists you'll be prompted to overwrite
```bash
Enter file name or hit enter to default to [input.pdf]:
Error: input_compressed.pdf already exists.
Overwrite (Y/N)?y
Processing [input.pdf] with original size of  26 MB
Saved: input_compressed.pdf with new size of 1 MB  which is  92.52 % smaller
```
