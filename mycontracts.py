import re

from contracts import new_contract


@new_contract
def word(word):
    if not isinstance(word, basestring):
        raise ValueError('word must be a string')
    if not word:
        raise ValueError('word is empty')
    if word != word.lower():
        raise ValueError('word must be lowercase')
    if not re.search(r"^[-' a-z0-9]+$", word):
        raise ValueError('word has invalid characters')


@new_contract
def meter(meter):
    if not isinstance(meter, basestring):
        raise ValueError('meter must be a string')
    if not meter:
        raise ValueError('meter is empty')
    if not set(meter) <= set(['0', '1']):
        raise ValueError('meter must have only 1 and 0')


@new_contract
def sound(sound):
    import poemy
    if not isinstance(sound, basestring):
        raise ValueError('sound must be a string')
    if not sound:
        raise ValueError('sound is empty')
    if not set(sound.split()) <= poemy.phonemes:
        raise ValueError('sound contains invalid phonemes',
                         set(sound.split()) - poemy.phonemes)
