import functools
import random
import re
import string
from dataclasses import dataclass
from enum import Enum, auto

from words import _ADJECTIVES, _ANIMALS

WORDS = {
    "SIZE": ["small", "big", "large", "huge", "tiny", "gigantic", "teeny", "enormous"],
    "COLOR": ["red", "blue", "green", "yellow", "black", "maroon", "pink", "purple"],
    "ADJECTIVE": _ADJECTIVES,
    "ANIMAL": _ANIMALS
}


class FancyIdGenerator:
    def __init__(self, format: str | None = None, seed: int | None = None, skip: int | None = None) -> None:
        self.spec = _parse_format_string(format) if format else None
        self.random = random.Random(seed)
        if skip:
            for _ in range(skip):
                self.generate()

    def generate(self) -> str:
        return _generate_from_spec(self.spec, self.random)


class _Casing(Enum):
    LOWER = auto()
    UPPER = auto()
    CAMEL = auto()
    LOWER_CAMEL = auto()


@dataclass
class FancyIdSpec:
    word_groups: list[str]
    casing: _Casing
    separator: str


DEFAULT_SPEC = FancyIdSpec(word_groups=["ADJECTIVE", "ADJECTIVE", "ANIMAL"], casing=_Casing.CAMEL, separator="")


_PUNCTUATION = "".join(c for c in string.punctuation)
PUNCTUATION_REGEX = re.compile(fr"[^{_PUNCTUATION}+]([{_PUNCTUATION}]+)[^{_PUNCTUATION}]+")
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

    # Determine casing
    if all(word.isupper() for word in word_groups):
        casing = _Casing.UPPER
    elif all(word.islower() for word in word_groups):
        casing = _Casing.LOWER
    elif word_groups[0][0].islower() and all(word[0].isupper() for word in word_groups[1:]):
        casing = _Casing.LOWER_CAMEL
    else:
        casing = _Casing.CAMEL

    return FancyIdSpec(word_groups=word_groups, casing=casing, separator=separator)


def _generate_from_spec(spec: FancyIdSpec, rng: random.Random = None) -> str:
    generator = rng.choice if rng else random.choice
    words = [generator(WORDS[group.upper()]) for group in spec.word_groups]

    if spec.casing == _Casing.LOWER:
        words = [word.lower() for word in words]
    elif spec.casing == _Casing.UPPER:
        words = [word.upper() for word in words]
    elif spec.casing == _Casing.CAMEL:
        words = [word.capitalize() for word in words]
    elif spec.casing == _Casing.LOWER_CAMEL:
        words = [words[0].lower()] + [word.capitalize() for word in words[1:]]

    return spec.separator.join(words)


def num_unique_ids(format: str) -> int:
    spec = _parse_format_string(format)
    return functools.reduce(lambda n1, n2: n1 * n2, (len(WORDS[group.upper()]) for group in spec.word_groups))


def generate(format: str | None = None) -> str:
    spec = _parse_format_string(format) if format else DEFAULT_SPEC
    return _generate_from_spec(spec)


if __name__ == "__main__":
    format_strings = [
        "SIZECOLORANIMAL",
        "SIZE_COLOR_ANIMAL",
        "SIZE-COLOR-ANIMAL",
        "SIZE--COLOR--ANIMAL",
        "SIZE COLOR ANIMAL",
        "SIZE     COLOR     ANIMAL",
        "sizecoloranimal",
        "sizeColorAnimal",
        "size color animal animal",
        "Size-Color-Animal",
        "size_Color_Animal",
    ]

    for fmt_str in format_strings:
        gen = FancyIdGenerator(format=fmt_str, seed=1337)
        print(gen.generate())
        print(gen.generate())
        print(gen.generate())
        print()

    print(generate("adjective-adjective-animal"))
    print(generate("adjective-adjective-animal"))
    print(generate("adjective-adjective-animal"))

    print(num_unique_ids("adjective-adjective-animal"))

