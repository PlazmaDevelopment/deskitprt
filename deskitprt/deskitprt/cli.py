import os
import sys
import argparse
from pathlib import Path
from .crypto import encrypt_file, decrypt_file

def process_directory(directory: str, password: str, mode: str = 'encrypt'):
    """Process all files in the given directory"""
    processed_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if mode == 'encrypt' and not file.endswith('.encrypted'):
                    encrypted_path = encrypt_file(file_path, password)
                    processed_files.append(encrypted_path)
                    print(f"Encrypted: {file_path}")
                elif mode == 'decrypt' and file.endswith('.encrypted'):
                    decrypted_path = decrypt_file(file_path, password)
                    if decrypted_path:
                        processed_files.append(decrypted_path)
                        print(f"Decrypted: {decrypted_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    return processed_files

def main():
    # Legacy support for -prt flag
    if len(sys.argv) > 1 and sys.argv[1] == '-prt':
        if len(sys.argv) < 4:
            print("Usage: deskit -prt <encrypt|decrypt> <password> [directory]")
            return
        
        mode = sys.argv[2].lower()
        password = sys.argv[3]
        directory = sys.argv[4] if len(sys.argv) > 4 else '.'
        
        if mode not in ['encrypt', 'decrypt']:
            print("Error: Mode must be 'encrypt' or 'decrypt'")
            return
            
        processed = process_directory(directory, password, mode)
        print(f"\n{'Encryption' if mode == 'encrypt' else 'Decryption'} complete. {len(processed)} files processed.")
        return
    
    # Normal argument parsing
    parser = argparse.ArgumentParser(description='Encrypt/decrypt files with a password')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt files')
    encrypt_parser.add_argument('password', help='Password for encryption')
    encrypt_parser.add_argument('-d', '--directory', default='.', help='Directory to encrypt')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt files')
    decrypt_parser.add_argument('password', help='Password for decryption')
    decrypt_parser.add_argument('-d', '--directory', default='.', help='Directory to decrypt')
    
    args = parser.parse_args()
    
    if not hasattr(args, 'password'):
        parser.print_help()
        return
    
    if args.command == 'encrypt':
        print(f"Encrypting files in {args.directory}...")
        processed = process_directory(args.directory, args.password, 'encrypt')
        print(f"\nEncryption complete. {len(processed)} files processed.")
    elif args.command == 'decrypt':
        print(f"Decrypting files in {args.directory}...")
        processed = process_directory(args.directory, args.password, 'decrypt')
        print(f"\nDecryption complete. {len(processed)} files processed.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
