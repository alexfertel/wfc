class WFCProblem:
    def __init__(self, pattern_clasifier, adjacency_validator, pattern_renderer):
        """
        This is an abstract type representing a Wave Function Collapse
        algorithm implementation.

        An subclass of this type should implement `classify_patterns`,
        `valid_adjacency` and `render_pattern`.
        """
        self.pc = pattern_clasifier
        self.av = adjacency_validator
        self.pr = pattern_renderer

    def classify_pattern(self, pattern):
        """
        This method approximates a function which maps a pattern from the example given
        into an identifier.
        """
        raise NotImplementedError

    def valid_adjacency(self, p1, p2):
        """
        This method approximates a function that maps two patterns into an identifier (predicate). 
        """
        raise NotImplementedError

    def render_pattern(self, identifier):
        """
        This method approximates a function that maps an identifier to a pattern.
        """
        raise NotImplementedError
        



