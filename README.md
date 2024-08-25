# iCloud to Nextcloud Migration Guide

This guide documents the process of migrating data from iCloud to Nextcloud, based on personal experience. It includes scripts and step-by-step instructions that may be helpful in your migration journey.

## Who This Guide Is For

This guide is intended for users who are:
- Comfortable with command-line interfaces
- Familiar with Docker and Linux environments
- Possibly new to Nextcloud but experienced with general tech setups
- Looking to migrate their data from iCloud to a self-hosted Nextcloud instance

Note that this guide reflects a personal migration process and may not cover all scenarios. You might need to adapt some steps to your specific situation.

## Table of Contents
1. [Setting Up Nextcloud](#setting-up-nextcloud)
   - [Setting Up Memories in Nextcloud](#setting-up-memories-in-nextcloud)
2. [Downloading iCloud Data](#downloading-icloud-data)
3. [Data Migration Process](#data-migration-process)
   - [Calendars](#calendars)
   - [Contacts](#contacts)
   - [Photos](#photos)
4. [Connecting Devices to Nextcloud](#connecting-devices-to-nextcloud)
   - [Linux](#linux)
   - [Android](#android)

## Setting Up Nextcloud

Before beginning the migration process, it's recommended to set up your Nextcloud instance:

1. For ease of installation and maintenance, consider using Nextcloud AIO (All-In-One). You can find more information and installation instructions at [https://github.com/nextcloud/all-in-one](https://github.com/nextcloud/all-in-one).

2. After setting up Nextcloud, proceed to set up the Memories app as described in the next section.

### Setting Up Memories in Nextcloud

The Memories app in Nextcloud is highly recommended for managing your photo collection, especially when migrating from iCloud. Here's why it's important:

- It provides features similar to what you're used to in iCloud, such as timeline view, face recognition, and location-based browsing.
- It relies on EXIF data to organize and display your photos effectively, which is crucial for the migration process we'll describe later.
- It can handle the playback of various video formats, including those commonly used in iCloud.
- The default Nextcloud Photos app sucks.

To set up Memories:

1. Install the Memories app in your Nextcloud instance if you haven't already.

2. Follow the installation guide at [https://memories.gallery/install/](https://memories.gallery/install/) for detailed setup instructions.

3. It's highly recommended to set up hardware transcoding. This is especially important for videos from iCloud, as many of them use the HEVC codec, which browsers can't play directly. Hardware transcoding will ensure smooth playback of your videos.

   - For instructions on setting up hardware transcoding, visit: [https://memories.gallery/hw-transcoding/](https://memories.gallery/hw-transcoding/)
   - Hardware transcoding can significantly improve performance and reduce CPU usage when viewing videos in Memories.

4. After completing the migration process and uploading your media, you may need to trigger a reindex of your photos and videos. This process will ensure that all your media is properly cataloged and that the new transcoding settings are applied.

## Downloading iCloud Data

To download all your iCloud data:
1. Go to [privacy.apple.com](https://privacy.apple.com)
2. Log in with your Apple ID
3. Request a copy of your data
4. Wait for Apple to process your request and download the data when available. Apparently this can take up to a week - for me, it took 3-4 days.

## Data Migration Process

Before proceeding with the migration, please note the following about the scripts in this repository:

- You will need to modify hardcoded variables in the scripts to match your specific directory structure and file locations:
  - For Bash scripts: Look for variables at the beginning of the script.
  - For Python scripts: Look for variables inside the `if __name__ == "__main__":` block.

- By default, most scripts are set to copy files rather than move them directly. This is the safest option as it preserves your original data. However, it's generally fine and more efficient to move files directly:
  - If you're confident in your setup and have backups, consider changing the scripts to move files instead of copying them.
  - To do this, look for variables or options in the scripts that control whether files are copied or moved, and adjust them accordingly.
  - Moving files directly can significantly speed up the migration process, especially for large collections.

- Always ensure you have backups of your data before running any migration scripts, regardless of whether you're copying or moving files.

- Make sure to review and modify the paths before running any scripts. The paths should point to the relevant data for each script (e.g., vCard files for contact scripts, photo directories for photo scripts).

### Calendars

1. In Nextcloud, go to Calendar
2. Navigate to Settings
3. Select "Import Calendar"
4. Choose the calendar files from your iCloud download

### Contacts

1. (Optional) If you encounter issues importing vCards, run the [remove_image_from_vcard.py](./contacts/remove_image_from_vcard.py) script to remove images from the vCards:
   ```
   python contacts/remove_image_from_vcard.py
   ```
2. Merge the multiple .vcf files from the iCloud download into a single file using the provided script:
   ```
   bash contacts/merge_vcfs.sh
   ```
   You can find the script here: [merge_vcfs.sh](./contacts/merge_vcfs.sh)
3. In Nextcloud, go to Contacts
4. Navigate to Settings
5. Select "Import"
6. Upload the merged .vcf file

### Photos

When migrating photos from iCloud to Nextcloud, there are two main challenges:

1. The iCloud download spreads photos across multiple directories, making organization difficult.
2. The downloaded photos lack EXIF metadata, which is crucial for proper organization in Nextcloud, especially when using the [Memories app](https://apps.nextcloud.com/apps/memories).

The Memories app in Nextcloud is highly recommended for managing your photo collection, as it provides features like timeline view, face recognition, and location-based browsing. However, it relies heavily on EXIF data to function effectively.

To address these challenges and prepare your photos for optimal use with the Memories app, we'll use a series of scripts to consolidate the photos and restore the EXIF metadata. Here's the process:

1. Extracting and moving photos:
   - Script: [move_images.py](./photos/move_images.py)
   - Purpose: This script extracts photos from various folders in your iCloud download and moves them all into a single folder: "Photos_All/Photos".
   - Usage: Run the script, ensuring you've set the correct source path. The script will create the "Photos_All/Photos" directory in the same location as the source.

2. Merging metadata CSV files:
   - Script: [merge_csv.py](./photos/merge_csv.py)
   - Purpose: In the iCloud download, you'll find several randomly named CSV files in the "Photos_All" folder. This script merges all these CSV files into a single metadata file.
   - Usage: Run the script, pointing it to the "Photos_All" directory containing the CSV files.

3. Adding EXIF data to photos:
   - Script: [add_exif_data.py](./photos/add_exif_data.py)
   - Purpose: This script takes the photos in the "Photos_All/Photos" folder and the merged CSV metadata file. It then processes the metadata and adds it as EXIF data to each image file.
   - Usage: Run the script, ensuring you've set the correct paths for the photo directory and the merged metadata CSV file.
   - Note: This process can take a considerable amount of time, potentially multiple hours for large collections (e.g., around 20,000 files). Please be patient and ensure your computer won't go to sleep during this process.

4. (Optional) Adding EXIF data from filenames:
   - Script: [add_exif_data_from_filename.py](./photos/add_exif_data_from_filename.py)
   - Purpose: This script adds metadata to pictures if they have a date in their filename.
   - Usage: Run the script after setting the appropriate variables for your file structure.

5. Migrating albums:
   There are two methods to migrate your albums:

   a. Using Memories albums directly (Recommended):
   - Script: [migrate_albums.py](./photos/migrate_albums.py)
   - Purpose: This script migrates your albums to Memories albums directly.
   - Usage: Run the script after setting the appropriate variables.
   - Note: This method is recommended as it avoids duplicating images that appear in multiple albums.

   b. Creating directories for each album:
   - Script: [migrate_albums_to_dirs.py](./photos/migrate_albums_to_dirs.py)
   - Purpose: This script creates directories for each album and copies the photos into them.
   - Usage: Run the script after setting the appropriate variables.
   - Note: This method will duplicate images if they are in multiple albums.

   If you choose method b and want to delete the original photos after copying:
   - Script: [delete_copied_album_photos.py](./photos/delete_copied_album_photos.py)
   - Purpose: This script deletes the original photos after they've been copied to album directories.
   - Usage: Run this script only after successfully running migrate_albums_to_dirs.py and verifying the copies.

After running these scripts, your photos will be organized with all relevant metadata embedded as EXIF data. This will allow the Nextcloud Memories app to properly organize and display your photos. You can then proceed to upload these processed photos to Nextcloud:

6. Upload photos to Nextcloud
   - If Nextcloud is on the same machine, consider copying the processed files directly into Nextcloud's data directory for large collections.
     - Note: If you copy files directly, permissions might get messed up. Make sure to fix the permissions after copying. You may need to run a command like `chown -R www-data:www-data /path/to/nextcloud/data` (adjust the user and group as necessary for your setup).
   - Otherwise, use the Nextcloud web interface or desktop client to upload the photos.

7. After uploading, run the following commands to ensure Nextcloud recognizes all the new files and indexes them properly:

   For Nextcloud AIO (All-In-One) Docker setups, use this command structure:
   ```
   sudo docker exec --user www-data -it nextcloud-aio-nextcloud php occ [command]
   ```

   Run these specific commands:
   ```
   sudo docker exec --user www-data -it nextcloud-aio-nextcloud php occ files:scan --all
   sudo docker exec --user www-data -it nextcloud-aio-nextcloud php occ memories:index
   ```

   If you're not using Nextcloud AIO, adjust the commands according to your specific Nextcloud installation.

Note: Make sure to review and modify the paths in each script before running them. The scripts are designed to create new data without overwriting original files, but always ensure you have backups before proceeding.

## Connecting Devices to Nextcloud
### Linux
1. Use the "Online Accounts" application to add your Nextcloud account.

Once set up, Nextcloud will automatically integrate with various GNOME applications. For example:
- Calendar app for calendar sync
- Evolution for calendars and contacts

Note: Available integrations may vary depending on your Linux distribution and desktop environment.

### Android
Note: It's recommended to use F-Droid to download and install all the following apps, as it provides open-source versions.

1. Install the Nextcloud app.
2. Set up auto-upload in settings for various photo libraries (e.g., Gallery, Screenshots)
3. For calendar and contacts sync:
   - Install DAVx5
   - Set up DAVx5 (possibly through Nextcloud app settings, or manually)
4. For WebCal calendars, install ICSx5
5. For notes, install the Nextcloud Notes app
6. For photos, install the Memories app
