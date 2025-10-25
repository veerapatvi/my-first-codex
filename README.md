# my-first-codex

## Getting Started

### 1. Set up the project
Clone the repository and move into it:
```bash
git clone <repository-url>
cd my-first-codex
```

(Optional) Create a virtual environment to keep dependencies isolated:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

This project relies only on the Python standard library, so no additional packages are required.

### 2. Run the sample analysis
Use the helper script to total the amounts in a CSV file:
```bash
python scripts/summarize_amounts.py data/sample.csv
```

### Example output
```text
Total amount: 3950.00
```
