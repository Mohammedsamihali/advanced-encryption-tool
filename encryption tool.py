import os
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Function to generate a 32-byte AES key
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()  # Derive a 32-byte key

# Function to encrypt a file
def encrypt_file(file_path, key):
    chunk_size = 64 * 1024
    output_file = file_path + ".enc"
    iv = get_random_bytes(16)  # Generate a random IV

    cipher = AES.new(key, AES.MODE_CBC, iv)

    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as infile, open(output_file, "wb") as outfile:
        outfile.write(file_size.to_bytes(8, 'big'))  # Store original file size
        outfile.write(iv)  # Store IV

        while chunk := infile.read(chunk_size):
            if len(chunk) % 16 != 0:  # Apply padding if needed
                chunk += b' ' * (16 - len(chunk) % 16)
            outfile.write(cipher.encrypt(chunk))

    print(f"Encryption completed: {output_file}")

# Function to decrypt a file
def decrypt_file(file_path, key):
    chunk_size = 64 * 1024
    output_file = file_path.replace(".enc", ".dec")

    with open(file_path, "rb") as infile:
        file_size = int.from_bytes(infile.read(8), 'big')  # Read original file size
        iv = infile.read(16)  # Read IV

        cipher = AES.new(key, AES.MODE_CBC, iv)

        with open(output_file, "wb") as outfile:
            while chunk := infile.read(chunk_size):
                decrypted_chunk = cipher.decrypt(chunk)
                outfile.write(decrypted_chunk)

            outfile.truncate(file_size)  # Remove padding

    print(f"Decryption completed: {output_file}")

# Example Usage
if __name__ == "__main__":
    print("AES-256 File Encryption Tool")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt a file? ").lower()

    file_path = input("Enter the file path: ")
    password = input("Enter a password: ")
    key = generate_key(password)  # Convert password to AES-256 key

    if choice == 'e':
        encrypt_file(file_path, key)
    elif choice == 'd':
        decrypt_file(file_path, key)
    else:
        print("Invalid choice!")
