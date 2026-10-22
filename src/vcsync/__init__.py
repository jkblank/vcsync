"""vcsync — a standalone, owned iPod sync engine for VCpod.

Forked from iOpenPod 1.68.1 (MIT, Copyright (c) 2025 John Gibbons), with the
GUI application layer removed. Covers device discovery/safety, backup and
restore, iTunesDB/ArtworkDB read and write, transcoding, and podcast
sync-plan building — the engine-layer capabilities VCpod's sync-orchestrator
service drives headlessly. See README.md and THIRD_PARTY_NOTICES.md.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
