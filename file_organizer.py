import argparse
import logging
import shutil
import time
from pathlib import Path

# --- Configuration ---

# Map file extensions (lowercase) to their target directory names
CATEGORIES = {
    ".py": "Python_Code",
    ".txt": "Documents",
    ".docx": "Documents",
    ".pdf": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".mp3": "Audio",
    ".mp4": "Videos",
    # Add more mappings as needed
}

# Configure logging to write to 'organizer.log' file
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

# --- Core Logic ---

def get_target_path(item: Path, target_dir: Path) -> Path:
    """
    Determines the safe final path for a file, handling filename conflicts.
    Conflict resolution: report.txt becomes report (1).txt, report (2).txt, etc.
    """
    target_path = target_dir / item.name
    counter = 0

    while target_path.exists():
        counter += 1
        # Example conflict resolution: report.txt -> report (1).txt
        new_name = f"{item.stem} ({counter}){item.suffix}"
        target_path = target_dir / new_name
    
    if counter > 0:
        logging.warning(f"Conflict resolved: {item.name} renamed to {target_path.name}")
        
    return target_path

def organize_directory(source_dir: Path, dry_run: bool = False):
    """
    Scans and organizes files in the source directory.
    
    Args:
        source_dir: The directory to scan.
        dry_run: If True, only previews actions without moving files.
    """
    
    # Report tracking
    total_files_scanned = 0
    files_moved_count = 0
    errors_encountered = 0
    
    logging.info(f"--- Starting organization for: {source_dir} (Dry-Run: {dry_run}) ---")
    
    try:
        # Use Path.iterdir() for a flat scan of the source directory, 
        # as a recursive scan (os.walk/Path.glob('**/*')) can be complex for a simple first project.
        for item in source_dir.iterdir():
            if item.is_file():
                total_files_scanned += 1
                
                # 1. File Type Detection
                ext = item.suffix.lower()
                # Map extension to category, defaulting to "Other"
                category = CATEGORIES.get(ext, "Other")
                target_dir = source_dir / category
                
                # 2. Directory Creation
                if not target_dir.exists():
                    logging.info(f"Creating directory: {target_dir.name}")
                    if not dry_run:
                        # Use exist_ok=True to prevent race conditions/errors if directory is created by another process
                        target_dir.mkdir(exist_ok=True) 

                # 3. Conflict Resolution
                target_path = get_target_path(item, target_dir)
                
                # 4. Logging and Movement
                action_msg = f"{'DRY-RUN: Will move' if dry_run else 'Moving'} {item.name} to {target_path.relative_to(source_dir)}"
                logging.info(action_msg)

                if not dry_run:
                    try:
                        # Safe file moving
                        shutil.move(str(item), str(target_path))
                        files_moved_count += 1
                    except PermissionError:
                        errors_encountered += 1
                        logging.error(f"Permission Error: Could not move {item.name}")
                    except Exception as e:
                        errors_encountered += 1
                        logging.error(f"Error moving {item.name}: {e}")

    except FileNotFoundError:
        errors_encountered += 1
        logging.critical(f"Source directory not found: {source_dir}")
    except PermissionError:
        errors_encountered += 1
        logging.critical(f"Permission Denied accessing source directory: {source_dir}")
    except Exception as e:
        errors_encountered += 1
        logging.critical(f"An unexpected error occurred: {e}")

    # --- Summary Report ---
    logging.info("--- Summary Report ---")
    logging.info(f"Total files scanned: {total_files_scanned}")
    logging.info(f"Files successfully moved: {files_moved_count}")
    logging.info(f"Errors encountered: {errors_encountered}")
    logging.info(f"Log details are in 'organizer.log'")


# --- CLI Integration ---

if __name__ == "__main__":
    # Setup argument parsing for the command-line interface (CLI)
    parser = argparse.ArgumentParser(
        description="Automated File Organizer: Scans a directory and organizes files by extension."
    )
    # Positional argument for the source directory
    parser.add_argument(
        "source", 
        help="Directory to organize (e.g., /path/to/downloads)"
    )
    # Optional flag for dry-run mode
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Preview changes without actually moving files."
    )
    
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    source_path = Path(args.source).resolve()
    organize_directory(source_path, args.dry_run)