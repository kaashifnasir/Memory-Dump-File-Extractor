import argparse
import os
from tqdm import tqdm

# File signatures and limits (max size for file)
file_signatures = {
    "jpg": {
        "header": b'\xFF\xD8',
        "footer": b'\xFF\xD9',
        "max_size": 10 * 1024 * 1024  # 10 MB
    },
    "docx": {
        "header": b'\x50\x4B\x03\x04',
        "footer": b'\x50\x4B\x05\x06',
        "max_size": 50 * 1024 * 1024  # 50 MB
    },
    "png": {
        "header": b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
        "footer": b'\x49\x45\x4E\x44\xAE\x42\x60\x82',
        "max_size": 20 * 1024 * 1024  # 20 MB
    },
}

def extract_files(memdump_file, output_dir, file_types):
    with open(memdump_file, 'rb') as file:
        data = file.read()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_type in file_types:
        sig = file_signatures[file_type]
        header = sig["header"]
        footer = sig["footer"]
        max_size = sig["max_size"]

        pos = 0
        file_count = 0

        print(f"\n[+] Extracting {file_type.upper()} files...")
        while True:
            start = data.find(header, pos)
            if start == -1:
                break  # No more headers found

            end = data.find(footer, start + len(header))
            if end == -1:
                break  # No footer found

            # Calculate size
            size = end + len(footer) - start

            if size <= max_size:
                file_count += 1
                file_path = os.path.join(output_dir, f"{file_type}{file_count}.{file_type}")
                with open(file_path, 'wb') as out_file:
                    out_file.write(data[start:end + len(footer)])
            else:
                # Skip overly large matches (probably false positive)
                pass

            pos = end + len(footer)

        print(f"[+] Found and saved {file_count} {file_type.upper()} files.")

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
