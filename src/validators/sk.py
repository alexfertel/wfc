from collections import defaultdict

from .validator import Validator
from ..utils import compatible, dirs, d2s


class MonsterValidator(Validator):
    def __init__(self, patterns):
        super().__init__()

        self.patterns = patterns
        self.adjacency_rules = defaultdict(list)

        # self.learn_adjacencies()

        # Fit the model
        self.clf = self.setup(patterns)

    def setup(self, patterns):
        ps = [p.flatten() for p in patterns]

        X, y = [], []
        for x in ps:
            for y in ps:
                for d in dirs:
                    X.append((x, y, np.array(d2s(d))))
                    y.append(compatible(x, y, d))


        # y = [vector[0] for vector in X]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

        # clf = GaussianNB()
        # clf = KNeighborsClassifier(3)
        # clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
        clf = AdaBoostClassifier()
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)

        return clf

    def learn_adjacencies(self):
        # Learn adjacencies
        for p1 in self.patterns:
            for p2 in self.patterns:
                for x, y in dirs:
                    d = (x, y)
                    if compatible(p1.matrix, p2.matrix, d):
                        self.adjacency_rules[(p1.index, d)].append(p2.index)
                        self.adjacency_rules[(p2.index, (-x, -y))].append(p1.index)
        pprint(self.adjacency_rules)
        return self

    def valid_adjacencies(self, identifier, direction):
        return self.adjacency_rules[identifier, direction]