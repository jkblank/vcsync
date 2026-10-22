# Third-party notices

Most of `src/vcsync/` (`device/`, `sync/`, `podcasts/`, `itunesdb_parser/`,
`itunesdb_shared/`, `itunesdb_writer/`, `artworkdb_parser/`,
`artworkdb_writer/`, `artworkdb_shared/`, `sqlitedb_writer/`,
`infrastructure/media_folders.py`, `infrastructure/settings_paths.py`,
`sync_progress_stages.py`) is derived from
[iOpenPod](https://github.com/TheRealSavi/iOpenPod) `v1.68.1`
(commit `de300074a25f6f327b54a7141720e5fbff9d5c5b`), with its GUI
application layer (PyQt6 widgets/dialogs/themes, the GUI-only app shell,
and the network-driven podcast-subscription-manager UI) removed, the
top-level package renamed from `iopenpod` to `vcsync`, and (as of this
fork) two upstream fixes ported from iOpenPod 2.0.x's non-GUI engine code
(the MHLI/MHII image-count repair algorithm, and a JPEG-decoder
hardening). See `notes.md` in the `music-stack` repo (2026-10-22) for the
investigation that led to this fork, and this repo's own `README.md` for
what's included/excluded.

iOpenPod's original license:

```
MIT License

Copyright (c) 2025 John Gibbons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
