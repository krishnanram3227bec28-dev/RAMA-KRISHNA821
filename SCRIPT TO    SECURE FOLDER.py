import os
import shutil
from cryptography.fernet import Fernet

def generate_and_save_key(key_path="secret.key"):
    """Generates a symmetric encryption key and saves it to a file."""
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"🔒 New key generated and saved to: {key_path}")
    print("⚠️ KEEP THIS KEY SAFE. If you lose it, you cannot decrypt your folder!")

def load_key(key_path="secret.key"):
    """Loads the encryption key from the specified path."""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Key file not found at {key_path}. Cannot proceed.")
    with open(key_path, "rb") as key_file:
        return key_file.read()

def encrypt_folder(folder_path, key_path="secret.key"):
    """Zips a folder and encrypts the zip archive."""
    if not os.path.exists(key_path):
        generate_and_save_key(key_path)
        
    key = load_key(key_path)
    fernet = Fernet(key)
    
    # 1. Compress the folder into a temporary zip file
    print(f"📦 Compressing folder: {folder_path}...")
    zip_output_name = folder_path  # Creates folder_path.zip
    shutil.make_archive(zip_output_name, 'zip', folder_path)
    zip_file_path = f"{zip_output_name}.zip"
    
    # 2. Read the zip data and encrypt it
    with open(zip_file_path, "rb") as file_to_encrypt:
        data = file_to_encrypt.read()
        
    encrypted_data = fernet.encrypt(data)
    
    # 3. Write encrypted data to a new secure file extension (.enc)
    encrypted_output_path = f"{folder_path}.enc"
    with open(encrypted_output_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
        
    # 4. Clean up the plaintext zip file
    os.remove(zip_file_path)
    print(f"🛡️ Folder successfully encrypted into: {encrypted_output_path}")

def decrypt_folder(encrypted_file_path, output_folder_name, key_path="secret.key"):
    """Decrypts an .enc file and extracts it back into a standard folder."""
    key = load_key(key_path)
    fernet = Fernet(key)
    
    # 1. Read and decrypt the data
    print(f"🔓 Decrypting file: {encrypted_file_path}...")
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        
    decrypted_data = fernet.decrypt(encrypted_data)
    
    # 2. Save the decrypted data as a temporary zip file
    temp_zip = "temp_decrypted.zip"
    with open(temp_zip, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
        
    # 3. Extract the zip file back into a folder
    shutil.unpack_archive(temp_zip, output_folder_name, 'zip')
    os.remove(temp_zip)
    print(f"📂 Folder successfully restored to: {output_folder_name}/")

# --- Example Usage ---
if __name__ == "__main__":
    # Define paths (Change these to match your local folders)
    my_folder = "./my_private_data"
    
    # Create a dummy folder for testing if it doesn't exist
    if not os.path.exists(my_folder):
        os.makedirs(my_folder)
        with open(f"{my_folder}/notes.txt", "w") as f:
            f.write("This is a secret portfolio file.")

    # 1. Test Encryption
    encrypt_folder(my_folder)
    
    # 2. Test Decryption (Restores it to a new folder named 'restored_data')
    # decrypt_folder(f"{my_folder}.enc", "./restored_data")
