import numpy as np

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from .renderer import Renderer


class MonsterRenderer(Renderer):
    def __init__(self, patterns):
        super().__init__()
        
        self.patterns = patterns

        # Fit the model
        self.clf = self.setup()

        # Feature vectors
        self.train = []

    def setup(self):
        X = [p.flatten() for p in self.patterns]
        y = [vector[0] for vector in train]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

        clf = GaussianNB()
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)

        print(score)

        return clf

    def render_patterns(self, identifiers):
        return list(map(self.render_pattern, identifiers))

    def render_pattern(self, identifier):
        return self.patterns[identifier]

