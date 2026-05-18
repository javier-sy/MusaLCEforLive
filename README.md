# MusaLCE for Live

**Ableton Live MIDI Remote Script for the Musa Live Coding Environment.**

A MIDI Remote Script (Python) for Ableton Live 11+ that bridges Ableton Live with the [musalce-server](https://github.com/javier-sy/musalce-server) Ruby gem. The score code you write in [Visual Studio Code](https://github.com/javier-sy/MusaLCEClientForVSCode) is evaluated by `musalce-server`, which uses this script to drive Live (MIDI clock sync via a virtual MIDI bus, track manipulation via the Live API, MIDI note output).

## How it fits in the suite

```
[VSCode + MusaLCEClientForVSCode] ──TCP 1327─▶ [musalce-server] ──OSC/UDP──▶ [MusaLCEforLive] ──▶ [Ableton Live]
```

This component is the DAW-side endpoint for Live. It is part of the **suite workflow** of MusaLCE — for the standalone REPL workflow (no server, no script), see the [MusaLCEClientForVSCode README](https://github.com/javier-sy/MusaLCEClientForVSCode#readme).

For the full architecture of the suite (component responsibilities, REPL DSL surface, Stop/Play semantics, and the OSC handler + surface contracts in detail), see the canonical reference: [musalce-server/docs/architecture.md](https://github.com/javier-sy/musalce-server/blob/master/docs/architecture.md).

## Requirements

- Ableton Live 11 or higher
- macOS, Linux or Windows (paths and bus setup differ — see below)
- A virtual MIDI bus for clock sync (IAC Driver on macOS, loopMIDI on Windows, snd-virmidi on Linux). Live does not expose its transport directly to MIDI Remote Scripts, so MusaLCE drives Live's tempo by sending MIDI clock through this bus.
- [musalce-server](https://github.com/javier-sy/musalce-server) installed and running (`musalce-server live`).

## Install

Copy the entire `MusaLCEforLive/` folder (or symlink it) into Live's *User Library → Remote Scripts*:

| OS | Path |
|---|---|
| macOS | `~/Music/Ableton/User Library/Remote Scripts/MusaLCEforLive/` |
| Linux | `~/Music/Ableton/User Library/Remote Scripts/MusaLCEforLive/` |
| Windows | `%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\MusaLCEforLive\` |

Restart Ableton Live so it picks up the new script.

## Enable in Live

1. Open Live's **Preferences → Link/Tempo/MIDI → MIDI**.
2. In the *Control Surface* dropdown, pick **MusaLCEforLive**.
3. Leave the *Input* and *Output* dropdowns at "(None)" — this script does its own OSC I/O and does not need a MIDI port assigned at the Control Surface level.

A confirmation banner appears in Live: *"Musa Live Coding Environment for Live: Listening for OSC on port 10001"*.

## IAC bus setup (macOS)

Live's MIDI Remote Script API does not expose transport control (play/stop/position). MusaLCE works around this by sending MIDI clock through a virtual bus that Live can sync to.

1. Open **Audio MIDI Setup → Window → Show MIDI Studio**.
2. Double-click the **IAC Driver** icon.
3. Check **Device is online**.
4. Make sure there is at least one bus (default: *Bus 1*) — create one if needed.

In your score (REPL), tell the server to send MIDI clock through this bus:

```ruby
daw.midi_sync('IAC Driver Bus 1')
```

In Live's *Preferences → Link/Tempo/MIDI → MIDI*, enable **Sync** on the IAC bus input so Live follows the clock.

For Windows use [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html); for Linux use `snd-virmidi`. Same pattern: virtual MIDI bus, MusaLCE sends clock, Live syncs to it.

## OSC ports

| Direction | Port | Constant |
|---|---|---|
| musalce-server → script | 10001 (UDP) | `OSC_LISTEN_PORT` (in `musalce4liveosc/constants.py`) |
| script → musalce-server | 11011 (UDP) | `OSC_RESPONSE_PORT` (in `musalce4liveosc/constants.py`) |

Both ports are hardcoded to match `musalce-server`'s expected channel.

## Limitations vs MusaLCEforBitwig

| Aspect | Live | Bitwig |
|---|---|---|
| Transport control from server | ❌ Not available (Live MIDI Remote Script API limitation) | ✅ Full control |
| Clock sync mechanism | Server sends MIDI clock through virtual bus, Live syncs to it | Server reads MIDI clock from any controller marked as clock source |
| Track names | Can repeat — use `daw.track('Drums', all: true)` to access all of them | Must be unique |
| MusaLCE Surface protocol (Stream Deck via Pulso) | ❌ **Not yet implemented** | ✅ Implemented in `MusaLCESurfaceRelay` |

### Surface protocol feature gap

This script does **not** yet implement the MusaLCE Surface protocol relay that ships in [MusaLCEforBitwig](https://github.com/javier-sy/MusaLCEforBitwig). That means Stream Deck integration via **Pulso Bridge** ([yeste.studio](https://yeste.studio)'s upcoming Stream Deck plugin for the MusaLCE Surface protocol; public release pending) is currently a Bitwig-only feature. Scoring `surface[:event]` controls works in code, but their state will not reach a Stream Deck driven from a Live session until the relay is ported here.

## Reload during development

The script exposes an OSC reload command at `/live/reload` that re-imports all `musalce4liveosc.*` modules in place. Useful when editing the Python source without wanting to fully restart Live. It is also called automatically on Live API errors.

There is also a smoke-test endpoint `/live/test` that replies `/live/test ok` and shows a banner — handy for verifying the OSC link.

Live's embedded Python implementation does **not** support threading (Live beachballs if a thread is started). All long-running work, including the OSC server, runs from the script's `tick()` method scheduled every 100 ms.

## Logs

The script writes to a hardcoded log file:

- macOS / Linux: `/tmp/musalce4live.log`
- Windows: *not yet portable — the path is hardcoded.*

```bash
tail -f /tmp/musalce4live.log
```

## Acknowledgements

This project is based on [ideoforms](https://github.com/ideoforms)' project [AbletonOSC](https://github.com/ideoforms/AbletonOSC).

As **ideoforms** acknowledges:
- Thanks to [Stu Fisher](https://github.com/stufisher/) (and other authors) for LiveOSC, the spiritual predecessor to **AbletonOSC**.
- Thanks to [Julien Bayle](https://structure-void.com/ableton-live-midi-remote-scripts/#liveAPI) and [NSUSpray](https://nsuspray.github.io/Live_API_Doc/) for providing XML API docs, based on original work by [Hans Petrov](http://remotescripts.blogspot.com/p/support-files.html).

## License

The original **AbletonOSC** project from **ideoforms** on which this project is based has no license published on its GitHub repository (as of 2021-11-20) so it is considered to have all rights reserved ([see why here](https://choosealicense.com/no-permission/) and [here](https://opensource.stackexchange.com/questions/1720/what-can-i-assume-if-a-publicly-published-project-has-no-license)).

For this reason **MusaLCEforLive** cannot have a Copyright nor a LICENSE. If a license could be applied, it would be **GPL 3.0**, which is believed to be compatible with the intention of the authors (material and spiritual) of the code on which **MusaLCEforLive** is based.

**MusaLCEforLive** is being developed extensively in directions not covered by **AbletonOSC** so, in the future, the remaining derived source code parts may be rewritten to make it possible to license the project under a public **GPL 3.0 License**.
