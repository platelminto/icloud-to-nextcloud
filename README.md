# iCloud to Nextcloud Migration Guide

This repository documents the process of migrating data from iCloud to Nextcloud, including scripts and step-by-step instructions.

## Table of Contents
1. [Downloading iCloud Data](#downloading-icloud-data)
2. [Using the Scripts](#using-the-scripts)
3. [Migrating Specific Data Types](#migrating-specific-data-types)
   - [Calendars](#calendars)
   - [Contacts](#contacts)
   - [Photos](#photos)
4. [Connecting Devices to Nextcloud](#connecting-devices-to-nextcloud)
   - [Linux](#linux)
   - [Android](#android)

## Downloading iCloud Data

To download all your iCloud data:
1. Go to [privacy.apple.com](https://privacy.apple.com)
2. Log in with your Apple ID
3. Request a copy of your data
4. Wait for Apple to process your request and download the data when available

## Using the Scripts

Before proceeding with the migration, please note the following about the scripts in this repository:

- Most scripts will need to have their directory paths modified to match your specific setup:
  - For Python scripts: Look for a variable that sets the input or output directory.
  - For Bash scripts: Check for variables at the beginning of the script that define file or directory paths.

- By default, all scripts create new data and will not overwrite your original files. You can run them without worrying about losing your original data.

- Some scripts contain options to change from only-copy to overwrite/move directly. This can be faster for large migrations. Review the script options carefully before using these modes.

- Make sure to review and modify the paths before running any scripts. The paths should point to the relevant data for each script (e.g., vCard files for contact scripts, photo directories for photo scripts).

## Migrating Specific Data Types

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

1. Use the following scripts to prepare your photos:
   - [move_images.py](./photos/move_images.py): Script to extract photos from different folders into one
   - [Script to merge metadata CSVs]
   - [Script to add metadata as EXIF to photo files]
2. Upload photos to Nextcloud
   - If Nextcloud is on the same machine, consider copying files directly into Nextcloud's data directory for large collections

## Connecting Devices to Nextcloud

### Linux

1. Add an online account for Nextcloud in your system settings

### Android

1. Install the Nextcloud app from the Play Store
2. Set up auto-upload in settings for various photo libraries (e.g., Gallery, Screenshots)
3. For calendar and contacts sync:
   - Install DAVx5
   - Set up DAVx5 (possibly through Nextcloud app settings, or manually)
4. For WebCal calendars, install ICSx5
5. For notes, install the Nextcloud Notes app
6. For photos, install the Memories app

[Additional sections and details to be added]
