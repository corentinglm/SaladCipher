import os
import enchant

class Cipher:

    """
    Class used for encrypting and decrypting messages using a key.
    Supports numbers and letters\n
    Encryption method used: Caesar Cipher\n
    Function auto copies the encrypted/decrypted message to the clipboard\n

    Create a cipher object by calling the class
    >>> cipher = Cipher()

    Ask the user input using the 'userMessage' and 'userKey' functions
    >>> msg = cipher.userMessage()
    >>> key = cipher.userKey()

    Encrypt a message using the 'encrypt' function
    >>> cipher.encrypt(3, "charline1337")

    Decrypt a message using the 'decrypt' function
    >>> cipher.decrypt(3, "FKDUOLQH4660")

    Auto decrypt a message and get the key used in the encryption by using the 'auto_decrypt' function
    >>> cipher.auto_decrypt("FKDUOLQH4660")
    """

    # Initializing class
    def __init__(self):
        """
        Initializing the class, creating the alphabet and numbers used for encryption/decryption
        >>> alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Alphabet
        >>> numbers = "0123456789" # Numbers
        """
        self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.numbers = "0123456789"

        self.d = enchant.Dict("en_US")

    def split_message(self, message):
        """
        Splits a message into a list of words
        """
        return message.split(" ")

    def consistency(self, message):
        """
        Checks if a word is consistent with the english language\n
        """

        consistent_words = 0

        for word in self.split_message(message):
            if self.d.check(word) == True:
                consistent_words += 1

        return consistent_words

    def reliability(self, percentage):
        """
        Returns the reliability of a decryption
        """
        if percentage >= 80:
            return "Very reliable"

        elif percentage >= 60:
            return "Reliable"

        elif percentage >= 40:
            return "Unreliable"

        elif percentage >= 20:
            return "Very unreliable"

        else:
            return "Not reliable at all, try with another margin, or maybe the text cannot be decrypted"

    def auto_decrypt(self, message, require=1):
        """
        Automatically decrypts a message, using the consistency function ( Brute Force )
        Takes one arguments: message \n

        Margin is the amount of consistent words needed to be considered a correct decryption, the function requires a perfect decryption, but if the decryption is not perfect, it will try with a lower margin ( require + 0.10 ) until it reaches 4, then it will return False, meaning you cannot decrypt the message with the current margin\n
        """

        # Prevents errors from enchant library
        message = message.strip()

        margin = len(self.split_message(message)) / require
        print(f"WORKING: Testing with {round(margin)} consistent words needed\n")

        for i in range(0, 26):
            decrypted = self.__quick_decrypt(i, message).lower()

            if self.consistency(decrypted) >= margin:
                percentage = round(
                    self.consistency(decrypted) / len(self.split_message(message)) * 100
                )
                print(f"Auto decrypted to:\n\n'{decrypted}'\n\nKey: '{i}'\n")
                print(f"Consistent words found: {self.consistency(decrypted)}")
                print(f"Reliability: {percentage}% ({self.reliability(percentage)})")

                return decrypted

        # If no decryption is found, try with a lower requirement ( margin )
        if require < 4:
            self.auto_decrypt(message, require + 0.10)
        else:
            print("No decryption found")
            return False

    def __quick_decrypt(self, key, message):
        """
        Quick decrypt function, used for the auto_decrypt function
        """
        message = message.upper()
        res = ""

        for letter in message:
            if letter in self.alpha and letter.isdigit() == False:
                res += self.alpha[(self.alpha.index(letter) - key) % 26]

            elif letter in self.numbers:
                res += self.numbers[(self.numbers.index(letter) - key) % 10]

            else:
                res += letter
        # Return
        return res

    def userMessage(self):
        """
        Asks the user for a message, then returns the message in a string
        """

        print("Type a text to decrypt/encrypt...\n")
        text = input("Type in : \n")

        # Returns Message
        return str(text)

    def userKey(self):
        """
        Asks for the user for a key, then returns the key in an integer.
        If the input is not a number, it will return the default key (3)
        """
        print("Specify key...\n")
        key = input("Key: \n")

        if key.isdigit() == False:
            print("ERROR: Key must be a number\nUsing default key... (3)")
            return 3

        else:
            # Returns Key
            return int(key)

    def __clipboard(self, text):
        command = "echo " + text.strip() + "| clip"
        os.system(command)

        # Recap
        print(f'"{text}" copied to clipboard')

        return

    # Encryption Function
    def encrypt(self, key, message):
        """
        Encrypts a message. Takes two arguments: key and message.

        >>> cipher.encrypt(3,"charline1337")
        "FKDUOLQH4660"

        """
        message = message.upper()
        res = ""

        for letter in message:
            if letter in self.alpha and letter.isdigit() == False:
                res += self.alpha[(self.alpha.index(letter) + key) % 26]

            elif letter in self.numbers:
                res += self.numbers[(self.numbers.index(letter) + key) % 10]

            else:
                res += letter

        # Recap
        print(f'"{message}" encrypted to "{res}" with the key "{key}"')

        # Copy to clipboard
        self.__clipboard(res)

        # Return
        return res

    # Decryption Function
    def decrypt(self, key, message):
        """
        Decrypts a message. Takes two arguments: key and message.

        >>> cipher.decrypt(3,"FKDUOLQH4660")
        "CHARLINE1337"
        """
        message = message.upper()
        res = ""

        for letter in message:
            if letter in self.alpha and letter.isdigit() == False:
                res += self.alpha[(self.alpha.index(letter) - key) % 26]

            elif letter in self.numbers:
                res += self.numbers[(self.numbers.index(letter) - key) % 10]

            else:
                res += letter

        # Recap
        print(f'"{message}" decrypted to "{res}" with the key "{key}"')

        # Copy to clipboard
        self.__clipboard(res)

        # Return
        return res
