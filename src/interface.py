import numpy as np

from .classifiers.deterministic import DeterministicClassifier
from .validators.deterministic import DeterministicValidator
from .renderers.deterministic import DeterministicRenderer
from .core import Core


class Interface:
    def __init__(
            self,
            example,
            size,
            classifier=None,
            validator=None,
            renderer=None,
            allow_rotations=False,
            allow_reflections=False):

        # This is the example image.
        self.example = np.array(example)

        # This is the N for the NxN patterns.
        self.size = size

        self.allow_rotations = allow_rotations
        self.allow_reflections = allow_reflections

        # Setup `Classifier` instance.
        self.classifier = classifier if classifier else DeterministicClassifier()

        # Preprocess input image to extract patterns, compute frequency hints
        # and build adjacency rules.
        # Extract patterns without wrapping.
        patterns, weights = self.classify_patterns()
        print("Done setting up classifier.")

        # Setup `Validator` instance.
        self.validator = validator if validator else DeterministicValidator(
            patterns)
        print("Done setting up validator.")

        # Setup `Renderer` instance.
        self.renderer = renderer if renderer else DeterministicRenderer(patterns)
        print("Done setting up renderer.")

        self.core = Core(patterns, weights, self.size)
        
        self.core.classifier = self.classifier
        self.core.validator = self.validator
        self.core.renderer = self.renderer


    def classify_patterns(self):
        patterns = self.extract_patterns()

        return self.classifier.classify_patterns(patterns)


    def extract_patterns(self):
        n, m = self.example.shape
        N = self.size

        submatrices = []
        for i in range(n):
            for j in range(m):
                sm = self.classifier.extract_pattern(self.example, i, j, N)
                submatrices.append(sm)

                # Add rotations. We argue reflections
                # and rotations should not always be allowed.
                for _ in range(3):
                    if self.allow_rotations:
                        sm = np.rot90(sm)
                        submatrices.append(sm)

                    if self.allow_reflections:
                        sm = np.flip(sm)
                        submatrices.append(sm)

        return submatrices

    def generate(self, name, size):

        tex = Texture(os.path.join('images', f'{name}.png'))

        sample = tex.sample

        wfc = Core(sample, N)

        for index, grid in enumerate(wfc.generate(size)):
            print(f'Generated step #{index}.')
            tex.save(grid, os.path.join('results', name, f"{name}{index}.bmp"))

            # pprint(grid, width=200)
