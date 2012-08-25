import os
import re
import sys
import glob
import marshal

from poemy import soundparts


if __name__ == '__main__':
    db = {}
    db['sounds'] = {}         # delisted -> ['D IY L IH S T IH D', ...]
    db['meters'] = {}         # delisted -> ['110', ...]
    db['rhyme'] = {}          # IH D -> wretched, winded, wielded, ...
    db['brhyme'] = {}         # IY -> regal, eagle, ...
    db['frhyme'] = {}         # EY N T AH D -> painted, acquainted, ...
    db['mets'] = {}           # 110 -> delisted, digested, discounted, ...
    db['syl2words'] = {}      # 1 -> cat, hat, log, dog, bam, doh, ...
    db['front'] = {}          # T -> typo, tycoon, tye, ...
    db['back'] = {}           # T -> zealot, what, hat, zapped, ...
    db['lex2words'] = {}      # 8 -> womb, tissue, thumb, scab, ...
    db['word2lex'] = {}       # tissue -> 8, 27, 36
    db['adjectives'] = set()  # all english adjectives from wordnet
    db['adverbs'] = set()     # all english adverbs from wordnet
    db['nouns'] = set()       # all english nouns from wordnet
    db['verbs'] = set()       # all english verbs from wordnet
    db['words'] = set()       # all words from specified corpora
    db['chain'] = {}          # markov chain built from specified corpora

    if len(sys.argv) == 1:
        print "please specify at least one corpus"
        sys.exit(1)
    for corpus in sys.argv[1:]:
        if not os.path.exists('corpora/' + corpus):
            print "'%s' corpus not found" % (corpus)
            sys.exit(1)

    print 'loading cmudict.txt...'
    for line in open('cmudict.txt').readlines():
        if not line or line.startswith(';;;'):
            continue
        word, pron = line.split('  ')
        if word.endswith(')'):
            word = word[:-3]
        word = word.lower().replace('_', ' ')
        pron = pron.strip()
        sound = re.sub(r'\d', '', pron)
        meter = re.sub(r'\D', '', pron).replace('2', '1')
        db['sounds'].setdefault(word, []).append(sound)
        db['meters'].setdefault(word, [])
        if meter not in db['meters'][word]:
            db['meters'][word].append(meter)
        db['mets'].setdefault(meter, set()).add(word)
        db['syl2words'].setdefault(len(meter), set()).add(word)
        snds = sound.split()
        db['front'].setdefault(snds[0], set()).add(word)
        db['back'].setdefault(snds[-1], set()).add(word)
        _, syls = soundparts(sound)
        db['rhyme'].setdefault(syls[-1], set()).add(word)
        db['brhyme'].setdefault(syls[0], set()).add(word)
        while len(syls) >= 2:
            db['frhyme'].setdefault(' '.join(syls), set()).add(word)
            syls = syls[1:]

    print 'loading wordnet...'
    for path in glob.glob('wordnet/data.*'):
        for line in open(path).readlines():
            if not line or line.startswith('  '):
                continue
            toks = line.split()
            lex = int(toks[1])
            wtype = toks[2]
            cnt = int(toks[3], 16)
            for n in range(cnt):
                word = toks[4 + n * 2].replace('_', ' ')
                db['lex2words'].setdefault(lex, set()).add(word)
                db['word2lex'].setdefault(word, set()).add(lex)
                if wtype == 'r':
                    db['adverbs'].add(word)
                elif wtype == 'n':
                    db['nouns'].add(word)
                elif wtype in ('a', 's'):
                    db['adjectives'].add(word)
                elif wtype == 'v':
                    db['verbs'].add(word)

    for corpus in sys.argv[1:]:
        print "loading '%s' corpus..." % (corpus)
        for path in glob.glob('corpora/%s/*.txt' % (corpus)):
            data = open(path).read()
            data = data.lower()
            data = re.sub(r"[^-'\n a-z]", r'', data)
            data = re.sub(r"([a-z])-+(\s)", r'\1\2', data)
            data = re.sub(r"(\s)-+([a-z])", r'\1\2', data)
            db['words'] |= set(data.split())
            for line in data.splitlines():
                if not line.strip():
                    continue
                try:
                    iwords = iter(line.split())
                    w1 = iwords.next()
                    w2 = iwords.next()
                    while True:
                        w3 = iwords.next()
                        db['chain'].setdefault((w1, w2), []).append(w3)
                        w1, w2 = w2, w3
                except StopIteration:
                    pass

    print 'marshaling...'
    marshal.dump(db, open('db.marshal', 'w'))
