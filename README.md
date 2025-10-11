# 🤖 Project 1: Automated File Organizer 📂

A Python command-line utility for **recursive file system management**, designed to automatically scan, categorize, and organize files across a directory tree.

---

## 🏆 Project Goal & Requirements

The primary objective is to develop a robust script that demonstrates mastery of core Python I/O, error handling, and CLI development by creating an automated file organization solution.

| Feature | Status | Core Implementation |
| :--- | :--- | :--- |
| **Directory Traversal** | Recursive scan using `pathlib.Path.rglob('*')`. |
| **File Type Detection** | Extension mapping with a default **"Other"** category. |
| **Conflict Resolution** | Filename conflicts resolved via index: `report(1).txt`. |
| **Error Handling** | Gracefully handles `PermissionError` and checks for invalid paths. |
| **Logging & Reporting** | Detailed logs to `organizer.log` and a final console summary report. |
| **User Experience (CLI)**| Accepts source path via `argparse` and features a `--dry-run` mode. |

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.6+** (No external packages required)

### Execution

The script is executed via the command line, requiring the target directory path as a mandatory argument.

| Mode | Command Syntax | Description |
| :--- | :--- | :--- |
| **Dry-Run (Test Run)** | `python file_organizer.py <source_directory_path> --dry-run` | **Simulates all actions** (moves, directory creation) without modifying the file system. |
| **Live Execution** | `python file_organizer.py <source_directory_path>` | **Executes the organization**, moving files and creating category folders. |

### Example

To run a dry-run on your `Downloads` folder:
```bash
python file_organizer.py /Users/username/Downloads --dry-run
