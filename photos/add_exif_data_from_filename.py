import os
import subprocess
import shutil
import re
from datetime import datetime


def extract_date_from_filename(filename):
    date_pattern = r'20\d{2}[-._]?(?:0[1-9]|1[0-2])[-._]?(?:0[1-9]|[12]\d|3[01])'
    match = re.search(date_pattern, filename)
    if match:
        date_str = match.group()
        date_str = re.sub(r'\D', '', date_str)
        try:
            return datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            return None
    return None


def process_images(directory, processed_dir=None, move=False, in_place=False, replace_old_metadata=False):
    if not in_place and processed_dir:
        os.makedirs(processed_dir, exist_ok=True)

    stats = {
        'total_files': 0,
        'files_changed': 0,
        'files_skipped_no_date': 0,
        'files_skipped_existing_metadata': 0,
        'files_metadata_replaced': 0,
        'files_error': 0
    }

    for filename in os.listdir(directory):
        stats['total_files'] += 1
        input_file = os.path.join(directory, filename)
        output_file = os.path.join(processed_dir, filename) if not in_place else input_file

        # Extract date from filename
        date_obj = extract_date_from_filename(filename)
        if not date_obj:
            print(f"Couldn't extract date from {filename}, skipping...")
            stats['files_skipped_no_date'] += 1
            continue

        exif_date = date_obj.strftime("%Y:%m:%d 00:00:00")

        # Check if date metadata already exists
        check_command = ["exiftool", "-CreateDate", "-DateTimeOriginal", "-s", "-s", "-s", input_file]
        result = subprocess.run(check_command, capture_output=True, text=True)

        if result.stdout.strip() and not replace_old_metadata:
            print(f"Skipping {filename}: Date metadata already exists")
            stats['files_skipped_existing_metadata'] += 1
            continue

        # Copy or move the file if not in-place
        if not in_place:
            if move:
                shutil.move(input_file, output_file)
                print(f"Moved {filename} to processed directory")
            else:
                shutil.copy2(input_file, output_file)
                print(f"Copied {filename} to processed directory")

        # Prepare exiftool command
        command = [
            "exiftool",
            "-overwrite_original",
            f"-CreateDate={exif_date}",
            f"-DateTimeOriginal={exif_date}",
            output_file
        ]

        # Run exiftool command
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            if result.stdout.strip() and replace_old_metadata:
                print(f"Replaced existing metadata for {filename}")
                stats['files_metadata_replaced'] += 1
            else:
                print(f"Successfully updated metadata for {filename}")
                stats['files_changed'] += 1
        except subprocess.CalledProcessError as e:
            print(f"Error processing {filename}: {e.stderr}")
            stats['files_error'] += 1

    return stats


if __name__ == "__main__":
    # Configuration variables
    input_directory = './Photos_All/Photos'  # Replace with your input directory path
    processed_directory = os.path.join(input_directory, "processed")
    move_files = False  # Set to True if you want to move files instead of copying
    in_place_edit = False  # Set to True for in-place editing (makes move_files useless)
    replace_old_metadata = True  # Set to False if you don't want to replace metadata if it's already there

    stats = process_images(input_directory, processed_directory, move_files, in_place_edit, replace_old_metadata)

    print("\nProcessing complete. Here are the statistics:")
    print(f"Total files processed: {stats['total_files']}")
    print(f"Files with metadata changed: {stats['files_changed']}")
    print(f"Files with metadata replaced: {stats['files_metadata_replaced']}")
    print(f"Files skipped (no date found): {stats['files_skipped_no_date']}")
    print(f"Files skipped (existing metadata): {stats['files_skipped_existing_metadata']}")
    print(f"Files with errors: {stats['files_error']}")
