r"""

    poemy
    ~~~~~

    A poetry generator.

"""

import marshal
from itertools import product

from contracts import contract

import mycontracts


# EY / IY <-- very similar

vowels = set('AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW'.split())
consonants = set('B CH D DH F G HH JH K L M N NG P R S SH T TH V W '
                 'Y Z ZH'.split())
phonemes = vowels | consonants
semi_vowels = set('W Y'.split())
stop_consonants = set('B D G K P T'.split())
liquid_consonants = set('L R'.split())
nasal_consonants = set('M N NG'.split())
fricative_consonants = set('DH F S SH TH V Z ZH'.split())
affricate_consonants = set('CH JH'.split())  # should go in stop/fricative too?

lexnames = {
    0: "adj.all",
    1: "adj.pert",
    2: "adv.all",
    3: "noun.tops",
    4: "noun.act",
    5: "noun.animal",
    6: "noun.artifact",
    7: "noun.attribute",
    8: "noun.body",
    9: "noun.cognition",
    10: "noun.communication",
    11: "noun.event",
    12: "noun.feeling",
    13: "noun.food",
    14: "noun.group",
    15: "noun.location",
    16: "noun.motive",
    17: "noun.object",
    18: "noun.person",
    19: "noun.phenomenon",
    20: "noun.plant",
    21: "noun.possession",
    22: "noun.process",
    23: "noun.quantity",
    24: "noun.relation",
    25: "noun.shape",
    26: "noun.state",
    27: "noun.substance",
    28: "noun.time",
    29: "verb.body",
    30: "verb.change",
    31: "verb.cognition",
    32: "verb.communication",
    33: "verb.competition",
    34: "verb.consumption",
    35: "verb.contact",
    36: "verb.creation",
    37: "verb.emotion",
    38: "verb.motion",
    39: "verb.perception",
    40: "verb.possession",
    41: "verb.social",
    42: "verb.stative",
    43: "verb.weather",
    44: "adj.ppl",
}
lexids = {v: k for k, v in lexnames.items()}

stopwords = set('''
a about above above across after afterwards again against all almost alone
along already also although always am among amongst amoungst amount an and
another any anyhow anyone anything anyway anywhere are around as at back be
became because become becomes becoming been before beforehand behind being
below beside besides between beyond bill both bottom but by call can cannot
cant co con could couldnt de describe detail do done down due during each eg
eight either eleven else elsewhere empty enough etc even ever every everyone
everything everywhere except few fifteen fify fill find fire first five for
former formerly forty found four from front full further get give go had has
hasnt have he hence her here hereafter hereby herein hereupon hers herself him
himself his how however hundred ie if in inc indeed interest into is it its
itself keep last latter latterly least less ltd made many may me meanwhile
might mill mine more moreover most mostly move much must my myself name namely
neither never nevertheless next nine no nobody none noone nor not nothing now
nowhere of off often on once one only onto or other others otherwise our ours
ourselves out over own part per perhaps please put rather re same see seem
seemed seeming seems serious several she should show side since sincere six
sixty so some somehow someone something sometime sometimes somewhere still
such system take ten than that the their them themselves then thence there
thereafter thereby therefore therein thereupon these they thickv thin third
this those though three through throughout thru thus to together too top
toward towards twelve twenty two un under until up upon us very via was we
well were what whatever when whence whenever where whereafter whereas whereby
wherein whereupon wherever whether which while whither who whoever whole whom
whose why will with within without would yet you your yours yourself
yourselves the thee thy thyself thine hast dost thou art shalt shall wilst
didst hath wert doth wouldst hitherto ought nought i o
'''.split())


class DB(object):
    r"""Lazily loaded poem database"""

    def __init__(self):
        self.db = None

    def load(self):
        if not self.db:
            self.db = marshal.load(open('db.marshal'))

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            self.load()
            return self.db[key]


@contract
def wordsounds(word):
    r"""Returns how a word is pronounced

    For example::

        >>> wordsounds('dog')
        ['D AO G']
        >>> wordsounds('adult')
        ['AH D AH L T', 'AE D AH L T']

    :param word: Word to look up
    :type word:  word
    :return:     List of strings of phonemes separated by spaces
    :rtype:      list[>=1](sound)
    """
    return db.sounds[word]


@contract
def wordmeters(word):
    r"""Returns how each syllable is emphasized

    For example::

        >>> wordmeters('adulterate')
        ['0101']
        >>> wordmeters('adult')
        ['01', '10']
        >>> wordmeters('created')
        ['010']

    :param word: Word to look up
    :type word:  word
    :return:     List of strings of 1/0's to denote emphasis of syllables
    :rtype:      list[>=1](meter)
    """
    return db.meters[word]


@contract
def meterwords(meter):
    r"""Return all words greater than one syllable compatible with meter

    This function is memoized.

    For example::

        >>> 'adulterate' in meterwords('01' * 5)
        True
        >>> 'created' in meterwords('01' * 5)
        True
        >>> 'biggie' in meterwords('01' * 5)
        False

    :param meter: Meter to be consumed
    :type meter:  meter
    :return:      List of strings of 1/0's to denote emphasis of syllables
    :rtype:       myset
    """
    if len(meter) <= 1:
        return set()
    happy = set()
    for n in range(1, 5):
        if len(rim) >= n:
            happy |= poemy.db.mets[rim[:n]]


@contract
def soundparts(sound):
    r"""Break sound down into syllables

    When rhyming, we need a syllable sound which consists of a vowel and its
    following consonants. The bare consonant at the beginning of a word
    doesn't matter when rhyming and is only useful for alliteration.

    For example:

        >>> soundparts('P AE SH AH N')
        ('P', ['AE SH', 'AH N'])
        >>> soundparts('DH IY')
        ('DH', ['IY'])
        >>> soundparts('AE D AH P OW S')
        ('', ['AE D', 'AH P', 'OW S'])

    :param sound: Full sound phonemes for a word
    :type sound:  sound
    :return:      Onset consonant (if any) and list of phonemes each syllable
    :rtype:       tuple(str, list[>=1](sound))
    """
    res = []
    part = []
    for snd in sound.split():
        if snd in vowels:
            res.append(' '.join(part))
            part = []
        part.append(snd)
    if part:
        res.append(' '.join(part))
    return res[0], res[1:]


@contract
def is_rhyme(word1, word2):
    r"""Test if last syllable of each word is pronounced the same

    This function takes into consideration various accents.

    For example::

        >>> is_rhyme('painted', 'acquainted')
        True
        >>> is_rhyme('thee', 'philosophy')
        True
        >>> is_rhyme('property', 'theft')
        False

    :param word1: First word
    :type word1:  word
    :param word2: Second word
    :type word2:  word
    :return:      True if it rhymes
    :rtype:       bool
    """
    try:
        ws1, ws2 = wordsounds(word1), wordsounds(word2)
    except KeyError:
        return False
    for s1, s2 in product(ws1, ws2):
        p1, p2 = soundparts(s1), soundparts(s2)
        if p1[1][-1] == p2[1][-1]:
            return True
    return False


@contract
def is_frhyme(word1, word2):
    r"""Test if feminine rhyme (last two syllables pronounced the same)

    This function takes into consideration various accents.

    For example::

        >>> is_frhyme('painted', 'acquainted')
        True
        >>> is_frhyme('thee', 'philosophy')
        False
        >>> is_frhyme('property', 'theft')
        False
        >>> is_frhyme('instigator', 'simulator')
        True

    :param word1: First word
    :type word1:  word
    :param word2: Second word
    :type word2:  word
    :return:      True if it rhymes in a 'feminine' manner
    :rtype:       bool
    """
    try:
        ws1, ws2 = wordsounds(word1), wordsounds(word2)
    except KeyError:
        return False
    for s1, s2 in product(ws1, ws2):
        p1, p2 = soundparts(s1), soundparts(s2)
        if (len(p1[1]) >= 2 and
            len(p2[1]) >= 2 and
            p1[1][-2] == p2[1][-2] and
            p1[1][-1] == p2[1][-1]):
            return True
    return False


db = DB()
