# Safe Password Manager

This console program is created to help you with your passwords. It can help you create a password encrypt it and the decrypt when needed.

There are 2 main scripts:

    		  1) KeyForPasswordDecryption.py is used to create a key for encryption. To do so you should pass a password that will be a key
    		     to get the same encryption code.

    		  2) "PasswordsManager.py" is has several functions:
    		  	a) -cp - this function generates password and creates 2 files.
    		  	   One is stored in "User\Appdata\Roaming\MyPasswords\Passwords.txt" it stores all generated passwords and check that they
    		  	   dont repeat each other. Second file is stored in GoogleDrive foler and contains all encrypted passwords.
    		  	b) -wpf - is shortage of "what password for" and if this argument(it's single string) is passed then it writes
    		  	   next to a password string that explains what it's for.
    		  	c) -dp - this function decrypt given password it has one argument in which you need to pas encrypted version of your
    		  	   password(it should be passed as a string) and then it'll print decrypted password.
