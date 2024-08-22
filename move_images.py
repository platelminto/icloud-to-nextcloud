import os
import shutil
import random
import string

def random_string(length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def process_icloud_folders(base_dir):
    # Create the Photos_All directory if it doesn't exist
    photos_all_dir = os.path.join(base_dir, "Photos_All")
    os.makedirs(photos_all_dir, exist_ok=True)

    # Iterate through all directories in the base directory
    for dir_name in os.listdir(base_dir):
        if dir_name.startswith("iCloud Photos Part"):
            full_dir_path = os.path.join(base_dir, dir_name)
            print(dir_name)
            if os.path.isdir(full_dir_path):
                photos_dir = os.path.join(full_dir_path, "Photos")
                if os.path.exists(photos_dir):
                    # Process CSV files
                    for filename in os.listdir(photos_dir):
                        if filename.endswith(".csv"):
                            old_path = os.path.join(photos_dir, filename)
                            new_filename = f"{random_string()}.csv"
                            new_path = os.path.join(photos_all_dir, new_filename)
                            shutil.copy2(old_path, new_path)
                            print(f"Copied and renamed: {filename} -> {new_filename}")

                    # Copy contents of Photos directory
                    for item in os.listdir(photos_dir):
                        old_path = os.path.join(photos_dir, item)
                        new_path = os.path.join(photos_all_dir, "Photos", item)
                        # Create Photos subdirectory in Photos_All if it doesn't exist
                        os.makedirs(os.path.join(photos_all_dir, "Photos"), exist_ok=True)
                        # Copy the item
                        if os.path.isdir(old_path):
                            shutil.copytree(old_path, new_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(old_path, new_path)
                        # print(f"Copied: {item} to Photos_All/Photos/")

if __name__ == "__main__":
    base_directory = "/home/platelminto/Documents/local/apple_backup_20082024"  # Replace with your actual path
    process_icloud_folders(base_directory)
