import argparse
import os
import re
import binascii
from tqdm import tqdm

# Define file signatures and corresponding file extensions
file_signatures = {
    "jpg": (b'\x00\xFF\xD8', b'\xFF\xD9'),
    "docx": (b'\x00\x50\x4B\x03\x04', b'\x50\x4B\x05\x06'),
    "png": (b'\x00\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x49\x45\x4E\x44\xAE\x42\x60\x82'),
    # Add more file signatures here as needed
}

def extract_files(memdump_file, output_dir, file_types):
    with open(memdump_file, 'rb') as file:
        data = file.read()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_type in file_types:
        header, footer = file_signatures[file_type]
        pattern = re.compile(re.escape(header) + b'(.*?)' + re.escape(footer), re.DOTALL)
        matches = pattern.findall(data)
        
        for i, match in tqdm(enumerate(matches), desc=f"Extracting {file_type.upper()} files", unit="file"):
            file_name = f"{file_type}{i + 1}.{file_type}"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'wb') as output_file:
                output_file.write(header + match + footer)

def main():
    parser = argparse.ArgumentParser(description='Extract files from memory dump.')
    parser.add_argument('memdump_file', type=str, help='Path to the memory dump file')
    parser.add_argument('-types', nargs='+', choices=file_signatures.keys(), required=True, 
                        help='File types to extract (e.g., -types jpg png)')
    parser.add_argument('-dir', dest='output_dir', type=str, help='Output directory for extracted files')

    args = parser.parse_args()

    extract_files(args.memdump_file, args.output_dir, args.types)

if __name__ == "__main__":
    main()
