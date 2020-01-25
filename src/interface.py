from .classifiers.deterministic import DeterministicClassifier
from .validators.deterministic import DeterministicValidator
from .renderers.deterministic import DeterministicRenderer


class Interface:
    def __init__(
            self, 
            example, 
            size, 
            classifier=None,
            validator=None,
            renderer=None):
            
        self.example = np.array(example)
        self.size = size

        self.classifier = classifier if classifier else DeterministicClassifier()
        self.validator = validator if validator else DeterministicValidator(self.patterns)
        self.renderer = renderer if renderer else DeterministicRenderer()





