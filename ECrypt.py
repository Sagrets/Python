from cryptography.fernet import Fernet

filepath = input("Please enter the full filepath to your encryption key: ")
target_file = input('Please enter the full path to the file you wish to target: ')
choice = input('Would you like to encrypt the target file or decrypt? Enter decrypt or encrypt:')

with open(filepath, 'rb') as filekey:
        key = filekey.read()

fernet = Fernet(key)

def file_encrypt():
    with open(target_file, 'rb') as target:
        original = target.read()

    encrypted = fernet.encrypt(original)

    with open(target_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def file_decrypt():
    with open(target_file, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)

    with open(target_file, 'wb') as new_file:
        new_file.write(decrypted)

if choice.lower() == 'encrypt':
    file_encrypt()
elif choice.lower() == 'decrypt':
    file_decrypt()
else:
    print('Invalid choice.')