# Core Keeper Custom Music Player

Python-based script that allows for custom music to be played with the instruments within Core Keeper.

## Features

- Syntax for musical notation by text
- Automatic note length calculation by tempo (BPM)
- Separate files for storing songs
- Playing multiple song texts at the same time via multithreading (but this is really not great, can't recommend it, but it's there)

## Why?

Because I'm bad at playing the instruments. Realistically, it would've been less effort to actually practice playing the instruments well instead of writing this script, but I thought it'd be a fun project. I don't have much experience with parsing syntax, other than miscellaneous exercises in university. This can probably be seen in how I've implemented it... But it also serves as practice towards that.

## Instructions for use

### Basic requirements

- Python 3.12+
  - I'm fairly certain most of the features I'm using are present in older versions, but use them at your own risk

Probably nothing else.

### Usage

Install the requirements:

```
pip install -r requirements.txt
```

Run the script from your terminal with

```
py cksheetmusic.py
```

This will print out instructions for selecting songs.

## Creating your own songs

Songs are saved in .cksp files. They're effectively text files, but the script will only recognize .cksp files. <br/>
The file is formatted as: <br/>

```
Song name
Tempo
{
  song text 1
}
{
  song text 2
}
...
```

One song text is required, and adding more is optional. <br/>[Example file](./songs/songofstorms.cksp) (Song of Storms)

I've included 2 example songs in [The songs folder](./songs)

### Song text syntax

|             | Description                                                                                                           |
| ----------- | --------------------------------------------------------------------------------------------------------------------- |
| `key`       | Key to be pressed to play a quarter note                                                                              |
| `[key<n>]`  | Key to be pressed to play a note of _n_:th length                                                                     |
| `(keys)`    | Keys to be pressed to play as beamed notes <br/> Number of brackets determines note length; () = 8th, (()) = 16th     |
| `{keys<n>}` | Keys to be pressed simultaneously <br/> _n_ is optional; defaults to quarter notes if n is not present                |
| `-`         | Pause note; can be used identically to regular keys                                                                   |
| `<key>.`    | Dotted note marker <br/> Modifies the note to be played as a [dotted note](https://en.wikipedia.org/wiki/Dotted_note) |
| `<key>:`    | Staccato marker <br/> Modifies the note to be played as [Staccato](https://en.wikipedia.org/wiki/Staccato)            |
| `\|`        | _Optional:_ Measure separator <br/> Only serves as an aid when writing song texts, and does nothing to the end result |

### Example song text

`((2m))[28:][28:]((m2))[w8:][m8:]2|((2m2w))[28:][n8:][c8:]-`

<br/>

`((2m))` plays the keys _2_ and _m_ as beamed 16th notes. () = 8th, (()) = 16th, ...
<br/>

`[28:]` plays _2_ as an 8th note with staccato, resulting in 2 as 16th, pause as 16th = 8th note in length. This structure repeats quite often.
<br/>

`2` plays _2_ as a normal quarter note
<br/>

`|` indicates a measure separator, placed as an aid for writing the text. No effect on the outcome.
<br/>

`-` creates a pause of quarter note length

### Other example uses

`[y32]` plays _y_ as a 32th note
<br/>

`{bm}` plays _b_ and _m_ simultaneously as quarter notes
<br/>

`{vn[2]}` plays _v_ and _n_ simultaneously as half notes. **NOTE**: This structure of a sole number within `[]` is only available to use with simultaneous notes to determine their length.
<br/>

### Credits

- [Pugstorm](https://pugstorm.eu/) for creating Core Keeper!
- [SomePianoMusicDude33](https://musescore.com/user/20360426) for the Song of Storms sheet music
- [krowft](https://musescore.com/user/31400576) for the Sea Shanty 2 sheet music
