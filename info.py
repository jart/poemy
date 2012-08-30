import sys
import random

import poemy


def mkline(originality=7, nonrepetitiveness=2, syllables=10, rhythm='01' * 5):
    while True:
        try:
            rim = rhythm
            vary = 0
            w1, w2 = random.choice(poemy.db.chain.keys())
            line = [w1, w2]
            while len(line) < 10:
                words = poemy.db.chain[(w1, w2)]
                # ones = set(w for w in words if w in poemy.db.mets['1'])
                # words = set(w for w in words if w in happy and not in ones)
                vary += len(words)
                w1, w2 = w2, random.choice(words)
                line.append(w2)
        except KeyError:
            pass
        if len(line) < 8:
            continue
        if vary < len(line) * originality:
            continue
        if len(set(line)) <= len(line) / nonrepetitiveness:
            continue
        return line


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

    if sys.argv[1] == 'meter':
        for word in sys.argv[2:]:
            for meter in poemy.wordmeter(word, full=True):
                line = "%15s" % (word)
                line += "%10s" % (meter)
                print line
                word = ''

    if sys.argv[1] == 'markov':
        out = 0
        while True:
            l1, l2 = mkline(), mkline()
            if (l1[-1] != l2[-1] and
                l1[-1] not in poemy.stopwords and
                l2[-1] not in poemy.stopwords and
                poemy.is_rhyme(l1[-1], l2[-1])):
                print ' '.join(l1)
                print ' '.join(l2)
                out += 2
                if out == 10:
                    break
