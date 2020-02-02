import numpy as np

from .renderer import Renderer


class DeterministicRenderer(Renderer):
    def __init__(self, patterns):
        super().__init__()
        
        self.patterns = patterns

    def render_patterns(self, identifiers):
        return list(map(self.render_pattern, identifiers))

    def render_pattern(self, identifier):
        return self.patterns[identifier]