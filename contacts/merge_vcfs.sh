#!/bin/bash

# Set the directory containing your VCF files
VCF_DIRECTORY="."

# Set the output file name
MERGED_FILE="merged_contacts.vcf"

# Function to merge VCF files
merge_vcf_files() {
    echo "Merging VCF files..."
    
    # Ensure the output file doesn't exist
    rm -f "$MERGED_FILE"
    
    # Find all .vcf files and concatenate them
    find "$VCF_DIRECTORY" -maxdepth 1 -name '*.vcf' -print0 | xargs -0 cat > "$MERGED_FILE"
    
    # Check if the merge was successful
    if [ -s "$MERGED_FILE" ]; then
        echo "VCF files merged successfully into $MERGED_FILE"
        echo "Total contacts merged: $(grep -c "BEGIN:VCARD" "$MERGED_FILE")"
    else
        echo "Error: Failed to merge VCF files or no VCF files found."
    fi
}

# Execute the merge function
merge_vcf_files

echo "Merge complete. You can find the merged file in the current directory."
