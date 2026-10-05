# 🛡️ Local Folder Encryption Script (AES-128 / Fernet)

A Python-based automation script designed to secure sensitive directories on a local PC. The script zips a target folder, encrypts it using strong symmetric cryptography, and handles seamless decryption using a securely managed local key.

## 🚀 Features
- **Symmetric Encryption:** Built on top of the robust `cryptography.fernet` module (AES-128).
- **Automated Compression:** Zips entire directories before encryption to maintain file structures cleanly.
- **Production-Ready Formatting:** Modular code architecture with integrated error handling for path validation.

## 🛠️ Prerequisites & Setup
Make sure you have Python installed on your machine. Install the required dependencies using pip:

```bash
pip install cryptography
```

## 💻 How to Use

### 1. Encrypting a Folder
Run the script to automatically compress and encrypt your targeted folder into a protected `.enc` file:
```python
encrypt_folder("./your_sensitive_folder")
```
*Note: This will generate a local `secret.key` file. Keep this file safe!*

### 2. Decrypting a Folder
To unpack your data back into its original form:
```python
decrypt_folder("./your_sensitive_folder.enc", "./restored_folder")
```

## 🔒 Security Disclaimer
The `secret.key` file generated during the process holds the master access to your data. This repository includes a `.gitignore` configuration ensuring your keys and encrypted outputs are never leaked to public version control systems.
