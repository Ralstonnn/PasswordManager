import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import argparse
import getpass

parser = argparse.ArgumentParser(
    description="This programm creates a key to encrypt passwords/message or something else :)")
parser.add_argument('p', type=str, help='Enter your password to create a key')
args = parser.parse_args()
password_provided = args.p
password = password_provided.encode()

'''
To create a salt run this commands in python IDLE: 
    import os 
    os.urandom(16)
'''
# Enter your salt for programm to work
salt = ''

kdf = PBKDF2HMAC(algorithm=hashes.SHA256,
                 length=32,
                 salt=salt,
                 iterations=100_000,
                 backend=default_backend())
key = base64.urlsafe_b64encode(kdf.derive(password))

# Pass a path to directory that encryption-key-file will be saved in, and a name of the file with it's extention
with open(fr'', 'wb') as f:
    f.write(key)
print(key)
