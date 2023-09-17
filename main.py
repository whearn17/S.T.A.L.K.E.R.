import sys
from mftshell import MFTShell

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: main.py <path_to_mft_csv_file>")
        sys.exit(1)

    shell = MFTShell(sys.argv[1])
    shell.cmdloop("Welcome to the MFT interactive shell. Type 'help' for a list of commands.")
