import os
import csv


def merge_csv_files(directory):
    # Create a 'processed' folder if it doesn't exist
    processed_dir = os.path.join(directory, "processed_photo_details_csvs")
    os.makedirs(processed_dir, exist_ok=True)

    output_file = os.path.join(processed_dir, "merged_photo_details.csv")
    total_rows = 0
    first_file = True

    with open(output_file, 'w', newline='') as outfile:
        writer = None

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)

                # Skip the processed folder
                if os.path.dirname(file_path) == processed_dir:
                    continue

                with open(file_path, 'r', newline='') as infile:
                    reader = csv.reader(infile)

                    if first_file:
                        # Write headers from the first file
                        headers = next(reader)
                        writer = csv.writer(outfile)
                        writer.writerow(headers)
                        first_file = False
                    else:
                        # Skip header for subsequent files
                        next(reader)

                    # Write all rows from this file
                    for row in reader:
                        writer.writerow(row)
                        total_rows += 1

                print(f"Processed: {filename}")

    if total_rows > 0:
        print(f"Merged CSV saved as: {output_file}")
        print(f"Total rows in merged CSV: {total_rows}")
    else:
        print("No CSV files found to merge.")


if __name__ == "__main__":
    photos_all_directory = "."  # Replace with the path of the directory containing all the random-named .csvs (probably inside `Photos_All`)
    merge_csv_files(photos_all_directory)
