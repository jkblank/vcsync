"""Regression tests for the ported F1061 native-geometry fix
(upstream iOpenPod 233aeeb / ADR-0218) -- see the comments on
device/artwork_presets.py's ``ArtworkFormat(1061, ...)`` entry.

F1061 (the small Classic/Nano 3G cover-art thumbnail) is natively 55x55
visible RGB565 pixels with 112-byte rows, not 56x56. The prior 56x56
definition fed one extra garbage column/row into every encode -- visible
as corrupted/skewed small cover art on real Classic and Nano 3G hardware.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from vcsync.artworkdb_writer.ithmb_codecs import (
    decode_pixels_for_format,
    encode_image_for_format,
)
from vcsync.artworkdb_writer.rgb565 import IPOD_STRIDE_OVERRIDE, convert_art_for_ipod
from vcsync.device.artwork_presets import ARTWORK_FORMATS_BY_ID


def test_f1061_format_definition_is_55x55_with_112_byte_rows():
    fmt = ARTWORK_FORMATS_BY_ID[1061]
    assert (fmt.width, fmt.height, fmt.row_bytes) == (55, 55, 112)


def _solid_source_image(width: int, height: int, rgb: tuple[int, int, int]) -> Image.Image:
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    arr[:, :] = rgb
    return Image.fromarray(arr)


def test_encode_image_for_format_1061_produces_native_6160_byte_raster():
    # A real source photo, not already 55x55 -- exercises the resize path.
    source = _solid_source_image(300, 300, (10, 20, 30))

    payload = encode_image_for_format(source, 1061)

    assert (payload.width, payload.height) == (55, 55)
    assert payload.stride_pixels == 56
    assert payload.size == 56 * 55 * 2 == 6160
    assert len(payload.data) == 6160


def test_decoding_a_fresh_f1061_raster_crops_the_padding_column_away():
    source = _solid_source_image(300, 300, (200, 40, 80))
    payload = encode_image_for_format(source, 1061)

    decoded = decode_pixels_for_format(1061, payload.data, width=55, height=55)

    assert decoded is not None
    assert decoded.size == (55, 55)
    # No stray padding-column pixel should leak into the visible crop.
    arr = np.array(decoded.convert("RGB"))
    assert arr.shape == (55, 55, 3)


def test_rgb565_stride_override_matches_the_canonical_row_padding():
    # device/artwork_presets.py's row_bytes=112 for a 55px-wide format implies
    # a 56-pixel on-disk stride; the legacy rgb565.py helper must agree.
    assert IPOD_STRIDE_OVERRIDE[1061] == 56


def test_convert_art_for_ipod_legacy_path_also_uses_native_geometry():
    source = _solid_source_image(120, 120, (5, 5, 5))
    import io

    buf = io.BytesIO()
    source.save(buf, format="PNG")

    result = convert_art_for_ipod(buf.getvalue(), 1061)

    assert result is not None
    assert (result["width"], result["height"]) == (55, 55)
    assert result["size"] == 6160
