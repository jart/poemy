import re
import sys
import random

import poemy


class Exhausted(Exception):
    pass


@poemy.memoize
def firstwords():
    words = poemy.db.chain.keys()
    words.sort(key=lambda w: len(w[0] + w[1]), reverse=True)
    return words


def pick(words, opts):
    return random.randrange(int(round(len(words) * opts['bigwords'])))


def mkword(w1, w2, meter, rhyme, opts):
    if not meter:
        if w2 in poemy.badendwords:
            raise Exhausted()
        if rhyme:
            if w2 == rhyme:
                raise Exhausted()
            if not poemy.is_rhyme(w2, rhyme):
                raise Exhausted()
        return []
    words = poemy.db.chain.get((w1, w2), [])[:]
    if len(words) < opts['originality']:
        raise Exhausted()
    for n in range(opts['tries']):
        if not words:
            break
        w3 = words.pop(pick(words, opts))
        if w3 not in poemy.db.sounds:
            continue
        wcm = poemy.wordcompatmeter(meter, w3)
        if wcm is None:
            continue
        try:
            return [w3] + mkword(w2, w3, meter[len(wcm):], rhyme, opts)
        except Exhausted:
            pass
    raise Exhausted()


def mkline(meter, rhyme, **opts):
    opts.setdefault('tries', 20)
    opts.setdefault('originality', 1)
    opts.setdefault('bigwords', 0.7)
    words = firstwords()
    for n in xrange(opts['tries']):
        w1, w2 = words[pick(words, opts)]
        if w1 not in poemy.db.sounds or w2 not in poemy.db.sounds:
            continue
        if w1 in poemy.badstartwords:
            continue
        wcm = poemy.wordcompatmeter(meter, w1, w2)
        if wcm is None:
            continue
        try:
            return [w1, w2] + mkword(w1, w2, meter[len(wcm):], rhyme, opts)
        except Exhausted:
            pass
    raise Exhausted()


if __name__ == '__main__':
    # tool for comparing syllables for rhyming
    # python info.py rhyme cacophony aristophanes rolling controlling
    #       cacophony              (K) AE K      AA F      AH N      IY        
    #    aristophanes        AE R      AH S T    AO F      AH N      IY Z      
    #         rolling                                  (R) OW L      IH NG     
    #     controlling                        (K) AH N T R  OW L      IH NG     
    if sys.argv[1] == 'rhyme':
        longest = 0
        for word in sys.argv[2:]:
            for sound in poemy.wordsounds(word):
                onset, syls = poemy.soundparts(sound)
                longest = max(longest, len(syls))
        for word in sys.argv[2:]:
            for sound in poemy.wordsounds(word):
                onset, syls = poemy.soundparts(sound)
                line = "%15s" % (word)
                line += " " * ((longest - len(syls)) * 10)
                line += "%10s " % ("(" + onset + ")" if onset else "")
                for syl in syls:
                    line += "%-10s" % (syl)
                print line.rstrip()
                word = ''

    # generate some poetry using markov chains
    if sys.argv[1] == 'markov':
        # for n in range(14):
        #     print ' '.join(mkline('001' * 3))
        n = 0
        while True:
            # 01     - iambic
            # 10     - trochaic
            # 001    - anapestic
            # 100    - dactylic
            # 010    - amphibrachic
            # 11     - a spondee foot
            # 00     - a pyrrhic foot
            # 1 foot - monometer
            # 2 feet - dimeter
            # 3 feet - trimeter
            # 4 feet - tetrameter
            # 5 feet - pentameter
            # 6 feet - hexameter
            # 7 feet - heptameter
            try:
                m = '10' * 5
                l1 = mkline(m, None)
                l2 = mkline(m, l1[-1])
            except Exhausted:
                continue
            # print ' '.join(l1) + ', ' + ' '.join(l2)
            print ' '.join(l1)
            print ' '.join(l2)
            n += 1
            if n == 10:
                break

    # analyze the meter of a poem from stdin
    if sys.argv[1] == 'analyze':
        for line in sys.stdin.readlines():
            line = line.strip().lower()
            if not line:
                continue
            line = re.sub(r"[^-'a-z]", r' ', line)
            line = line.split()
            print ' '.join(line)
            out = [[], []]
            syls = 0
            for word in line:
                for j in range(len(out)):
                    try:
                        meter = list(poemy.wordmeters(word))[j]
                    except KeyError:
                        word2 = ['!' for n in range(len(word))]
                    except IndexError:
                        word2 = [' ' for n in range(len(word))]
                    else:
                        if j == 0:
                            syls += len(meter)
                        word2 = [' ' for n in range(len(word))]
                        for n in range(len(meter)):
                            word2[len(word) / len(meter) * n] = meter[n]
                    out[j].append(''.join(word2))
            out[0] += ["(%d syllables)" % (syls)]
            for l in out:
                print ' '.join(l)

    # tells you which words from specified corpora are missing and how often
    # they appeared
    if sys.argv[1] == 'missing':
        def words():
            for corpus in sys.argv[2:]:
                for word in poemy.corpuswords(corpus):
                    if word not in poemy.db.cmudict:
                        yield word
        tbl = {}
        for word in words():
            tbl.setdefault(word, 0)
            tbl[word] += 1
        tbl = [(w, c) for w, c in tbl.iteritems()]
        tbl.sort(key=lambda v: v[1])
        for word, count in tbl:
            print "%-15s %d" % (word, count)

    # what is the probability of each vowel being the stressed syllable?
    if sys.argv[1] == 'vowel-stress-probability':
        phonemes = {}
        for w in (poemy.db.syl2words[2] |
                  poemy.db.syl2words[3] |
                  poemy.db.syl2words[4] |
                  poemy.db.syl2words[5] |
                  poemy.db.syl2words[6]):
            for ps in poemy.db.cmudict.get(w, []):
                for p in ps.split():
                    if p.endswith(('0', '1')):
                        phonemes.setdefault(p, 0.0)
                        phonemes[p] += 1.0
        res = []
        for v in poemy.vowels:
            p = phonemes[v + '1'] / (phonemes[v + '0'] + phonemes[v + '1'])
            res.append((v, p))
        res.sort(key=lambda v: v[1])
        for v, p in res:
            print "%s %.5f" % (v, p)

    # same thing, but we include the following consonant
    if sys.argv[1] == 'syllable-stress-probability':
        phonemes = {}
        doodles = set()
        for w in (poemy.db.syl2words[2] |
                  poemy.db.syl2words[3] |
                  poemy.db.syl2words[4] |
                  poemy.db.syl2words[5] |
                  poemy.db.syl2words[6]):
            if w not in poemy.db.sounds:
                continue
            ss = poemy.db.sounds[w][0]
            ms = poemy.db.meters[w][0]
            for s, m in zip(poemy.soundparts(ss)[1], ms):
                phonemes.setdefault((s, int(m)), 0.0)
                phonemes[s, int(m)] += 1.0
                doodles.add(s)
        res = []
        for s in doodles:
            try:
                p = phonemes[s, 1] / (phonemes[s, 0] + phonemes[s, 1])
                t = phonemes[s, 0] + phonemes[s, 1]
                res.append((s, p, t))
            except KeyError:
                pass
        res.sort(key=lambda v: v[0])
        for s, p, t in res:
            print "%-10s %.5f (%d)" % (s, p, t)
