import os
import re
import glob
import marshal

from poemy import soundparts


if __name__ == '__main__':
    db = {}
    db['sound'] = {}          # delisted -> D IY L IH S T IH D
    db['altsound'] = {}
    db['meter'] = {}          # delisted -> 110
    db['altmeter'] = {}
    db['rhyme'] = {}          # IH D -> wretched, winded, wielded, ...
    db['brhyme'] = {}         # IY -> regal, eagle, ...
    db['frhyme'] = {}         # EY N T AH D -> painted, acquainted, ...
    db['mets'] = {}           # 110 -> delisted, digested, discounted, ...
    db['sibs'] = {}           # 1 -> cat, hat, log, dog, bam, doh, ...
    db['front'] = {}          # T -> typo, tycoon, tye, ...
    db['back'] = {}           # T -> zealot, what, hat, zapped, ...
    db['lex2word'] = {}       # 8 -> womb, tissue, thumb, scab, ...
    db['word2lex'] = {}       # tissue -> 8, 27, 36
    db['adjectives'] = set()
    db['adverbs'] = set()
    db['nouns'] = set()
    db['verbs'] = set()

    print 'loading cmudict.txt...'
    for line in open('cmudict.txt').readlines():
        if not line or line.startswith(';;;'):
            continue
        word, pron = line.split('  ')
        primary = True
        if word.endswith(')'):
            primary = False
            word = word[:-3]
        word = word.lower().replace('_', ' ')
        pron = pron.strip()
        sound = re.sub(r'\d', '', pron)
        meter = re.sub(r'\D', '', pron).replace('2', '1')
        if primary:
            db['sound'][word] = sound
            db['meter'][word] = meter
        else:
            db['altsound'].setdefault(word, []).append(sound)
            db['altmeter'].setdefault(word, [])
            if (meter != db['meter'][word] and
                meter not in db['altmeter'][word]):
                db['altmeter'][word].append(meter)
        db['mets'].setdefault(meter, set()).add(word)
        db['sibs'].setdefault(len(meter), set()).add(word)
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
                db['lex2word'].setdefault(lex, set()).add(word)
                db['word2lex'].setdefault(word, set()).add(lex)
                if wtype == 'r':
                    db['adverbs'].add(word)
                elif wtype == 'n':
                    db['nouns'].add(word)
                elif wtype in ('a', 's'):
                    db['adjectives'].add(word)
                elif wtype == 'v':
                    db['verbs'].add(word)

    print 'marshaling...'
    marshal.dump(db, open('db.marshal', 'w'))
