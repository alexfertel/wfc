import numpy as np

from .classifiers.deterministic import DeterministicClassifier
from .validators.deterministic import DeterministicValidator
from .renderers.deterministic import DeterministicRenderer
from .core import Core
from .utils import extract_submatrices, extract_wrapped_pattern

from pprint import pprint


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

        # Adds a useful identifier matrix for ML purposes
        self.init_id_matrix(patterns)
        pprint(self.id_matrix)
        print("Done setting up id_matrix.")

        # Setup `Validator` instance.
        self.validator = validator(patterns) if validator else DeterministicValidator(
            patterns)
        print("Done setting up validator.")

        # Setup `Renderer` instance.
        self.renderer = renderer(
            self.id_matrix, self.size) if renderer else DeterministicRenderer(patterns)
        print("Done setting up renderer.")

        self.core = Core(patterns, weights, self.size)

        self.core.validator = self.validator

    def classify_patterns(self):
        patterns = extract_submatrices(
            self.example, self.size, extract_wrapped_pattern)

        if self.allow_rotations or self.allow_reflections:
            for pattern in patterns:
                sm = None
                for _ in range(3):
                    if self.allow_rotations:
                        sm = np.rot90(pattern)
                        patterns.append(sm)

                    if self.allow_reflections:
                        sm = np.flip(sm)
                        patterns.append(sm)

        return self.classifier.classify_patterns(patterns)

    def init_id_matrix(self, patterns):
        n, m = self.example.shape
        print(f'init_id_matrix: {self.example.shape}')

        self.id_matrix = [[-1 for _ in range(m)] for _ in range(n)]

        pos = 0
        for i in range(n):
            for j in range(m):
                sm = extract_wrapped_pattern(self.example, i, j, self.size)

                for p in patterns:
                    if np.equal(p.matrix, sm).all():
                        self.id_matrix[i][j] = p.index
                        break

    def generate(self, name, size, quiet):
        if quiet:
            for _ in enumerate(wfc.generate(size)):
                continue
        else:
            for index, grid in enumerate(self.core.generate(size)):
                print(f'Generated step #{index}.')

        self.save(self.core.grid, os.path.join(
            'results', 'matrices', name, f"{name}.txt"))

        return self.core.grid

    def save(self, grid, path):
        with open(path, 'w') as fd:
            pprint(grid, width=200, stream=fd)

    def render(self, name):
        print('Start rendering phase.')
        print(f'render:example: {self.example.shape}')
        n, m = len(self.core.grid), len(self.core.grid[0])
        print(f'render:grid: ({n}, {m})')
        # patterns = self.extract_patterns(self.core.grid)
        identifiers = [[-1 for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                identifiers[i][j] = self.core.grid[i][j].identifier

        return self.renderer.render_patterns(np.array(identifiers))
