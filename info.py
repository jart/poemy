import re
import sys
import random

import poemy


class Exhausted(Exception):
    pass


@poemy.memoize
def get_firstwords():
    firstwords = poemy.db.chain.keys()
    firstwords.sort(key=lambda w: len(w[0] + w[1]), reverse=True)
    return firstwords


def mkword(w1, w2, meter, rhyme):
    if not meter:
        if w2 in poemy.badendwords:
            raise Exhausted()
        if rhyme:
            if w2 == rhyme:
                raise Exhausted()
            if not poemy.is_rhyme(w2, rhyme):
                raise Exhausted()
        return []
    nextwords = poemy.db.chain.get((w1, w2), [])[:]
    while nextwords:
        w3 = nextwords.pop(random.randrange(max(len(nextwords) / 8, 1)))
        if w3 not in poemy.db.sounds:
            continue
        wcm = poemy.wordcompatmeter(meter, w3)
        if wcm is None:
            continue
        try:
            return [w3] + mkword(w2, w3, meter[len(wcm):], rhyme)
        except Exhausted:
            pass
    raise Exhausted()


def mkline(meter, rhyme):
    firstwords = get_firstwords()[:]
    n = 0
    while firstwords and n < 10:
        n += 1
        w1, w2 = firstwords.pop(random.randrange(max(len(firstwords) / 4, 1)))
        if w1 not in poemy.db.sounds or w2 not in poemy.db.sounds:
            continue
        if w1 in poemy.badstartwords:
            continue
        wcm = poemy.wordcompatmeter(meter, w1, w2)
        if wcm is None:
            continue
        try:
            return [w1, w2] + mkword(w1, w2, meter[len(wcm):], rhyme)
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
            try:
                l1 = mkline('0101010101', None)
                l2 = mkline('0101010101', l1[-1])
            except Exhausted:
                continue
            # print ' '.join(l1) + ', ' + ' '.join(l2)
            print ' '.join(l1)
            print ' '.join(l2)
            n += 1
            if n == 20:
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
