import numpy as np

# from sklearn.naive_bayes import GaussianNB
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split
from ..utils import extract_submatrices, extract_wrapped_pattern


class MonsterRenderer:
    def __init__(self, id_matrix, size):
        super().__init__()

        self.size = size

        patterns = extract_submatrices(extract_wrapped_pattern, size, np.array(id_matrix))

        # Fit the model
        self.clf = self.setup(patterns)

    def setup(self, patterns):
        X = [p.flatten() for p in patterns]
        y = [vector[0] for vector in X]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

        # clf = GaussianNB()
        # clf = KNeighborsClassifier(3)
        # clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
        clf = AdaBoostClassifier()
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)

        return clf

    def render_patterns(self, identifiers):
        n, m = identifiers.shape

        rendered = [[-1 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                p = extract_wrapped_pattern(identifiers, i, j, self.size)

                rendered[i][j] = self.clf.predict([p.flatten()])[0]

        return rendered
