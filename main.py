#!/usr/bin/python3

import sys
from tests.test_texture_gen import test_pattern_extraction, test_build_propagator

def main():
    print("Hi!!!")

def tests():
    test_pattern_extraction()
    test_build_propagator()

if __name__ == "__main__":
    if "--debug" in sys.argv:
        tests() 
        exit()

    main()

