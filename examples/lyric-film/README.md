# Full lyric film

[Back to the showcase](../../README.md#showcase) · [Watch the original video](https://github.com/lbframe/animation-studio/releases/download/v0.1.0/lyric-film.mp4)

![Animation preview](../../docs/assets/showcase/lyric-film/preview.gif)

The chorus concept extends across the complete song, with revised word onsets and a short sequence of end-credit cards.

## Showcase render

| Input | Output | Method |
| --- | --- | --- |
| Song audio, supplied lyrics, mouth-pose reference, and corrected SRT timings | 184.9 seconds · 1080 × 1080 · 30 fps · audio | HyperFrames 0.9.17, GSAP, and Canvas; FFmpeg assembly for the credit revision |

The selected export is **V3** of **I Want the Mondays Too**. It retains the revised lyric and mouth animation before **2:51**, then introduces end credits without extending the original duration.

## Original request — English translation

> Take this audio reference and use the lip-sync reference image from earlier. Make a music video that synchronizes the mouth with the lyrics, with the words coming out of the mouth in a karaoke-like kinetic typography motion design style. I suggest showing me the chorus first before doing the whole song. Make the video square, in a 1:1 format.

## Important follow-ups — English translations

The chorus was approved before the project expanded to the whole song:

> Yes, I approve.

The user then supplied subtitle timing and requested corrections:

> Does this file help once you have cleaned it up and replaced the misspelled or misheard words using the official lyrics?

> I mostly noticed offsets at the beginnings of words, so I think using this file will help you fix those issues. Go!

The final revision added end credits:

> After 2:51, can you add end credits that follow cinema industry standards? Can you prepare them here and ask me for the role for each entry?

> Nobody reads the credits anyway, so they can be fast; don't overthink it.

The user also clarified that the special thanks should say **“putting up with me every day.”** The approved wording and credit names are recorded in the source project's `credits.json`.

## Recommended prompt

Provide the approved chorus study, full song, exact lyrics, subtitle timings, mouth reference, and approved credit list, then paste:

```text
Use $create-animation to extend the approved chorus study into the full
square lyric film. Preserve its mouth artwork, warm paper palette,
typography, and lyric-emission treatment. Deliver 1080 × 1080 at 30 fps
with the original song audio and the original 184.9-second duration.

Correct misspelled or misheard subtitle words against the supplied exact
lyrics. Use the corrected timings and audio to refine word onsets, then
align the lyric entrances and mouth articulation to the revised timing.
Keep phrases readable and make handoffs clean.

At 2:51, transition into concise cinema-style end credits using the
approved credit list exactly. Use a brisk sequence of four restrained
black-and-white cards. Preserve the corrected animation before 2:51
and keep the audio continuous through the ending.

Deliver the full MP4, editable project, and corrected SRT. Inspect word
onsets, phrase transitions, the cut into credits, and every credit card.
Report what was checked and any remaining synchronization limits.
```

This is a continuation prompt for an approved study. The timing fixes, credit start, brisk pace, and credit wording come from the follow-up requests. The four-card structure and exact output settings reflect the delivered revision.

## Recorded credits

| Role | Credit |
| --- | --- |
| Production | SEXYMOUTH PRODUCTION |
| Direction, animation, kinetic typography, and editing | Animation Studio |
| Art direction | GPT 6.1 Sol |
| Lyrics | Leonardo Balland · x.com/leonardoballand |
| Music, vocals, mixing, and mastering | Suno v6 Pro |
| Copyright | © 2026 SEXYMOUTH PRODUCTION |

The art-direction note reads: “He put in a lot of effort. High effort, literally.”

The final special thanks read:

> Thanks to my big, lovely team of AI agents for putting up with me every day. Some are smarter than others, but they all deserve my gratitude. Let’s cook together!

## Source and review notes

The original project includes the full composition, alignment data, corrected lyrics, corrected SRT, credit data, fonts with their license files, mouth artwork, lossless audio, and render settings. The delivered V3 joins the previously rendered opening to a new credit tail; the complete editable project is also included in the original source package.

The source review records unchanged decoded frames before 2:51 and unchanged audio packets relative to V2, plus inspection of credit frames and layout. Continuous audiovisual listening was not certified. The credit content was approved; the package does not record a separate final approval of the encoded V3 export.

The recommended prompt was written after this render. It is an editorial adaptation of the original request and follow-ups, and has not been rerun to certify an identical result.
