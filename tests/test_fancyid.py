import pytest

import fancyid
from fancyid import FancyIdGenerator


def test_generate_does_not_explode() -> None:
    fancy_ids = [fancyid.generate() for _ in range(1000)]

    assert all(isinstance(i, str) for i in fancy_ids)


def test_generate_respects_format_string() -> None:
    fancy_id = fancyid.generate(format="ADJECTIVE_ADJECTIVE_ANIMAL")

    components = fancy_id.split("_")
    assert len(components) == 3
    assert all(component.isupper() for component in components)


def test_fancy_id_generator_respects_format_string() -> None:
    generator = FancyIdGenerator(seed=13379999, format="ADJECTIVE_ADJECTIVE_ANIMAL")

    silent_drab_oyster = generator.generate()

    assert silent_drab_oyster == "SILENT_DRAB_OYSTER"


def test_fancy_id_generator_with_seed_generates_reproducible_sequence() -> None:
    generator_1 = FancyIdGenerator(seed=13379999)
    generator_2 = FancyIdGenerator(seed=13379999)

    sequence = [(generator_1.generate(), generator_2.generate()) for _ in range(100)]

    assert all(id1 == id2 for id1, id2 in sequence)


def test_fancy_id_generator_with_skip_is_equivalent_to_repeated_generate_calls() -> None:
    skip_generator = FancyIdGenerator(seed=13379999, skip=1000)
    normal_generator = FancyIdGenerator(seed=13379999)
    for _ in range(1000):
        normal_generator.generate()

    sequence = [(skip_generator.generate(), normal_generator.generate()) for _ in range(100)]

    assert all(id1 == id2 for id1, id2 in sequence)


def test_estimate_possible_ids_seems_plausible() -> None:
    some_number_of_ids = fancyid.estimate_possible_ids("ADJECTIVE-ANIMAL")
    a_larger_number_of_ids = fancyid.estimate_possible_ids("ADJECTIVE-ADJECTIVE-ANIMAL")

    assert some_number_of_ids < a_larger_number_of_ids


def test_format_string_separator_punctuation() -> None:
    format_str = "Adjective-Adjective-Animal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "Silent-Drab-Oyster"


def test_format_string_separator_whitespace() -> None:
    format_str = "Adjective Adjective Animal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "Silent Drab Oyster"


def test_format_string_no_separator() -> None:
    format_str = "AdjectiveAdjectiveAnimal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "SilentDrabOyster"


def test_format_string_many_word_groups() -> None:
    format_str = "AdjectiveAdjectiveAnimalAnimalAdjectiveAnimal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "SilentDrabOysterWombatExcellentElephant"


def test_format_string_upper_case() -> None:
    format_str = "ADJECTIVE ADJECTIVE ANIMAL"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "SILENT DRAB OYSTER"


def test_format_string_lower_case() -> None:
    format_str = "adjective adjective animal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "silent drab oyster"


def test_format_string_camel_case() -> None:
    format_str = "AdjectiveAdjectiveAnimal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "SilentDrabOyster"


def test_format_string_lower_camel_case() -> None:
    format_str = "adjectiveAdjectiveAnimal"
    generator = FancyIdGenerator(seed=13379999, format=format_str)

    fancy_id = generator.generate()

    assert fancy_id == "silentDrabOyster"


def test_format_string_bad_word_group_with_separator_throws() -> None:
    bad_format_str = "wibble wobble"
    with pytest.raises(ValueError):
        FancyIdGenerator(format=bad_format_str)


def test_format_string_bad_word_group_without_separator_throws() -> None:
    bad_format_str = "wibblewobble"
    with pytest.raises(ValueError):
        FancyIdGenerator(format=bad_format_str)
