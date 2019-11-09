#!/usr/bin/python3

import sys
from tests.test_texture_gen import test_pattern_extraction

def main():
    print("Hi!!!")

def tests():
    test_pattern_extraction()

if __name__ == "__main__":
    if "--debug" in sys.argv:
        tests() 
        exit()

    main()

