import unittest
import os
import shutil
from photos.add_exif_data import process_files


class TestPhotoProcessing(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_photos'
        self.processed_dir = os.path.join(self.test_dir, 'processed')
        self.csv_path = os.path.join(self.test_dir, 'test_photo_details.csv')

        # Ensure the CSV file exists
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Get the list of original files
        self.original_files = [f for f in os.listdir(self.test_dir)
                               if os.path.isfile(os.path.join(self.test_dir, f)) and f != 'test_photo_details.csv']
    def tearDown(self):
        # Clean up processed directory
        if os.path.exists(self.processed_dir):
            shutil.rmtree(self.processed_dir)

    def test_process_files(self):
        # Run the process_files function and capture its return values
        updated, repaired, failed, no_file = process_files(self.csv_path, self.test_dir)

        # Check if processed directory was created
        self.assertTrue(os.path.exists(self.processed_dir), "Processed directory was not created")

        # Check if all files were processed
        processed_files = os.listdir(self.processed_dir)
        self.assertEqual(set(processed_files), set(self.original_files), "Processed files do not match original files")

        # Check the number of repaired files
        self.assertEqual(repaired, 4, f"Expected 4 files to be repaired, but got {repaired}")

        # Check that there are no failed files
        self.assertEqual(failed, 0, f"Expected 0 failed files, but got {failed}")

        # Check that there are no missing files
        self.assertEqual(no_file, 0, f"Expected 0 missing files, but got {no_file}")

        # Check that the sum of updated and repaired equals the total number of files
        self.assertEqual(updated + repaired, len(self.original_files),
                         f"Sum of updated ({updated}) and repaired ({repaired}) should equal total files ({len(self.original_files)})")


if __name__ == '__main__':
    unittest.main()
