import numpy as np

from src.texture_gen import TextureGeneration


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