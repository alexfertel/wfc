class Classifier:
    def __init__(self):
        """
        This is an abstract type representing a Wave Function Collapse
        pattern classifier.

        Any subclass of this type should implement `classify_pattern`.
        """
        pass

    def classify_patterns(self, patterns):
        """
        This method will be called inside the algorithm `core` file
        as a wrapper for `classify_pattern`.
        
        It should be the equivalent of calling `classify_pattern` once
        for each pattern.

        It should return the classified patterns and their weights.
        """
        pass        

    def classify_pattern(self, pattern):
        """
        This method approximates a function which maps a pattern from the example given
        into an identifier.
        """
        raise NotImplementedError