import os
import re
import gc
import sys
import glob
import marshal

from poemy import soundparts, soundparts_left


if __name__ == '__main__':
    db = {}
    db['cmudict'] = {}        # delisted -> ['D IY1 L IH1 S T IH0 D', ...]
    db['sounds'] = {}         # delisted -> ['D IY L IH S T IH D', ...]
    db['meters'] = {}         # delisted -> ['110', ...]
    db['rhyme'] = {}          # IH D -> wretched, winded, wielded, ...
    db['brhyme'] = {}         # IY -> regal, eagle, ...
    db['frhyme'] = {}         # EY N T AH D -> painted, acquainted, ...
    db['meterwords'] = {}     # 110 -> delisted, digested, discounted, ...
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

    gc.disable()

    print 'loading cmudict.txt...'
    for line in open('data/cmudict.txt').readlines():
        if not line.strip() or line.startswith(';;;'):
            continue
        word, pron = line.split('  ')
        if word.endswith(')'):
            word = word[:-3]
        word = word.lower().replace('_', ' ')
        pron = pron.strip()
        sound = re.sub(r'\d', '', pron)
        meter = re.sub(r'\D', '', pron).replace('2', '1')
        db['cmudict'].setdefault(word, []).append(pron)
        db['sounds'].setdefault(word, []).append(sound)
        db['syl2words'].setdefault(len(meter), set()).add(word)
        if len(meter) > 1:
            db['meters'].setdefault(word, []).append(meter)
            db['meterwords'].setdefault(meter, set()).add(word)
        snds = sound.split()
        db['front'].setdefault(snds[0], set()).add(word)
        db['back'].setdefault(snds[-1], set()).add(word)
        _, syls = soundparts(sound)
        db['rhyme'].setdefault(syls[-1], set()).add(word)
        db['brhyme'].setdefault(syls[0], set()).add(word)
        while len(syls) >= 2:
            db['frhyme'].setdefault(' '.join(syls), set()).add(word)
            syls = syls[1:]

    # ok so here's the deal: cmudict does a great job telling us which
    # syllables are stressed in words with more than one syllable, but when it
    # comes to single syllable words, it always marks them as stressed. this
    # is incorrect because some words are highly stressed (like: cat, dog,
    # bog) and some words are almost never stressed (like: on, a, the). we
    # need to be able to tell the difference in order to maintain a consistent
    # meter.
    #
    # so what we do is we take all the multi-syllable words and build two
    # tables that tell us the probability that a word starting or ending with
    # a particular sound will be stressed. then we go through each single
    # syllable word and compare its start/end sounds to the probability tables
    # to determine the likelihood that the word is stressed
    print 'calculating probability of syllable stress...'
    starters = {}
    enders = {}
    for w in (db['syl2words'][2] | db['syl2words'][3] | db['syl2words'][4] |
              db['syl2words'][5] | db['syl2words'][6] | db['syl2words'][7]):
        for ss, ms in zip(db['sounds'][w], db['meters'][w]):
            s, m = soundparts_left(ss)[0][0], int(ms[0])
            starters.setdefault(s, [0.0, 0.0])[m] += 1.0
            s, m = soundparts(ss)[1][-1], int(ms[-1])
            enders.setdefault(s, [0.0, 0.0])[m] += 1.0
    starters = {s: v[1] / (v[0] + v[1]) for s, v in starters.iteritems()}
    enders = {s: v[1] / (v[0] + v[1]) for s, v in enders.iteritems()}

    print 'guessing which single syllable words are stressed...'
    db['meterwords']['0'] = set()
    db['meterwords']['1'] = set()
    for w in db['syl2words'][1]:
        start = soundparts_left(db['sounds'][w][0])[0][0]
        end = soundparts(db['sounds'][w][0])[1][-1]
        p = (starters.get(start, 0.6) + enders.get(end, 0.6)) / 2.0
        if p < 0.5:
            db['meters'][w] = ['0']
            db['meterwords']['0'].add(w)
        elif p < 0.7:
            db['meters'][w] = ['0', '1']
            db['meterwords']['0'].add(w)
            db['meterwords']['1'].add(w)
        else:
            db['meters'][w] = ['1']
            db['meterwords']['1'].add(w)

    print 'loading wordnet...'
    for path in glob.glob('data/wordnet/data.*'):
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
            data = re.sub(r'\.', '\n', data)
            data = re.sub(r"[^-'\n a-z]", r' ', data)
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
        for key in db['chain'].keys():
            db['chain'][key] = list(set(db['chain'][key]))
            db['chain'][key].sort(key=lambda w: len(w), reverse=True)

    print 'marshaling...'
    marshal.dump(db, open('db.marshal', 'w'))
