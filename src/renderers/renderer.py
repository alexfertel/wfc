class Renderer:
    def __init__(self):
        """
        This is an abstract type representing a Wave Function Collapse
        pattern renderer.

        Any subclass of this type should implement `render_pattern`.
        """
        pass

    def render_patterns(self, patterns):
        """
        This method will be called inside the algorithm `core` file
        as a wrapper for `render_pattern`.
        
        It should be the equivalent of calling `render_pattern` once
        for each slot on the output.
        """
        pass        

    def render_pattern(self, pattern):
        """
        This method approximates a function which maps an identifier into an output.
        """
        raise NotImplementedError