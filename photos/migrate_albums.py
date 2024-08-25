import os
import csv
import subprocess
from collections import defaultdict


# Change if you run occ differently.
def run_occ_command(command):
    full_command = f"sudo docker exec --user www-data -it nextcloud-aio-nextcloud php occ {command}"
    return subprocess.run(full_command, shell=True, check=False, capture_output=True, text=True)


def create_albums_and_add_photos(csv_dir, photos_dir):
    album_counts = defaultdict(int)
    total_processed = 0
    total_errors = 0

    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith('.csv'):
            csv_path = os.path.join(csv_dir, csv_file)
            album_name = os.path.splitext(csv_file)[0]

            # Create album using OCC command
            create_album_cmd = f"photos:albums:create admin \"{album_name}\""
            result = run_occ_command(create_album_cmd)
            if result.returncode == 0:
                print(f"Created album: {album_name}")
            else:
                print(f"Error creating album {album_name}: {result.stdout}")
                # continue

            if "WhatsApp" in album_name:
                continue

            with open(csv_path, 'r') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if row:
                        image_filename = row[0]
                        full_image_path = os.path.join(photos_dir, image_filename)

                        # Add photo to album using OCC command
                        add_photo_cmd = f"photos:albums:add admin \"{album_name}\" \"{full_image_path}\""
                        result = run_occ_command(add_photo_cmd)
                        if result.returncode == 0:
                            album_counts[album_name] += 1
                            total_processed += 1
                            print(f"Added {image_filename} to album {album_name}")
                        else:
                            print(f"Error adding {image_filename} to album {album_name}: {result.stdout}")
                            total_errors += 1

    # Print final counts
    print("\nFinal Counts:")
    for album, count in album_counts.items():
        print(f"{album}: {count} files")
    print(f"\nTotal files processed: {total_processed}")
    print(f"Total errors: {total_errors}")


if __name__ == "__main__":
    photos_dir = "/nextcloud/datadir/admin/files/Photos/Photos"  # Where your photos are
    csv_dir = "icloud_backup/Albums"  # Usually found in one of the iCloud Photos Part X directories
    create_albums_and_add_photos(csv_dir, photos_dir)
