from poemy import *


def test_rhyme():
    assert is_rhyme('rhyme', 'sublime')
    assert is_rhyme('thee', 'philosophy')
    assert is_rhyme('spent', 'went')
    assert is_rhyme('produced', 'reduced')
    assert is_rhyme('head', 'tread')
    assert is_rhyme('bore', 'lore')
    assert is_rhyme('outpour', 'before')
    assert is_rhyme('head', 'tread')
    assert is_rhyme('head', 'tread')


def test_frhyme():
    assert is_frhyme('painted', 'acquainted')
    assert is_frhyme('passion', 'fashion')
    assert is_frhyme('regal', 'eagle')
    assert is_frhyme('rolling', 'controlling')
    # assert is_frhyme('created', 'defeated')  # close but no cigar Shakespeare
    assert is_frhyme('pleasure', 'treasure')
    assert is_frhyme('ungainly', 'plainly')
    assert is_frhyme('napping', 'tapping')
    assert is_frhyme('dreary', 'weary')
    assert not is_frhyme('rhyme', 'sublime')
    assert not is_frhyme('thee', 'philosophy')
    assert not is_frhyme('spent', 'went')
    # assert not is_frhyme('produced', 'reduced')
    assert not is_frhyme('head', 'tread')
    assert not is_frhyme('bore', 'lore')
    assert not is_frhyme('outpour', 'before')
    assert not is_frhyme('head', 'tread')
    assert not is_frhyme('head', 'tread')
