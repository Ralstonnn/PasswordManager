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


# Enter your salt for programm to work
salt = b'\xea%\xa9\xb2\xef\xe0\xcc\x95\xf5\x83\x02\xf46\xb0\xaf='
kdf = PBKDF2HMAC(algorithm=hashes.SHA256,
                 length=32,
                 salt=salt,
                 iterations=100_000,
                 backend=default_backend())
key = base64.urlsafe_b64encode(kdf.derive(password))


MyPasswordsDir = os.path.join(
    'C:\\', 'Users', f'{getpass.getuser()}', 'AppData', 'Roaming', 'MyPasswords')
if not os.path.exists(MyPasswordsDir):
    os.mkdir(MyPasswordsDir)

with open(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\MyPasswords\Key.key', 'wb') as f:
    f.write(key)
print(key)
