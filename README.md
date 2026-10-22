# vcsync

A standalone, owned iPod sync engine for [VCpod](https://github.com/jkblank/VCpod).
Covers device discovery/safety, backup and restore, iTunesDB/ArtworkDB
read and write, transcoding, and podcast sync-plan building -- the
engine-layer capabilities VCpod's `sync-orchestrator` service drives
headlessly to sync music, podcasts, and audiobooks onto real click-wheel
iPods.

## Why this exists

`sync-orchestrator` used to depend on [iOpenPod](https://github.com/TheRealSavi/iOpenPod)
(PyPI `iopenpod`) for this. Upstream's `1.68.1` is the newest release in
its compatible line; everything after it (`2.0.x`) is a ground-up,
GUI-app rewrite -- renamed top-level package, the headless `SyncEngine`/
`BackupManager`/etc. API gone, Python 3.12-only, and a new dependency
footprint built around a GUI toolkit and an audio-reactive visualizer.
See `VCpod`'s `music-stack/notes.md` (2026-10-22) for the full
investigation.

`vcsync` is iOpenPod `1.68.1`'s non-GUI engine code (MIT-licensed, see
`THIRD_PARTY_NOTICES.md`), with the GUI application layer removed and the
package renamed, forked directly into this repo so we aren't exposed to
upstream's direction again. Two upstream fixes from iOpenPod `2.0.x`'s
engine code -- independently confirmed to apply to `1.68.1` too, not just
to bugs the 2.0 rewrite introduced in itself -- were ported in:

1. The MHLI/MHII image-count repair algorithm (upstream iOpenPod `4095fb5`,
   ADR-0133) -- `artworkdb_parser/mhli_parser.py` no longer silently drops
   real MHII artwork records sitting past a stale/wrong MHLI count.
2. A JPEG-decoder hardening one-liner in `artworkdb_writer/ithmb_codecs.py`.

## What's included / excluded

Included: `device/`, `sync/` (incl. `sync/core/`), `podcasts/`,
`itunesdb_parser/`, `itunesdb_shared/`, `itunesdb_writer/` (incl. the
`wasm/` HASHAB module for Nano 6G/7G), `artworkdb_parser/`,
`artworkdb_writer/`, `artworkdb_shared/`, `sqlitedb_writer/` (Nano 6G/7G
SQLite-based device DB), `infrastructure/media_folders.py` and
`settings_paths.py`, `sync_progress_stages.py`.

Excluded: the entire GUI application layer (`gui/`, `gui/widgets/`,
`themes/`, GUI-only `assets/`, `__main__.py`), `application/` (iOpenPod's
own GUI-session/job-progress shell -- `sync-orchestrator` plays this role
on our side), `resources.py`/`search.py` (GUI-facing helpers), and the
app-settings/theme persistence modules under `infrastructure/` that
iOpenPod's own GUI uses to remember window state/theme choice.

Confirmed, by direct inspection, zero GUI (PyQt6/QtWidgets/QtGui) imports
anywhere in the included tree.

## Status

Freshly forked -- not yet integration-tested against `sync-orchestrator`
or a real device. See `sync-orchestrator`'s own repo for the integration
work (re-pointing its imports at `vcsync` instead of PyPI `iopenpod`) and
the plan-before-execute verification against real hardware before this
is trusted for anything beyond planning.

## License

MIT, see `LICENSE`. Most of this codebase is derived from iOpenPod
`1.68.1` -- see `THIRD_PARTY_NOTICES.md` for its original license text.
