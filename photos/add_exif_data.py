import csv
import subprocess
from datetime import datetime
import os
import shutil


def parse_date(date_string):
    return datetime.strptime(date_string, "%A %B %d,%Y %I:%M %p %Z")


def add_metadata(input_file, output_file, creation_date):
    exif_date = creation_date.strftime("%Y:%m:%d %H:%M:%S")

    if input_file.lower().endswith('.mp4'):
        command = [
            "exiftool",
            "-overwrite_original",
            f"-CreateDate={exif_date}",
            f"-ModifyDate={exif_date}",
            f"-MediaCreateDate={exif_date}",
            f"-MediaModifyDate={exif_date}",
            f"-TrackCreateDate={exif_date}",
            f"-TrackModifyDate={exif_date}",
            f"-o={output_file}",
            input_file
        ]
    else:
        command = [
            "exiftool",
            "-overwrite_original",
            f"-CreateDate={exif_date}",
            f"-DateTimeOriginal={exif_date}",
            f"-o={output_file}",
            input_file
        ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)


def repair_mp4(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-c", "copy",
        "-f", "mp4",
        output_file
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def process_files(csv_path, photos_dir):
    processed_dir = os.path.join(photos_dir, 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        updated = 0
        failed = 0
        repaired = 0
        no_file = 0
        total = 0
        for row in reader:
            total += 1
            file_name = row['imgName']
            input_file = os.path.join(photos_dir, file_name)
            output_file = os.path.join(processed_dir, file_name)

            if os.path.exists(input_file):
                creation_date = parse_date(row['originalCreationDate'])
                try:
                    shutil.copy2(input_file, output_file)
                    add_metadata(output_file, output_file, creation_date)
                    updated += 1
                    print(f"Successfully updated metadata for {file_name}")
                except subprocess.CalledProcessError as e:
                    error_output = e.stdout + e.stderr
                    if "Truncated" in error_output or "Possible garbage" in error_output:
                        if input_file.lower().endswith('.mp4'):
                            print(f"Attempting to repair {file_name}")
                            try:
                                repair_mp4(input_file, output_file)
                                add_metadata(output_file, output_file, creation_date)
                                repaired += 1
                                print(f"Successfully repaired and updated metadata for {file_name}")
                            except subprocess.CalledProcessError as repair_error:
                                print(f"Failed to repair {file_name}")
                                print(f"Error: {repair_error.stdout}")
                                print(f"Error (stderr): {repair_error.stderr}")
                                failed += 1
                        else:
                            print(f"Cannot repair non-MP4 file: {file_name}")
                            failed += 1
                    else:
                        print(f"Failed to update metadata for {file_name}")
                        print(f"Error: {error_output}")
                        failed += 1
            else:
                no_file += 1
                print(f"File not found: {file_name}")

        print(f"Processed {total} files.")
        print(f"Updated metadata for {updated+repaired}/{total} files. ({repaired} repaired)")
        print(f"Failed to update metadata for {failed}/{total} files.")
        print(f"{no_file}/{total} files not found.")
        print("Maths adds up check: ", updated + repaired + failed + no_file == total)

    return updated, repaired, failed, no_file

if __name__ == '__main__':
    csv_path = './Photos_All/merged_photo_details.csv'
    photos_dir = './Photos_All/Photos'
    process_files(csv_path, photos_dir)
