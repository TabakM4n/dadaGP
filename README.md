# DadaGP

[**Paper**](https://archives.ismir.net/ismir2021/paper/000076.pdf) | [**Generation Results**](https://drive.google.com/drive/folders/1USNH8olG9uy6vodslM3iXInBT725zult?usp=sharing) | [**ISMIR Poster**](https://s3.eu-west-1.amazonaws.com/production-main-contentbucket52d4b12c-1x4mwd6yn8qjn/8ed232c2-bcce-46aa-a735-d24b865644ef.pdf) 

DadaGP is:

* a dataset of 26,181 GuitarPro songs in 739 genres, converted to a token sequence format suitable for generative language models like GPT2, TransformerXL, etc.
* an encoder/decoder (v1.1) that converts gp3, gp4, gp5 files to/from this token format.

*Please contact Dadabots or Pedro Sarmento via email or twitter, [@dadabots](http://twitter.com/dadabots) / [@umpedronosapato](https://twitter.com/umpedronosapato), to request access to the dataset for research purposes.*

## Usage

#### Requirements

* python3
* PyGuitarPro 0.6 *(it ONLY works with 0.6 -- if you're using a newer version, install 0.6 in a virtual environment to run dadagp.py)*
```
pip install 'PyGuitarPro==0.6'
```

#### ENCODE (guitar pro --> tokens)
```
python dadagp.py encode input.gp3 output.txt [artist_name]
python dadagp.py encode examples/progmetal.gp3 progmetal.tokens.txt unknown
```

#### DECODE (tokens --> guitar pro)
```
python dadagp.py decode input.txt output.gp5
python dadagp.py decode progmetal.tokens.txt progmetal.decoded.gp5
```

Note:
* only gp3, gp4, gp5 files are supported by the encoder;
* rare combinations of instruments and tunings may not be supported;
* banjo is not supported;
* instrument-change events are not supported;

---

## Metal Extensions (branch: `metal-extensions`)

This fork extends DadaGP v1.1 with five features for metal songwriting pipelines. All extensions are **backward-compatible** — original DadaGP token files decode without changes.

### 1. Section Label Tokens

Guitar Pro rehearsal marks (Intro, Verse, Chorus, etc.) are preserved as `[SECTION:name]` tokens emitted at the start of each marked measure:

```
new_measure
[SECTION:Chorus]
distorted0:note:s4:f0
...
```

During decode, these tokens recreate GP rehearsal marks at the correct bar positions, restoring full song structure in the decoded GP5.

### 2. 5-String Drop D Bass Tuning Support

Adds support for 5-string Drop D bass: **A1-D2-A2-D3-G3** (MIDI: 33-38-45-50-55), tuning type `b5_drop`. Previously only 4-string drop D was supported for drop-tuned basses.

The lowest string (Drop D) is encoded as frets `-1`/`-2` per the standard DadaGP drop convention.

### 3. Bass Octave Decode Fix

Basses tuned at a non-standard octave relative to the global pitch shift (e.g., a 5-string drop D played an octave higher than the b5_drop template) were previously decoded 12-14 semitones out of register.

The encoder now emits a `[BASS_OFFSET:N]` metadata token recording the octave difference. The decoder applies this offset when reconstructing bass string tuning, producing a GP5 with the correct playback register.

### 4. Track Name Preservation

GP track names are preserved via `[TRACK_NAME:prefix:name]` tokens inserted after `start`:

```
start
[TRACK_NAME:distorted0:Guitar 1 (TabakMan)]
[TRACK_NAME:distorted1:Guitar 2 (Koce)]
[TRACK_NAME:bass:Bass (Kris)]
[TRACK_NAME:drums:Drums (Dimitar)]
new_measure
...
```

The decoder restores original track names instead of generic defaults like "Guitar", "Bass", "Drums".

### 5. Song Metadata Tokens

Song-level metadata is captured at the beginning of the token file, before the artist/downtune/tempo/start sequence:

```
[TITLE:Hollow Ground]
[ARTIST:Broken]
[BPM:94]
[BASS_OFFSET:12]
Broken
downtune:0
tempo:90
start
...
```

`[TITLE:]`, `[ARTIST:]`, and the exact (non-rounded) `[BPM:]` tempo are restored in the decoded GP5. `[BASS_OFFSET:]` is only emitted when the bass octave differs from standard.

### New Token Reference

| Token | Placement | Description |
|-------|-----------|-------------|
| `[TITLE:name]` | File header | Song title from GP metadata |
| `[ARTIST:name]` | File header | Artist name |
| `[BPM:N]` | File header | Exact source tempo (unrounded) |
| `[BASS_OFFSET:N]` | File header | Bass octave correction offset |
| `[TRACK_NAME:prefix:name]` | After `start` | Original GP track name per instrument |
| `[SECTION:name]` | After `new_measure` | Section/rehearsal mark from GP score |

---

## How to Cite
```
@inproceedings{dadagp2021,
  author = {Sarmento, Pedro and Kumar, Adarsh and Carr, CJ and Zukowski, Zack and Barthet, Mathieu and Yang, Yi-Hsuan},
  booktitle = {Proceedings of the 22nd International Society for Music Information Retrieval Conference},
  title = {{DadaGP: a Dataset of Tokenized GuitarPro Songs for Sequence Models}},
  url = {https://archives.ismir.net/ismir2021/paper/000076.pdf},
  year = {2021}
}
