# poemy

poemy will soon be a poetry generator, written in the Python programming
language.

This project was started August 24th, 2012 by Justine Tunney and is still in
its infantile stages of development. But once poemy is finished, it will be
the greatest poetry generator there ever was or ever will be.

Why will poemy be so awesome? Because it'll be able to generate poetry from a
100k+ word dictionary with:

- **Any rhyming scheme**: like couplets, abab,
  [acab](http://en.wikipedia.org/wiki/A.C.A.B.), etc. Poemy knows how almost
  every word in the english language is pronounced and is able to distinguish
  between 15 vowel and 24 consonant phonemes. This means it knows "th**ee**"
  and "atrocit**y**" rhyme but "**one**" and "b**one**" don't. Poemy also
  takes into consideration how some words can be pronounced in different
  ways. The rhyming algorithm considers two words as rhyming if the last vowel
  and subsequent consonant phonemes match. Poemy can also do feminine rhymes!

- **Any meter**: Poemy knows which syllables are stressed in each word. Poemy
  can also predict with good accuracy whether or not a single syllable word
  will be stressed in a sentence. This means it can write poetry in iambic
  pentameter, trochaic tetrameter, anapestic trimeter, etc.

- **Any rhythm**. Poemy is able to distinguish between long and short sounding
  consonants. For example: "Cat attack galore" follows the rhyming scheme
  "sssll" (s = short, l = long).

- **Any style**. Poemy can be trained in various historical and contemporary
  styles. You want a Shakespearean sonnet? You got it. Some dark melancholic
  goth music lyrics? No problem.

- **Alliteration**. Poemy will be able to ensure that particular or similar
  consonants are repeated. It can also repeat vowels for assonance. It can
  place these phonemes in a rigid syllable meter or use probabilistic
  placement throughout a line.

What's the catch? The poems won't make any sense. But that doesn't matter
because poetry doesn't have to make sense! But even if you impute poor poemy
for not being able to carry a cohesive thought, you'll still appreciate the
beauty of the words it writes.

poemy will only be able to write poetry in English. There are absolutely no
plans or preparations to support other languages.

## Running

    python load.py goth
    python info.py markov

## Example Poems

This poem was generated from the gothic corpus in iambic pentameter using a
masculine couplet rhyming scheme:

> we really have to plug my eyes before  
> black angel i feel hunger for the shore  
> which answered not with a caress he died  
> shone for me to the lake of the night tide  
> with sadness here i opened wide the door  
> that scream i hear the angels name lenore  
> i'll show you all the seeming of a trend  
> no reason for you and i don't pretend  
> young soul from the laugh of the desolate  
> your mouth by your voice in my world of hate  
> from those brown hills have melted into spring  
> and dancing in the power of the thing

Here's an iambic pentameter couplet poem trained by Shakespeare's sonnets:

> than public means which public manners breeds  
> the judgment of my love that in thy deeds  
> be nothing new but that which flies before  
> stirr'd by a painted beauty to his store  
> friend's heart let my heart think that we before  
> remov'd that hidden in thee is of more  
> as objects to his palate doth prepare  
> clouds o'ertake me in my love as rare  
> pursuit of the world that i cannot blame  
> thus vainly thinking that she hath no name

Here's another iambic pentameter couplet poem trained by the book War and
Peace with a preference towards big words:

> natasha brightened up and disappeared  
> expressed approval and not once appeared  
> without restraining her sobs that were brought  
> concealed depression on the russians thought  
> more extraordinary in that plight  
> convince themselves by the thought could not quite  
> restrain themselves and mounted on black roan  
> direct participation of the cone  
> great disappointment like a suffering child  
> prepared provisions for the princess smiled

## Volunteers

I need your help to make poemy awesome!

1. Programming. If you know how to code, feel free to start hacking and send
me pull requests.

2. Corpus assembly. I need people who can help me collect poems in text file
format and categorize them by style.

3. Word pronunciation. Poemy has to know how every word is pronounced and
which syllables are emphasized, but many of the words in the corpora aren't
defined in `data/cmudict.txt` :( I need people to help me add entries to
cmudict that look like this: `TWISTED  T W IH1 S T AH0 D`.

If you're interested, send me a message on Github or email
<jtunney@lobstertech.com>.

## Copyright

Copright (c) 2012 Justine Tunney  
Licensed under the AGPL v3 or later
