import os


def remove_image_fields_from_vcard(vcard_content):
    lines = vcard_content.split('\n')
    cleaned_lines = []
    skip_photo = False

    for line in lines:
        if line.startswith('PHOTO'):
            skip_photo = True
            continue

        if skip_photo:
            if not line.startswith(' '):
                skip_photo = False
            else:
                continue

        if line.startswith('X-IMAGE'):
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def process_vcard_files(directory):
    processed_dir = os.path.join(directory, 'processed')

    # Create the 'processed' directory if it doesn't exist
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    for filename in os.listdir(directory):
        if filename.endswith('.vcf'):
            input_file_path = os.path.join(directory, filename)
            output_file_path = os.path.join(processed_dir, filename)

            with open(input_file_path, 'r', encoding='utf-8') as file:
                vcard_content = file.read()

            modified_vcard = remove_image_fields_from_vcard(vcard_content)

            # Save the modified vCard in the 'processed' directory
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(modified_vcard)

            print(f"Processed: {filename}")


if __name__ == "__main__":
    directory = '.'  # Replace with the directory containing your vCard files
    process_vcard_files(directory)
