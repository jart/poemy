import os
import sys
import bisect
import marshal


def similar(categories, examples, depth=2):
    """Returns a set of similar words within a lexical category"""
    categories = set(lexids[c] for c in categories)
    similar = set()
    visited = set()
    def work(word, recurse):
        if recurse == 0:
            return
        if word in visited:
            return
        visited.add(word)
        for lexid, wtype, words, ptrs, defin in lookup(word):
            for w in words:
                if lexid in categories:
                    similar.add(w)
                work(w, recurse - 1)
            for ptype, pwtype, poffset in ptrs:
                if pwtype not in ('~', '@', '+'):
                    continue
                lexid, wtype, words, ptrs, defin = lookup_offset(pwtype, poffset)
                for w in words:
                    work(w, recurse - 1)
    for word in examples:
        work(word, depth)
    return similar


def lookup(lemma, wtypes=None):
    """Return all WordNet entries associated with a particular word"""
    lemma = lemma.lower().replace(' ', '_')
    wtypes = wtypes or ('noun', 'verb', 'adj', 'adv')
    for wtype in wtypes:
        lemmas, offsets = index[wtype]
        i = bisect.bisect_left(lemmas, lemma)
        if i < len(lemmas) and lemma == lemmas[i]:
            for offset in offsets[i]:
                yield lookup_offset(wtype, offset)


def lookup_offset(wtype, offset):
    """Look up a WordNet entry provided the word type and offset in file"""
    data[wtype].seek(int(offset))
    line = data[wtype].readline()
    fields, definition = line.split(' | ', 1)
    definition = definition.strip()
    fields = fields.split()
    assert fields[0] == offset
    wcnt = int(fields[3], 16)
    lexid = int(fields[1])
    j = 4
    words = [w.replace('_', ' ') for w in fields[j:j + wcnt * 2:2]]
    j += wcnt * 2
    pcnt = int(fields[j])
    j += 1
    ptrs = []
    for i in range(pcnt):
        ptype = fields[j]
        poffset = fields[j + 1]
        pwtype = _wtypefix(fields[j + 2])
        psrctar = fields[j + 3]
        ptrs.append((ptype, pwtype, poffset))
        j += 4
    return (lexid, wtype, tuple(words), tuple(ptrs), definition)


def _load(name):
    """Load index into sorted tuple for binary search (1/3 memory of a dict)"""
    lemmas = []
    offsets = []
    with open(os.path.join(wordnetdir, 'index.' + name)) as fp:
        for line in fp:
            if line.startswith('  '):
                continue
            line = line.split()
            lemmas.append(line[0])
            offsets.append(tuple(p for p in line[1:] if len(p) == 8))
    return tuple(lemmas), tuple(offsets)


def _wtypefix(wtype):
    return {
        'n': 'noun',
        'v': 'verb',
        'a': 'adj',
        'r': 'adv',
    }[wtype]


def ptrname(ptype, wtype='noun'):
    if ptype == '\\':
        if wtype == 'adv':
            return 'Derived from adjective'
        else:
            return 'Pertainym (pertains to noun)'
    return {
        '!': 'Antonym',
        '@': 'Hypernym',
        '@i': 'Instance Hypernym',
        '~': 'Hyponym',
        '~i': 'Instance Hyponym',
        '#m': 'Member holonym',
        '#s': 'Substance holonym',
        '#p': 'Part holonym',
        '%m': 'Member meronym',
        '%s': 'Substance meronym',
        '%p': 'Part meronym',
        '*': 'Entailment',
        '>': 'Cause',
        '^': 'Also see',
        '$': 'Verb Group',
        '=': 'Attribute',
        '&': 'Similar to',
        '+': 'Derivationally related form',
        ';c': 'Domain of synset - TOPIC',
        '-c': 'Member of this domain - TOPIC',
        ';r': 'Domain of synset - REGION',
        '-r': 'Member of this domain - REGION',
        ';u': 'Domain of synset - USAGE',
        '-u': 'Member of this domain - USAGE',
    }[ptype]


codedir = os.path.dirname(os.path.abspath(__file__))
wordnetdir = os.path.join(codedir, 'data/wordnet')
data = {
    'noun': open('data/wordnet/data.noun'),
    'verb': open('data/wordnet/data.verb'),
    'adj': open('data/wordnet/data.adj'),
    'adv': open('data/wordnet/data.adv'),
}

if not os.path.exists(os.path.join(wordnetdir, 'index.marshal')):
    index = {
        'noun': _load('noun'),
        'verb': _load('verb'),
        'adj': _load('adj'),
        'adv': _load('adv'),
    }
    with open(os.path.join(wordnetdir, 'index.marshal'), 'w') as fp:
        marshal.dump(index, fp)
else:
    with open(os.path.join(wordnetdir, 'index.marshal')) as fp:
        index = marshal.load(fp)

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


if __name__ == '__main__':
    if sys.argv[1] == 'tree':
        for lexid, wtype, words, ptrs, defin in lookup(sys.argv[2]):
            s = "%s (%s)" % (', '.join(words), lexnames[lexid])
            print "%-90s %s" % (s, defin)
            for ptype, pwtype, poffset in ptrs:
                lexid, wtype, words, ptrs, defin = lookup_offset(pwtype, poffset)
                s = "%s: %s (%s)" % (ptrname(ptype, wtype), ', '.join(words), lexnames[lexid])
                print "    %-86s %s" % (s, defin)
                for ptype, pwtype, poffset in ptrs:
                    lexid, wtype, words, ptrs, defin = lookup_offset(pwtype, poffset)
                    s = "%s: %s (%s)" % (ptrname(ptype, wtype), ', '.join(words), lexnames[lexid])
                    print "        %-82s %s" % (s, defin)

    if sys.argv[1] == 'lexs':
        lexs = {}
        for word in sys.argv[2:]:
            for lexid, wtype, words, ptrs, defin in lookup(word):
                lexs.setdefault(lexid, 0)
                lexs[lexid] += 1
        for lexid, score in sorted(lexs.items(), key=lambda x: x[1], reverse=True):
            examples = list(similar([lexnames[lexid]], sys.argv[2:]))[:10]
            print score, lexnames[lexid], '(' + ', '.join(examples) + ')'

    if sys.argv[1] == 'similar':
        for w in similar([sys.argv[2]], sys.argv[3:]):
            print w
