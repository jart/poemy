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

- **Any meter**: Poemy can break words into syllables and knows which ones are
  stressed. Poemy can also predict with good accuracy whether or not a single
  syllable word will be stressed in a sentence. This allows it to write poetry
  in iambic pentameter, trochaic tetrameter, anapestic trimeter, etc.

- **Any rhythm**. Poemy is able to distinguish between long and short sounding
  consonants. For example: "Cat attack galore" follows the rhythm "sssll" (s =
  short, l = long).

- **Any style**. Poemy can be trained in various historical and contemporary
  styles. You want a Shakespearean sonnet? You got it. Some dark melancholic
  goth music lyrics? No problem.

- **Alliteration**. Poemy will be able to ensure that particular or similar
  consonants are repeated. It can also repeat vowels for assonance. It can
  place these phonemes in a rigid syllable meter or use probabilistic
  placement throughout a line. It can also make tongue-twisters!

What's the catch? The poems won't make any sense. But that doesn't matter
because poetry doesn't have to make sense! But even if you impute poor poemy
for not being able to carry a cohesive thought, you'll still appreciate the
beauty of the words it writes.

poemy will only be able to write poetry in English. There are absolutely no
plans or preparations to support other languages.

## Running

    sudo make apt-get-stuff-you-need
    make
    python load.py goth
    python info.py markov

## Example Poems

Even though poemy is still in the experimental proof of concept stage, it
still writes poetry better than most humans. Take for instance this poem which
was generated from the goth corpus (included with poemy) in iambic pentameter
using a masculine couplet rhyming scheme. What you see below was generated
*verbatim*; the only thing I changed was I added punctuation and removed two
lines that ripped off Edgar Allan Poe too heavily.

> We're lost in this cruel place your voice above  
> Young soul from out my heart be still in love  
> Worth this cruel place your voice from the deep snow  
> That this is the night of the world so slow  
> Will leave me as my hopes have flown before  
> Which answered not with a love that was more  
> I'm sitting in this kingdom by the grave  
> Your clothes by your voice at the stillness gave  
> She's gone to the floor floating on our side  
> She speaks in the earth and the truth inside  
> Have naught but the pain you feel the bright eyes  
> Beyond the waves wipe out my heart denies  
> Your voice from the laugh of the desolate  
> You're looking for the moon is full of hate  
> Forgive if I could change the time has come  
> We're lost in this world is not like a drum  
> Earth and the stillness broken by reply  
> Through the night tide I lie down in the sky  
> Beyond the waves wipe out the joyous light  
> And dancing in the power of the night  
> Want things to go before it is too late  
> Night tide I lie here in this world of hate  
> Away like the mist of the desolate  
> I'll show you all the world is full of hate  
> Pretend that I forgot who I was blind  
> Fall just to see the light in my own mind  
> Leave leave me as my hopes have flown before  
> Your clothes by your voice from the nightly shore  
> The london bridge is falling down my heart  
> Die! Please hang up now; I take it apart!  
> That's happened to my thoughts which help to note  
> Forever live on the earth and the boat  
> Whose name is on the ground and kiss those black  
> Melts into the deep of the faces back  
> Might have seen the end, you will understand  
> That's why I feel what I want my own land  
> Dear tokens of the saintly days abhor  
> Break all the night for me behind the door

This poem uses the same scheme but it was trained by the Shakespeare sonnet
corpus. This time I generated two poems, one with a preference towards large
words, the other for short words, and then I just sort of merged the lines
together haphazardly.

> O if I should despair I should despair  
> Lov'd I view in thee it is my love's fair  
> It no form of thee that the thought of hearts  
> But let your love and love that in thy parts  
> Assistance in my love's sweet face survey  
> Breathes even in the bay where all the day  
> Though absence seem'd my flame to qualify  
> Came tripping by but in the world must die  
> Translated and for that which flies before  
> Believe though in thy heart in love to score  
> Perfect'st love being made from thee I speed  
> Came tripping by but in my heart doth plead  
> On whom frown'st thou that which doth in it live  
> Phrase by all the world that I do forgive  
> Applying fears to hopes and hopes to fears  
> Believe though in thy glass and there appears  
> Mouthed graves will give thee so thine own bright eyes  
> Deliver'd from thy heart in love with sighs  
> Thee when I shall live your self but love hate  
> O no thy love though much is not so great  
> Time's leisure with my love's sweet face survey  
> Deliver'd from thy heart which I new pay  
> Friend's heart let my heart think that we before  
> Consum'd with that which is not love thee more  
> Remember'd not to love things nothing worth  
> Conceal'd wherein I am that I in earth  
> This to thee which thou hast passed by the height  
> As I think on thee when I in my sight  
> Thou shouldst print more not let that copy die  
> Still farther off from thee I both defy  
> Mine appetite I never more will grind  
> Believe though in my love that doth my mind  
> Contented when that mine eye may be straight  
> Return rebuk'd to my thoughts and my great  
> Where wasteful time debateth with decay  
> What conscience is born of love if I say  
> Those children nursed deliver'd from thy friend  
> Perfect'st love being made from thee I send  
> Eternal summer shall not be thy chief  
> Believe though in my love and all my grief  
> Breathes even in the world's due by the height  
> Believe though in my heart thy picture's sight  
> Love put in my thought whose love to hear why  
> Make my love thou my love that keeps mine eye  
> Thou shouldst print more not let that copy die  
> Deliver'd from thy walks and in the eye  
> And strangely but by all the better part  
> Thou stick'st not to love that thou shouldst depart  
> Increasing store with loss and loss with store  
> Return rebuk'd to my dear love to score  
> This separation I may change my state  
> Supposing thou art and that thou dost hate  
> At my abuses reckon up their own  
> What's in the world that I will not be shown  
> Soul that I cannot blame thee for her sake  
> Yet love knows it is but as the waves make  
> Deaf heaven with my love's sweet face survey  
> To play the tyrants to the world away  
> Bears it out even to the ending doom  
> Wait on thee in the world will be the tomb  
> Not on thy heart torment me with disdain  
> You live your epitaph to make one twain  
> Than theirs less false in this change is my heart's  
> Reigns love and all my soul which in thy parts  
> Might I from my love's picture then my friend's  
> That thou hast her it is my love depends  
> To show false art what beauty was of yore  
> Save where thou dost seek to have thy love more  
> The lack of many lives upon his gains  
> Him I lose thee my loss is my love's veins  
> This fair gift in me that you should prepare  
> Cheeks need blood in thee it is my love's fair  
> Most I wink then do mine eyes out of sight  
> If thou wilt thou art all the day or night  
> Thief whence didst thou steal thee all my grief lies  
> As you to love that in my heart and eyes  
> Dead there's no more be griev'd at that which flies  
> Home of love to thee but what they despise  

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
