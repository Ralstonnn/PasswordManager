# A Python3 Program to generate OTP (One Time Password)
from cryptography.fernet import Fernet
import argparse
import getpass
import random
import sys
import os


MyPasswordsDir = os.path.join(
    'C:\\', 'Users', f'{getpass.getuser()}', 'AppData', 'Roaming', 'MyPasswords')
if not os.path.exists(MyPasswordsDir):
    print('You need to run "KeyForPasswordDecryption.py" first')
    sys.exit()


PasswordForUser = os.path.join('D:\\', 'MyPasswords')
if not os.path.exists(PasswordForUser):
    os.mkdir(PasswordForUser)


# Encryption key
# Pass a path to directory that encryption-key-file is saved in, and a name of the file with it's extention
with open(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\MyPasswords\Key.key', 'rb') as f:
    key = f.read()

fer = Fernet(key)

# Console arguments parser
parser = argparse.ArgumentParser(
    description="This program helps you to create\
            safe password that's cyphered and saved in the\
                log file")
parser.add_argument('-cp', '--createpassword',
                    help='If you want to create password just use this function',
                    action='store_true', default=False)
parser.add_argument('-wpf', '--whatpasswordfor',  type=str,
                    help='This function automatic writes what password will be use for. Need a string',
                    default='')
parser.add_argument('-dp', '--decypherpassword',
                    help='If you want to decypher password just use this function. \
                        Dont forget to pass a password as a string',
                    type=str, default='')
parser.add_argument('-gb', '--googlebackup', action='store_true',
                    help='If you want to backup file to Google Drive call this function',
                    default=False)

args = parser.parse_args()


# Pass a path to directory that log-file should be saved in, and a name of the file with it's extention
log_file_directory = fr'C:\Users\{getpass.getuser()}\AppData\Roaming\MyPasswords\MyPasswords.txt'

# Pass a path to directory that file with passwords should be saved in, and a name of the file with it's extention
file_for_user = fr'D:\MyPasswords\Passwords.txt'

OTPSet = set()


# Adding password file to chosen diresctory, if there is one then reading data from it
if os.path.isfile(log_file_directory):
    with open(log_file_directory, 'rb') as f:
        OTPSet.add(f.read().strip())


# Clearing log file before adding new password
def ClearLogFile():
    if os.path.isfile(log_file_directory):
        with open(log_file_directory, 'r+') as f:
            f.truncate(0)
            f.close()


# A Function to generate a unique OTP everytime
def generateOTP(length):

    # All possible characters of my OTP
    str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    n = len(str)

    # String to hold my OTP
    OTP = ""

    for i in range(length):
        OTP += str[random.randint(0, n-1)]

    # String to check if the same OTP was generated before
    # And if it was then generate new one
    if(bytes(OTP, 'utf-8') not in OTPSet):
        return (OTP)

    return(generateOTP(length))


def CreateNewPassword(passwordFor=''):
    ClearLogFile()

    length = 18
    newOTP = generateOTP(length)
    newOTPEncrypted = fer.encrypt(bytes(newOTP, 'utf-8'))

    # Adding new encrypted password to log file
    OTPSet.add(newOTPEncrypted)
    with open(log_file_directory, 'wb') as f:
        for item in OTPSet:
            f.write(item + b'\n')

    # Creating new file with encrypted passwords and adding it in passed user folder
    with open(file_for_user, 'a+') as f:
        if passwordFor != '':
            passwordFor = f' (Password for {passwordFor})'
        f.write(str(newOTPEncrypted)[2:-1] + (passwordFor) + '\n')

    return(str(newOTP))


# Method that helps you decypher given password
def Decypher(passwordToD):
    passwordToD = bytes(passwordToD, 'utf-8')
    passwords = fer.decrypt(passwordToD).decode()

    return passwords


def Main():

    if args.createpassword:
        print(CreateNewPassword(args.whatpasswordfor))

    if args.decypherpassword != '':
        print(f'\nDecyphered password: {Decypher(args.decypherpassword)}\n')

    if args.googlebackup:
        from GDriveBackup.GDriveBackup import google_drive_upload_file
        """
        In order for google backup to work you need to pass a path to folder with
        credential and token to "FOLDER_WITH_TOKEN_AND_CREDENTIAL" variable, if you 
        dont have a token it will be generated automaticly.

        Also you need to pass a path to file with passwords to "google_drive_upload_file" method
        """
        google_drive_upload_file(r'D:\MyPasswords\Passwords.txt')


# Methon that's called if code was run directly
if __name__ == '__main__':
    Main()
