class WFCProblem:
    def __init__(self):
        """
        This is an abstract type representing a Wave Function Collapse
        algorithm implementation.

        An subclass of this type should implement `classify_patterns`,
        `valid_adjacency` and `render_pattern`.
        """
        pass

    def classify_pattern(self, pattern):
        """
        This method approximates a function which maps a pattern from the example given
        into an identifier.
        """
        raise NotImplementedError

    def valid_adjacency(self, id1, id2, **kwargs):
        """
        This method approximates a function that maps two pattern identifiers into a boolean (predicate). 
        """
        raise NotImplementedError

    def render_pattern(self, identifier):
        """
        This method approximates a function that maps an identifier to a pattern.
        """
        raise NotImplementedError
        


