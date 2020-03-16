from .interface import Interface
from .texture import Texture

from .classifiers.deterministic import DeterministicClassifier
from .validators.deterministic import DeterministicValidator
from .validators.sk import MonsterValidator
from .renderers.deterministic import DeterministicRenderer
from .renderers.sk import MonsterRenderer


CLASSIFIERS = [
    DeterministicClassifier
]

VALIDATORS = [
    DeterministicValidator,
    MonsterValidator
]

RENDERERS = [
    DeterministicRenderer,
    MonsterRenderer
]
