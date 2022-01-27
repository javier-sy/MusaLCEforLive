# Musa Live Coding Environment for Ableton Live

**Ableton Live Controller for Musa Live Coding Environment.**

This project is part of **Musa Live Coding Environment**.

Musa Live Coding Environment is a suite of components to add a live coding environment based on [Musa-DSL](https://github.com/javier-sy/musa-dsl) to several DAW's (Ableton Live 11 or higher and Bitwig Studio 4 or higher, for the moment).

The suite is composed of:
- Atom source code editor (where the user edits the source code of the composition and can submit commands to run on real-time).
- musa-dsl-atom-repl plugin for Atom editor (that allows Atom editor to communicate with the server).
- MusaLCEServer processing server (the server that interprets the source code and the commands submitted by the user).
- MusaLCEforLive Ableton Live Controller (that establishes the communication between Ableton Live and the server).
- MusaLCEforBitwig Bitwig Studio Controller (that establishes the communication between Bitwig Studio and the server).

You need also, of course, Ableton Live 11 or greater or Bitwig Studio 4 or greater.

MusaLCEforLive Ableton Live (this component) integrates with Ableton Live as a MIDI Controller Script.

## Install
**TODO**

## Usage
**TODO**

## Documentation
**TODO**

## Acknowledgements

This project is based on [ideoforms](https://github.com/ideoforms) project [AbletonOSC](https://github.com/ideoforms/AbletonOSC).

Thanks to [ideoforms](https://github.com/ideoforms) for all the work done in **AbletonOSC**.

As **ideoforms** acknowledges:
* Thanks to [Stu Fisher](https://github.com/stufisher/) (and other authors) for LiveOSC, the spiritual predecessor to **AbletonOSC**.
* Thanks to [Julien Bayle](https://structure-void.com/ableton-live-midi-remote-scripts/#liveAPI) and [NSUSpray](https://nsuspray.github.io/Live_API_Doc/) for providing XML API docs, based on original work by [Hans Petrov](http://remotescripts.blogspot.com/p/support-files.html).

# License

The original **AbletonOSC** project from **ideoforms** on which is based 
my project **MusaLCEforLive** has no license published on his github repository (on 2021-11-20)
so it is considered to have all rights reserved 
([see why here](https://choosealicense.com/no-permission/) and 
[here](https://opensource.stackexchange.com/questions/1720/what-can-i-assume-if-a-publicly-published-project-has-no-license)).

For this reason **MusaLCEforLive** can't have a Copyright nor a LICENSE. 
If I could put a license it would be licensed under **GPL 3.0 License** that I think 
could be compatible with the intention of the authors (material and spiritual) 
of the code on which **MusaLCEforLIVE** is based.

Anyway, I will be developing **MusaLCEforLive** extensively in the future, 
adding features not  included in the source code of **AbletonOSC** so, 
in the future I could rewrite the remaining source code parts to make it possible 
to license the project under a public **GPL 3.0 License**. 
