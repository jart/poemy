# poemy

poemy will soon be a poetry generator, written in the Python programming
language.

This project was started August 24th, 2012 by Justine Tunney and is still in
its infantile stages of development. But once poemy is finished, it will be
the greatest poetry generator there ever was or ever will be.

Why will poemy be so awesome? Because it'll be able to generate poetry from a
100k+ word dictionary with:

- **Any rhyming scheme**: like couplets, abab,
  [acab](http://en.wikipedia.org/wiki/A.C.A.B.), etc. It'll also be able to do
  feminine rhymes and repeat similar consonants for alliteration.
- **Any meter or rhythm**: like iambic pentameter, trochaic tetrameter,
  anapestic trimeter, etc.
- **Any style**. Poemy will be trained to be capable of picking words and
  sentence structures from various historical and contemporary styles. You
  want a Shakespearean sonnet? You got it. Some dark melancholic goth music
  lyrics? No problem.

What's the catch? The poems won't make any sense. But that doesn't matter
because poetry doesn't have to make sense! But even if you impute poor poemy
for not being able to carry a cohesive thought, you'll still appreciate the
beauty of the words it writes.

poemy will only be able to write poetry in English. There are absolutely no
plans or preparations to support other languages.

## Running

    python load.py goth
    python info.py markov

## Example Poem

This poem was generated from the goth corpus in iambic pentameter using a
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
