# fancyid

Fancy string identifiers for human consumption.

## Quick start

Installation:

```
pip install fancyid
```

Usage:

```python3
import fancyid


# Generate IDs using the default AdjectiveAdjectiveAnimal format

fancyid.generate()
# "GiganticGreenTortoise"


# Generate IDs using a custom format string

fancyid.generate("adjective-animal")
# "gigantic-tortoise"


# Create a generator instance using a fixed seed

fancy_generator = fancyid.Generator(format="adjective-animal", seed=1337)
fancy_generator.generate()
# "sure-footed-mouse"


# Create a generator instance and skip forward in the sequence of IDs:

skip_fancy_generator = fancyid.Generator(format="adjective-animal", seed=1337, skip=1)
skip_fancy_generator.generate()
# "weighty-heron"
```


## Format strings

Format strings allow you to specify three things:

* The choice/number of words
* The separator between the words
* The casing of the words

Here are some exmaples of valid format strings:

| Format string | Example ID |
| --- | --- |
| `"AdjectiveAnimal"` | `BigTortoise` |
| `"adjective-animal-animal"` | `big-tortoise-penguin` |
| `"adjectiveAdjectiveAnimal"` |  `bigGreenTortoise` |
| `"ADJECTIVE ANIMAL"` | `BIG TORTOISE` |

Currently-understood categories of word: adjective, animal. That's it.


## Sources of words

https://gist.github.com/raineorshine/599777e98e5e968a15c545043973f035
https://github.com/sroberts/wordlists/

and a few additions from me.
