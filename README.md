 📂 Project 1: Automated File Organizer

 Description
[cite_start]This project is a **Python command-line utility** designed to automatically organize files within a specified source directory and its subdirectories[cite: 3]. [cite_start]The script identifies files by their extensions and moves them into categorized folders (e.g., "Documents", "Images", "Code")[cite: 4]. [cite_start]It handles edge cases like filename conflicts and logs all operations for operational transparency[cite: 5, 33].

---

 Key Features

* [cite_start]**Recursive Traversal:** Scans the specified source directory and all its subdirectories for files[cite: 8].
* **Categorization:** Maps file extensions (defined in the `CATEGORIES` dictionary) to corresponding category folders. [cite_start]Unrecognized extensions are grouped into an **"Other"** folder[cite: 10, 11].
* [cite_start]**Conflict Resolution:** Resolves duplicate filenames by appending an index to the filename, following the format `report(1).txt` if `report.txt` already exists[cite: 13].
* [cite_start]**Robust Error Handling:** Gracefully handles OS errors, such as `PermissionError` and `FileNotFoundError`, during file system manipulation[cite: 14, 29].
* [cite_start]**Logging & Reporting:** Logs all successes, failures, and operational steps with timestamps to an `organizer.log` file[cite: 15, 16]. [cite_start]A summary report is also generated upon completion.
* [cite_start]**Dry-Run Mode:** Supports a dry-run mode to preview all proposed actions without actually moving or modifying any files[cite: 19, 36].

---

 Installation and Setup

 Prerequisites
* Python 3.6+ (or newer)
* The script uses only standard Python libraries (`argparse`, `logging`, `shutil`, `pathlib`).

 Files
1.  Save the Python script as `file_organizer.py`.
2.  Ensure you have a `.gitignore` file to exclude logs and test directories.

---

 How to Run

The script is executed via the command line and requires the path to the directory you wish to organize.

 1. Dry-Run Mode (Recommended First)
Use the `--dry-run` flag to preview exactly which files will be moved. [cite_start]The summary report will still be displayed, and all actions will be logged in `organizer.log` as "DRY-RUN" actions[cite: 19].

```bash
# Example command using the dry-run flag
python file_organizer.py /path/to/your/downloads/ --dry-run
