import argparse
import logging
import shutil
from pathlib import Path

# --- Configuration ---
CATEGORIES = {
    ".py": "Python_Code",
    ".txt": "Documents",
    ".pdf": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".zip": "Archives",
    # Add more categories here
}

# Configure logging
logging.basicConfig(
    filename='organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def get_target_path(item: Path, target_dir: Path) -> Path:
    """
    Determines the safe final path for a file, handling filename conflicts
    using the requested file (1).ext format.
    """
    target_path = target_dir / item.name
    counter = 0

    # Resolve filename conflicts [cite: 13]
    while target_path.exists():
        counter += 1
        new_name = f"{item.stem} ({counter}){item.suffix}"
        target_path = target_dir / new_name
    
    if counter > 0:
        logging.warning(f"Conflict resolved: {item.name} renamed to {target_path.name}")
        
    return target_path

def organize_directory(source_dir: Path, dry_run: bool = False):
    """
    Recursively scans and organizes files in the source directory.
    """
    
    total_files_scanned = 0
    files_moved_count = 0
    errors_encountered = 0
    
    logging.info(f"--- Starting organization for: {source_dir.name} (Dry-Run: {dry_run}) ---")
    
    # Recursively scan all files in the directory and subdirectories [cite: 8, 22]
    for item in source_dir.rglob('*'):
        if item.is_file(): # Identify files while skipping directories/symlinks [cite: 8]
            total_files_scanned += 1
            
            # File Type Detection [cite: 9]
            ext = item.suffix.lower()
            category = CATEGORIES.get(ext, "Other") # Handle unrecognized extensions in an "Other" folder. [cite: 11]
            
            target_dir = source_dir / category
            
            # Directory Creation [cite: 26]
            if not target_dir.exists():
                logging.info(f"Creating category directory: {target_dir.name}")
                if not dry_run:
                    target_dir.mkdir(exist_ok=True)

            # Conflict Resolution [cite: 13]
            target_path = get_target_path(item, target_dir)
            
            # Logging and Movement [cite: 15]
            action_msg = f"{'DRY-RUN: Will move' if dry_run else 'Moving'} {item.relative_to(source_dir)} to {target_path.relative_to(source_dir)}"
            logging.info(action_msg)

            if not dry_run:
                try:
                    # Safe file moving/shutil [cite: 27]
                    shutil.move(str(item), str(target_path))
                    files_moved_count += 1
                except PermissionError: # Gracefully handle permission errors [cite: 14, 29]
                    errors_encountered += 1
                    logging.error(f"Permission Error: Could not move {item.name}. Skipping.")
                except Exception as e: # Handle other OS errors [cite: 29]
                    errors_encountered += 1
                    logging.error(f"Error moving {item.name}: {e}. Skipping.")

    # Summary Report [cite: 18]
    print("\n" + "="*40)
    print("      ORGANIZATION SUMMARY REPORT")
    print("="*40)
    print(f"Directory Scanned: {source_dir}")
    print(f"Total files scanned: {total_files_scanned}")
    print(f"Files successfully moved: {files_moved_count}")
    print(f"Errors encountered (permission, etc.): {errors_encountered}")
    print(f"Detailed activity log: organizer.log")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automated File Organizer: Scans a directory and recursively organizes files by extension."
    )
    # Accept source directory via command-line arguments [cite: 19]
    parser.add_argument(
        "source", 
        help="Directory to organize (e.g., /path/to/downloads)"
    )
    # Add dry-run mode [cite: 19]
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Preview changes without actually moving files."
    )
    
    args = parser.parse_args()
    
    source_path = Path(args.source).resolve()
    # Handle invalid paths [cite: 14]
    if not source_path.is_dir():
        logging.critical(f"Invalid source path or not a directory: {source_path}")
    else:
        organize_directory(source_path, args.dry_run)
