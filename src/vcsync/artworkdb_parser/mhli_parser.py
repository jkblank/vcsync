import struct
from typing import Any

# Minimum bytes a well-formed mhii record needs before its fixed fields
# (type, header_length, chunk_length, childCount, img_id, ..., srcImgSize)
# can be read -- see mhii_parser.parse_imageItem.
_MHII_MIN_HEADER_LENGTH = 52


def _looks_like_well_formed_mhii(data: bytes, offset: int) -> tuple[int, int] | None:
    """Return (header_length, chunk_length) if a complete, plausible mhii
    record starts at *offset*, else None.

    Used only to recover real mhii records the MHLI header's declared count
    missed -- never to doubt a record already reached by the declared count.
    """
    if offset + 12 > len(data):
        return None
    if data[offset: offset + 4] != b"mhii":
        return None
    header_length = struct.unpack("<I", data[offset + 4: offset + 8])[0]
    chunk_length = struct.unpack("<I", data[offset + 8: offset + 12])[0]
    if header_length < _MHII_MIN_HEADER_LENGTH or chunk_length < header_length:
        return None
    if offset + chunk_length > len(data):
        return None
    return header_length, chunk_length


def parse_mhli(data, offset, header_length, imageCount) -> dict[str, Any]:
    from .chunk_parser import parse_chunk

    imageList = []

    # Parse Children
    next_offset = offset + header_length
    for _i in range(imageCount):
        response = parse_chunk(data, next_offset)
        next_offset = response["nextOffset"]
        imageList.append(response["result"])

    # Recovery pass: iOpenPod upstream (ADR-0133, "Recover evidenced artwork
    # without clearing unavailable covers") found that a stale/incorrect
    # MHLI count can hide real MHII records that are actually present and
    # well-formed right after the ones the declared count already covered.
    # Trusting imageCount alone then silently drops them. Walk forward past
    # the declared count using each candidate record's own header/chunk
    # length -- never the MHLI count -- and only keep going while every
    # step lands on a complete, plausible mhii record; any ambiguity stops
    # the walk immediately and leaves everything already parsed untouched.
    while True:
        probe = _looks_like_well_formed_mhii(data, next_offset)
        if probe is None:
            break
        response = parse_chunk(data, next_offset)
        next_offset = response["nextOffset"]
        imageList.append(response["result"])

    return {"nextOffset": next_offset, "result": imageList}
