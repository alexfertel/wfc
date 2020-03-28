class Validator:
    def __init__(self, alpha=.0):
        """
        This is an abstract type representing a Wave Function Collapse
        adjacency validator.

        Any subclass of this type should implement:
        - `valid`
        - `learn`
        - `prune`
        """
        pass

    def valid(self, identifier, direction):
        """
        This method approximates a function that maps a pattern identifier
        and a direction to a list of allowed patterns when overlapping in
        the given direction with the pattern identified by `identifier`. 
        """
        raise NotImplementedError

    def learn(self, patterns):
        """
        This method exposes a hook to be able to update the validator
        object with new patterns. 
        """
        raise NotImplementedError

    def prune(self, patterns):
        """
        This method exposes a hook that prunes the validator
        object patterns. Here, 'to prune' means that the patterns
        provided are marked as negative, which results in the following:
        Every overlapping adjacency found between these patterns will be
        disallowed by the validator object.
        """
        raise NotImplementedError

    def postprocess(self, patterns):
        """
        Hook to make any post-processing after the build phase.
        """
        pass
