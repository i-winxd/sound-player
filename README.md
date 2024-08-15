# Sound Player

A Python GUI application that lets you quickly play sounds in a folder. Really useful if you have a folder full of sound
effects and want to quickly go through them. The feel of this is very similar to how FL Studio's file explorer on the
left sidebar works.

![image](https://github.com/i-winxd/sound-player/assets/31808925/6829df31-b171-4e5c-ac5d-bb5803dac058)


## Installation

You can go to the releases tab and download the executable there.

Alternatively, if you don't trust executable files, then:

Any version of Python 3.9 or later works. Download it off the [Python website](https://python.org/). When installing, be sure to check `Add Python to PATH`. You will also need `pygame`. Install it by
running `python -m pip install pygame`

Note that macOS users and Linux users may have to sub all `python` commands with `python3`.

## Running

Using command prompt, `cd` to this folder, and run `python main.py`. For Windows users, you can quickly open the command prompt **focused** at a folder by typing `cmd` in the search bar of the folder you are targeting, in file explorer.

## Usage

- `Select folder`: Select the folder. All audio files in that folder (not subdirectories) will then appear in the list below.
- `Open selected`: Open file explorer focused to the file you have selected in the list below. If you don't have a file selected, this does nothing.
- `Stop`: Stop any playing audio. Does nothing if nothing is playing.
- The slider: That's the volume.
