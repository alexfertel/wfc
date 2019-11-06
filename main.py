#!/usr/bin/python3

import sys
from tests.ac3_tests import csp_lib_test

def main():
    print("Hi!!!")

def tests():
        # map_coloring_test()
        csp_lib_test()

if __name__ == "__main__":
    if "--debug" in sys.argv:
        tests() 
        exit()

    main()

