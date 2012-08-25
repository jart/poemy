import sys

import poemy


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
