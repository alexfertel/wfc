from collections import defaultdict

from .validator import Validator
from ..utils import compatible, dirs, d2s
from sklearn.tree import DecisionTreeClassifier

class MonsterValidator(Validator):
    def __init__(self, patterns):
        super().__init__()

        self.patterns = patterns
        self.adjacency_rules = defaultdict(list)

        # Fit the model
        self.clf = self.setup(map(lambda p: p.matrix, patterns))

        self.learn_adjacencies()

    def setup(self, patterns):
        ps = [p.flatten() for p in patterns]

        X, y = [], []
        for x in ps:
            for y in ps:
                for d in dirs:
                    X.append(np.concatenate(x, y, np.array(d2s(d))))
                    y.append(1 if compatible(x, y, d) else 0)


        # y = [vector[0] for vector in X]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

        # clf = GaussianNB()
        # clf = KNeighborsClassifier(3)
        # clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        # score = clf.score(X_test, y_test)

        return clf

    def learn_adjacencies(self):
        # Learn adjacencies
        for p1 in self.patterns:
            for p2 in self.patterns:
                for x, y in dirs:
                    d = (x, y)

                    vector = np.concatenate(p1, p2, np.array(d2s(d)))
                    if self.clf.predict([vector])[0]:
                        self.adjacency_rules[(p1.index, d)].append(p2.index)
                        self.adjacency_rules[(p2.index, (-x, -y))].append(p1.index)
        pprint(self.adjacency_rules)
        return self

    def valid_adjacencies(self, identifier, direction):
        return self.adjacency_rules[identifier, direction]

