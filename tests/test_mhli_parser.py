"""Regression tests for the ported MHLI/MHII image-count repair fix
(upstream iOpenPod 4095fb5 / ADR-0133) -- see artworkdb_parser/mhli_parser.py.
"""

from __future__ import annotations

import struct

from vcsync.artworkdb_parser.mhli_parser import parse_mhli

_MHII_HEADER_LENGTH = 52


def _build_mhii(img_id: int) -> bytes:
    """A minimal, well-formed, childless mhii record."""
    chunk_length = _MHII_HEADER_LENGTH
    body = b"mhii"
    body += struct.pack("<I", _MHII_HEADER_LENGTH)
    body += struct.pack("<I", chunk_length)
    body += struct.pack("<I", 0)  # childCount
    body += struct.pack("<I", img_id)
    body += struct.pack("<Q", 0)  # songId
    body += struct.pack("<I", 0)  # unk1
    body += struct.pack("<I", 0)  # rating
    body += struct.pack("<I", 0)  # unk2
    body += struct.pack("<I", 0)  # originalDate
    body += struct.pack("<I", 0)  # exifTakenDate
    body += struct.pack("<I", 0)  # srcImgSize
    assert len(body) == chunk_length
    return body


def test_parse_mhli_recovers_well_formed_mhii_records_past_a_stale_count():
    # Three real mhii records on disk, but the MHLI header only declared 1 --
    # the exact defect family ADR-0133 describes and that 1.68.1 inherited
    # unfixed (parse_mhli used to just trust imageCount).
    records = [_build_mhii(img_id) for img_id in (1, 2, 3)]
    data = b"".join(records)

    result = parse_mhli(data, offset=0, header_length=0, imageCount=1)

    assert [r["img_id"] for r in result["result"]] == [1, 2, 3]
    assert result["nextOffset"] == len(data)


def test_parse_mhli_stops_cleanly_when_no_extra_mhii_follows():
    # Declared count matches reality exactly -- no recovery should trigger,
    # and trailing non-mhii bytes must not be touched or consumed.
    records = [_build_mhii(img_id) for img_id in (1, 2)]
    data = b"".join(records) + b"mhlfXXXXXXXX"  # next real sibling chunk

    result = parse_mhli(data, offset=0, header_length=0, imageCount=2)

    assert [r["img_id"] for r in result["result"]] == [1, 2]
    assert result["nextOffset"] == len(records[0]) + len(records[1])


def test_parse_mhli_stops_on_the_first_ambiguous_record():
    # A declared-undercount scenario where what follows is NOT a complete,
    # well-formed mhii record -- must abort the recovery walk rather than
    # guess, leaving only the originally-declared records.
    good = _build_mhii(1)
    truncated_mhii = b"mhii" + struct.pack("<I", _MHII_HEADER_LENGTH) + struct.pack("<I", 9999)
    data = good + truncated_mhii  # chunk_length=9999 claims more bytes than exist

    result = parse_mhli(data, offset=0, header_length=0, imageCount=1)

    assert [r["img_id"] for r in result["result"]] == [1]
    assert result["nextOffset"] == len(good)
