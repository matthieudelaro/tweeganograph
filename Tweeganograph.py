# This file describs the main user interface to encode/decode.
# It has been designed for Python 3.5. Please upgrade if you
# are using Python 2.X version.

import sys
from Cipher import Cipher
import Database


def usage():
    # todo
    print("""Tweeganograph hide data into tweets. Call it with
        ... parameters to encode, and with ... to decode.
        This is a placeholder => usage() function has to be implemented.""")


def main(argv):
    # helper : http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
    usage()
    db = Database.MockDatabase()
    cipher = Cipher()
    print()
    print()
    spam = cipher.encode("your plaintext", "awesome password", "topic", db)
    print("Here is your spam:")
    print(spam)

if __name__ == "__main__":
    main(sys.argv[1:])
