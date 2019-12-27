class Validator:
    def __init__(self):
        """
        This is an abstract type representing a Wave Function Collapse
        adjacency validator.

        Any subclass of this type should implement `valid_adjacencies`.
        """
        pass

    def valid_adjacencies(self, identifier, direction):
        """
        This method approximates a function that maps a pattern identifier
        and a direction to a list of allowed patterns when overlapping in
        the given direction with the pattern identified by `identifier`. 
        """
        raise NotImplementedError
