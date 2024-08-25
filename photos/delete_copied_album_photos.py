import os
import csv


def delete_photos(source_dir, csv_dir):
    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith('.csv'):
            csv_path = os.path.join(csv_dir, csv_file)

            with open(csv_path, 'r') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if row:
                        image_filename = row[0]
                        file_path = os.path.join(source_dir, image_filename)

                        if os.path.exists(file_path):
                            try:
                                os.remove(file_path)
                                print(f"Deleted: {image_filename}")
                            except PermissionError:
                                print(f"Permission denied: Unable to delete {image_filename}")
                        else:
                            print(f"File not found: {image_filename}")


if __name__ == "__main__":
    photos_dir = "/nextcloud/datadir/admin/files/Photos/Photos"  # Where your photos are
    csv_dir = "icloud_backup/Albums"  # Usually found in one of the iCloud Photos Part X directories

    delete_photos(photos_dir, csv_dir)
