# pyadventureboard :sound: :notes:
A little soundboard/light/something system that lets you use it as a meme machine gun or use it as helper to get a quick mix.

Forked from pysoundboard
[https://github.com/lombartec/pysoundboard](https://github.com/lombartec/pysoundboard)

Still a rough work in prorgress

## Features
- Playing sounds (don't you say!).
- Loop sounds.
- Stop everything that is playing.
- Profiles.
- Auto populating of keys

## Set up
- Install requirements
  - `pip install -r requirements`
  - Put your profiles in place
    - Create a folder with name `q` then paste audio files
    - Example: `profiles/q/funnynoise.mp3`
    - Sounds will be auto assigned for letters qwe asd zxcv
  - Run `./Soundboard.py`

## Key bindings
#### Everything is controlled from the numpad!
- To play a sound press the key assigned to it (qwe asd zxcv)
- To loop a sound hold multiply key (3) and press the number assigned to it.
  - To stop looping the sound just play it again pressing they key assigned to it.
- To switch to another profile hold the divide key (2) and press the number assigned to the profile.
- To stop all sounds that are playing press the spacebar
