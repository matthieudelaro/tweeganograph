# This file describes the main user interface to encode/decode.
# It has been designed for Python 3.5. Please upgrade if you
# are using Python 2.X version.

import sys
from Cipher import Cipher
import Database
import getopt


def usage():
    out = ("USAGE:\n"
        "Tweeganograph hides data into tweets. Call it with "
        "two parameters to encode: the plaintext first, and then the password.\n"
        "For example: python3.5 Tweeganograph.py \"Your majesty the queen.\" \"awesome password\"")
    print(out)


def main(argv):
    plaintext = None
    password = None
    topic = "topic"
    ciphertext = None
    userTriedAction = False
    # helper : http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
    # try:
    #     opts, args = getopt.getopt(argv, "hg:d", ["help", "p=", "c=", "k="])
    # except getopt.GetoptError:
    #     usage()
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt in ("-h", "--help"):
    #         usage()
    #         sys.exit()
    #     elif opt in ("-p", "--plaintext"):
    #         plaintext = arg
    #         userTriedAction = True
    #     elif opt in ("-c", "--ciphertext"):
    #         ciphertext = arg
    #         userTriedAction = True
    #     elif opt in ("-k", "--key"):
    #         password = arg
    #         userTriedAction = True

    # print("args: ", plaintext, key, ciphertext)
    try:
        plaintext = argv[0]
        password = argv[1]
    except:
        if len(argv) == 0:
            usage()
            print("\nNo argument provided. Entering development mode.")
            dev(argv)
        else:
            print("Invalide arguments.")
            usage()
            sys.exit(2)

    try:
        topic = argv[3]
    except:
        pass

    if plaintext != None and password != None:
        db = Database.TweetDatabase()
        cipher = Cipher()
        spam,key = cipher.encode(plaintext, password, "topic", db)

        print("Here is your spam:")
        print(spam)

        print("Checking decoding process: here is the message hidden in the spam:")
        print(cipher.decode(spam,key))
    else:
        usage()


def dev(argv):
    db = Database.TweetDatabase()
    cipher = Cipher()
    print()
    print()
    spam,key = cipher.encode("Your majesty the quee", "awesome password", "topic", db)
    print("Here is your spam:")
    print(spam)

    print(cipher.decode(spam,key))

if __name__ == "__main__":
    main(sys.argv[1:])
    # dev(sys.argv[1:])
