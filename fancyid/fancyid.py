import functools
import random
import re
import string
from dataclasses import dataclass
from enum import Enum, auto

from fancyid.words import _ADJECTIVES, _ANIMALS


class FancyIdGenerator:
    """
    This class may be used to generate a reproducible sequence of fancy IDs.
    """

    def __init__(self, format: str | None = None, seed: int | None = None, skip: int | None = None) -> None:
        """
        :param format: Optional format string describing the structure of the IDs that will be returned by this
            `FancyIdGenerator`. If not specified, IDs will be of the form "AdjectiveAdjectiveAnimal".
        :param seed: Optional seed for the internal random generator.
        :param skip: Optional offset to skip forward in the random sequence produced by this `FancyIdGenerator`
            instance. Passing `skip=N` is equivalent to calling `FancyIdGenerator.generate` N times.
        """
        self.spec = _parse_format_string(format) if format else DEFAULT_SPEC
        self.random = random.Random(seed)
        if skip:
            for _ in range(skip):
                self.generate()

    def generate(self) -> str:
        """
        Generate the next random fancy ID in the random sequence represented by this class.

        :return: A fancy string identifier.
        """
        return _generate_from_spec(self.spec, self.random)


def generate(format: str | None = None) -> str:
    """
    Generate a random fancy ID.

    If `format` is not specified, the ID will be of the form "AdjectiveAdjectiveAnimal".

    :param format: Optional format string specifying the structure of the ID that should be returned.
    :return: A fancy string identifier.
    """
    spec = _parse_format_string(format) if format else DEFAULT_SPEC
    return _generate_from_spec(spec)


def estimate_possible_ids(format: str) -> int:
    """
    Estimate the number of unique random identifiers which may be generated from a given format string. This is an
    upper bound, as it doesn't take repeated component words into account.

    :param format: The format string.
    :return: An approximate number of random unique identifiers which may be generated from the input format string.
    """
    spec = _parse_format_string(format)
    return functools.reduce(lambda n1, n2: n1 * n2, (len(WORDS[group.upper()]) for group in spec.word_groups))


class Casing(Enum):
    LOWER = auto()
    UPPER = auto()
    CAMEL = auto()
    LOWER_CAMEL = auto()


@dataclass
class FancyIdSpec:
    word_groups: list[str]
    casing: Casing
    separator: str


DEFAULT_SPEC = FancyIdSpec(word_groups=["ADJECTIVE", "ADJECTIVE", "ANIMAL"], casing=Casing.CAMEL, separator="")


PUNCTUATION = "".join(c for c in string.punctuation)
PUNCTUATION_REGEX = re.compile(fr"[^{PUNCTUATION}+]([{PUNCTUATION}]+)[^{PUNCTUATION}]+")
WHITESPACE_REGEX = re.compile(fr"[^\W+](\W+)[^\W]+")


def _parse_format_string(format_str: str) -> FancyIdSpec:
    separator = ""
    if punctuation_match := PUNCTUATION_REGEX.search(format_str):
        separator = punctuation_match.groups(1)[0]
    elif whitespace_match := WHITESPACE_REGEX.search(format_str):
        separator = whitespace_match.groups(1)[0]

    if separator != "":
        word_groups = format_str.split(separator)
    else:
        # This is not smart, but it's about as smart as I can be given my current level of caffeination.
        word_groups = []
        chunk_start_index = 0
        for i in range(len(format_str) + 1):
            chunk = format_str[chunk_start_index:i]
            if chunk.upper() in WORDS.keys():
                word_groups.append(chunk)
                chunk_start_index = i

    bad_word_groups = [group for group in word_groups if group.upper() not in WORDS.keys()]
    if any(bad_word_groups):
        raise ValueError(f"Unknown word groups: {bad_word_groups}")

    if not any(word_groups):
        raise ValueError("Format string did not contain any valid word groups")

    # Determine casing
    if all(word.isupper() for word in word_groups):
        casing = Casing.UPPER
    elif all(word.islower() for word in word_groups):
        casing = Casing.LOWER
    elif word_groups[0][0].islower() and all(word[0].isupper() for word in word_groups[1:]):
        casing = Casing.LOWER_CAMEL
    else:
        casing = Casing.CAMEL

    return FancyIdSpec(word_groups=word_groups, casing=casing, separator=separator)


WORDS = {
    "ADJECTIVE": _ADJECTIVES,
    "ANIMAL": _ANIMALS
}


def _generate_from_spec(spec: FancyIdSpec, rng: random.Random = None) -> str:
    generator = rng.choice if rng else random.choice
    words = [generator(WORDS[group.upper()]) for group in spec.word_groups]

    if spec.casing == Casing.LOWER:
        words = [word.lower() for word in words]
    elif spec.casing == Casing.UPPER:
        words = [word.upper() for word in words]
    elif spec.casing == Casing.CAMEL:
        words = [word.capitalize() for word in words]
    elif spec.casing == Casing.LOWER_CAMEL:
        words = [words[0].lower()] + [word.capitalize() for word in words[1:]]

    return spec.separator.join(words)
