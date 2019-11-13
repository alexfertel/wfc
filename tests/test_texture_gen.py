import numpy as np

from src.texture_gen import TextureGeneration
from src.utils.matrices import directions

def test_pattern_extraction():
    """
    Tests if the correct patterns are extracted from the example input
    """
    example = np.arange(9).reshape(3, 3)

    tg = TextureGeneration(example)

    # Test size 0 should be empty list
    assert tg.extract_patterns(0) == [], f'Test #1: Failed.'

    # Test size 1 should be each element of the matrix
    result = tg.extract_patterns(1)
    should = [np.array([[i]]) for i in range(len(example.flatten()))]
    assert result == should, f'Test #2: Failed. Result: {result}, should be: {should}' 


def test_build_propagator():
    """
    Tests if the index data-structure built is correct
    """

    example = np.arange(30).reshape(5, 6)

    tg = TextureGeneration(example)

    patterns = tg.extract_patterns(3)
    
    tg.classify_patterns(patterns)

    # Propagator should be an empty dict when matrix is a range.
    result = tg.learn_adjacencies(patterns)
    should = {}
    assert result == should, f'Test #1: Failed. Result: {result}, should be: {should}'


    example = np.ones(4)

    tg = TextureGeneration(example)

    patterns = tg.extract_patterns(1)

    tg.classify_patterns(patterns)

    # Propagator should allow everything when all patterns are equal.
    result = tg.learn_adjacencies(patterns)
    matches = [i for i in range(4)]
    should = {(iden, d): matches for iden in matches for d in directions}
    print(result)
    print(should)
    assert result == should, f'Test #1: Failed. Result: {result}, should be: {should}'
