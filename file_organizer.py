import argparse
import logging
import shutil
from pathlib import Path

CATEGORIES = {
    ".py": "Python_Code",
    ".txt": "Documents",
    ".jpg": "Images",
}

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
    target_path = target_dir / item.name
    counter = 0

    while target_path.exists():
        counter += 1
        new_name = f"{item.stem} ({counter}){item.suffix}"
        target_path = target_dir / new_name
    
    if counter > 0:
        logging.warning(f"Conflict resolved: {item.name} renamed to {target_path.name}")
        
    return target_path

def organize_directory(source_dir: Path, dry_run: bool = False):
    
    total_files_scanned = 0
    files_moved_count = 0
    errors_encountered = 0
    
    logging.info(f"--- Starting organization for: {source_dir.name} (Dry-Run: {dry_run}) ---")
    
    for item in source_dir.rglob('*'):
        [cite_start]if item.is_file(): [cite: 8]
            total_files_scanned += 1
            
            ext = item.suffix.lower()
            [cite_start]category = CATEGORIES.get(ext, "Other") [cite: 11]
            
            target_dir = source_dir / category
            
            if not target_dir.exists():
                logging.info(f"Creating category directory: {target_dir.name}")
                if not dry_run:
                    [cite_start]target_dir.mkdir(exist_ok=True) [cite: 26]

            target_path = get_target_path(item, target_dir)
            
            action_msg = f"{'DRY-RUN: Will move' if dry_run else 'Moving'} {item.relative_to(source_dir)} to {target_path.relative_to(source_dir)}"
            [cite_start]logging.info(action_msg) [cite: 15]

            if not dry_run:
                try:
                    [cite_start]shutil.move(str(item), str(target_path)) [cite: 27]
                    files_moved_count += 1
                except PermissionError:
                    errors_encountered += 1
                    logging.error(f"Permission Error: Could not move {item.name}. Skipping.")
                except Exception as e:
                    errors_encountered += 1
                    [cite_start]logging.error(f"Error moving {item.name}: {e}. Skipping.") [cite: 29]

    print("\n" + "="*40)
    [cite_start]print("      ORGANIZATION SUMMARY REPORT") [cite: 18]
    print("="*40)
    print(f"Directory Scanned: {source_dir}")
    print(f"Total files scanned: {total_files_scanned}")
    print(f"Files successfully moved: {files_moved_count}")
    print(f"Errors encountered (permission, etc.): {errors_encountered}")
    print(f"Detailed activity log: organizer.log")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automated File Organizer: Scans a directory and organizes files by extension."
    [cite_start]) [cite: 35]
    parser.add_argument(
        "source", 
        help="Directory to organize (e.g., /path/to/downloads)"
    [cite_start]) [cite: 19]
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Preview changes without actually moving files."
    [cite_start]) [cite: 19]
    
    args = parser.parse_args()
    
    source_path = Path(args.source).resolve()
    [cite_start]if not source_path.is_dir(): [cite: 14]
        [cite_start]logging.critical(f"Invalid source path or not a directory: {source_path}") [cite: 29]
    else:
        organize_directory(source_path, args.dry_run)
