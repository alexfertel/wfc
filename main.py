#!/usr/bin/python3

import sys
# from tests.test_texture_gen import test_pattern_extraction, test_build_propagator
from src.wfc import WFC
from src.core import Core
from src.graphics import Texture
from pprint import pprint

def main():

    # This is the example used in the paper:
    # "WaveFunctionCollapse is Constraint Solving in the Wild"
    # called "Red Maze".
    # red_maze = [
    #     [0, 0, 0, 0, 0],
    #     [0, 1, 1, 1, 0],
    #     [0, 1, 2, 1, 0],
    #     [0, 1, 1, 1, 0],
    #     [0, 0, 0, 0, 0]
    #     ]
    # red_maze = [
    #     [0, 0, 0, 0],
    #     [0, 1, 1, 1],
    #     [0, 1, 2, 1],
    #     [0, 1, 1, 1],
    #     ]


    wfc = WFC(allow_rotations=True)

    tex = Texture("Rooms")

    sample = tex.sample
    wfc.preprocess(sample, 3)
    # pprint(wfc.frequency_hints)


    wfc.run((56, 56), 50)
    # wfc.run((200, 200), 50)
    
    # for row in wfc.history[-1]:
    #     print(row)

    # with open("tests/test.txt", 'w') as fd:
    #     for item in wfc.history:
    #         for row in item:
    #             fd.write(str(row))
    #             fd.write("\n")
    #         fd.write("\n")

    for index, item in enumerate(wfc.history):
        tex.save(item, f"Rooms{index}")

    # tex.save(wfc.history[-1], "test")



    # print(grid)
    
    # for _ in range(50):
    #     grid = wfc.run((15, 15))

    #     for i in range(15):
    #         for j in range(15):
    #             if grid[i][j] == 2:
    #                 print("Found one!")
    #                 pprint(grid)
    #                 break


    # for item in wfc.patterns:
    #    pprint(item.matrix) 


def samples(name):
    tex = Texture(name)

def tests():
    test_pattern_extraction()
    test_build_propagator()

def core():
    tex = Texture("Rooms")

    sample = tex.sample

    wfc = Core(sample, 3)

    for grid in wfc.generate((28, 28)):
        pass
        # print(grid)

if __name__ == "__main__":
    if "--debug" in sys.argv:
        tests() 
        exit()
    if "--sample" in sys.argv:
        samples(sys.argv[2]) 
        exit()

    # main()
    core()

