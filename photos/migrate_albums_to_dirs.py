import os
import csv
import shutil
from collections import defaultdict

def organize_photos(source_dir, csv_dir, destination_parent_dir, move_mode=False):
    os.makedirs(destination_parent_dir, exist_ok=True)
    album_counts = defaultdict(int)
    total_processed = 0
    total_errors = 0

    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith('.csv'):
            csv_path = os.path.join(csv_dir, csv_file)
            album_name = os.path.splitext(csv_file)[0]
            destination_dir = os.path.join(destination_parent_dir, album_name)

            os.makedirs(destination_dir, exist_ok=True)

            with open(csv_path, 'r') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if row:
                        image_filename = row[0]
                        source_path = os.path.join(source_dir, image_filename)
                        destination_path = os.path.join(destination_dir, image_filename)

                        if os.path.exists(source_path):
                            try:
                                if move_mode:
                                    shutil.move(source_path, destination_path)
                                    # print(f"Moved: {image_filename} to {album_name}")
                                else:
                                    shutil.copy2(source_path, destination_path)
                                    # print(f"Copied: {image_filename} to {album_name}")
                                album_counts[album_name] += 1
                                total_processed += 1
                            except PermissionError:
                                print(f"Permission denied: Unable to {'move' if move_mode else 'copy'} {image_filename}")
                                total_errors += 1
                        else:
                            print(f"File not found: {image_filename}")
                            total_errors += 1

    for root, dirs, files in os.walk(destination_parent_dir):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.chmod(dir_path, 0o755)
            shutil.chown(dir_path, user='www-data', group='www-data')
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, 0o644)
            shutil.chown(file_path, user='www-data', group='www-data')

    # Print final counts
    print("\nFinal Counts:")
    for album, count in album_counts.items():
        print(f"{album}: {count} files")
    print(f"\nTotal files processed: {total_processed}")
    print(f"Total errors: {total_errors}")


if __name__ == "__main__":
    photos_dir = './Photos_All/Photos'  # Where your photos are
    csv_dir = "icloud_backup/Albums"  # Usually found in one of the iCloud Photos Part X directories
    destination_parent_dir = './Photos_All'  # Usually just parent of photos_dir
    move_mode = False

    organize_photos(photos_dir, csv_dir, destination_parent_dir, move_mode)
