import numpy as np

from pprint import pprint
from collections import defaultdict

from wfc.extraction import compatible, dirs
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split


def d2v(direction):
    x, y = direction

    if x == 1:
        return [1, 0, 0, 0]
    if x == -1:
        return [0, 0, 1, 0]
    if y == 1:
        return [0, 1, 0, 0]
    if y == -1:
        return [0, 0, 0, 1]

    raise Exception('`direction` arg', direction, 'is not a valid direction.')


class MonsterValidator:
    def __init__(self, alpha=.0):
        super().__init__()

        self.adjacency_rules = defaultdict(list)

        # Fit the model
        self.clf = self.setup(map(lambda p: p.matrix, patterns))

        self.learn(patterns)

    def setup(self, patterns):
        X, y = [], []
        for p1 in patterns:
            for p2 in patterns:
                for d in dirs:
                    fp1 = p1.flatten()
                    fp2 = p2.flatten()
                    direction_vector = np.array(d2v(d))
                    vector = np.concatenate((fp1, fp2, direction_vector))
                    X.append(vector)
                    y.append(1 if compatible(p1, p2, d) else 0)

        # y = [vector[0] for vector in X]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=.2, random_state=42)

        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        pprint(score)

        return clf

    def learn(self, patterns):
        # Learn adjacencies
        for p1 in patterns:
            for p2 in patterns:
                for d in dirs:
                    (x, y) = d

                    fp1 = p1.matrix.flatten()
                    fp2 = p2.matrix.flatten()
                    direction_vector = np.array(d2v(d))
                    vector = np.concatenate((fp1, fp2, direction_vector))
                    if self.clf.predict([vector])[0]:
                        self.adjacency_rules[(p1.index, d)].append(p2.index)
                        self.adjacency_rules[(p2.index, (-x, -y))].append(p1.index)
        # pprint(self.adjacency_rules, width=1000)
        return self

    def valid(self, identifier, direction):
        return self.adjacency_rules[identifier, direction]
