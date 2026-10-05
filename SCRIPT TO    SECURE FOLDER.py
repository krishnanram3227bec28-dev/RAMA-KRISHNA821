import os
import shutil
import boto3  # AWS SDK for Python
from botocore.exceptions import NoCredentialsError
from cryptography.fernet import Fernet

# --- AWS CONFIGURATION ---
# Replace these with your own configuration or set them as environment variables
AWS_BUCKET_NAME = "your-secure-cloud-backup-bucket" 

def generate_and_save_key(key_path="secret.key"):
    """Generates a symmetric encryption key and saves it locally."""
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"🔒 New key generated and saved to: {key_path}")

def load_key(key_path="secret.key"):
    """Loads the encryption key from the specified path."""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Key file not found at {key_path}.")
    with open(key_path, "rb") as key_file:
        return key_file.read()

def upload_to_s3(local_file, bucket, s3_file):
    """Uploads the encrypted file directly to an AWS S3 Bucket."""
    s3 = boto3.client('s3')
    try:
        print(f"☁️ Uploading {local_file} to AWS S3 bucket '{bucket}'...")
        s3.upload_file(local_file, bucket, s3_file)
        print("🚀 Upload Successful! Your backup is secure in the cloud.")
        return True
    except FileNotFoundError:
        print("❌ The local file was not found.")
        return False
    except NoCredentialsError:
        print("❌ AWS Credentials not found. Please configure 'aws configure' in your local CLI.")
        return False

def encrypt_and_backup_folder(folder_path, key_path="secret.key"):
    """Zips a folder, encrypts the zip archive, and uploads it to AWS S3."""
    if not os.path.exists(key_path):
        generate_and_save_key(key_path)
        
    key = load_key(key_path)
    fernet = Fernet(key)
    
    # 1. Compress the folder into a temporary zip file
    print(f"📦 Compressing folder: {folder_path}...")
    shutil.make_archive(folder_path, 'zip', folder_path)
    zip_file_path = f"{folder_path}.zip"
    
    # 2. Read the zip data and encrypt it
    with open(zip_file_path, "rb") as file_to_encrypt:
        data = file_to_encrypt.read()
    encrypted_data = fernet.encrypt(data)
    
    # 3. Write encrypted data to an .enc file
    encrypted_output_path = f"{folder_path}.enc"
    with open(encrypted_output_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
        
    # Clean up the plaintext zip file
    os.remove(zip_file_path)
    print(f"🛡️ Folder successfully encrypted locally: {encrypted_output_path}")

    # 4. AUTOMATED CLOUD BACKUP
    # Uploads the encrypted file to S3 using just the file name
    s3_filename = os.path.basename(encrypted_output_path)
    upload_to_s3(encrypted_output_path, AWS_BUCKET_NAME, s3_filename)

if __name__ == "__main__":
    # Example Target Directory
    target_dir = "./my_private_data"
    
    # Run the automated local encryption + cloud backup pipeline
    encrypt_and_backup_folder(target_dir)
