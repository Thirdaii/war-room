from pathlib import Path
import hashlib
import sys

EXPECTED_SHA256 = "b004ea59dd59d33c0c1739e7796c2f8c5a62d39ca48bdf3bd7555f81c9dd2c70"
EXPECTED_BYTES = 32939
V176_MARKER = "/* War Room v1.7.26 - Atomic per-character Inspect snapshots */"
V175_GRAPHICS_MARKER = "/* War Room v1.7.25 - Live gems and enchantments in WoW tooltips */"
V175_GRAPHICS_END = "window.applyWarRoomInspectGraphics=apply;\n})();"

root = Path(sys.argv[1])
index = root / "index.html"
parts_dir = Path(__file__).with_name("v176_parts")
parts = sorted(parts_dir.glob("part*.txt"))
if len(parts) != 7:
    raise RuntimeError(f"Expected 7 protected v1.7.26 source parts, found {len(parts)}")

block_bytes = b"".join(p.read_bytes() for p in parts)
if len(block_bytes) != EXPECTED_BYTES:
    raise RuntimeError(f"Protected v1.7.26 block byte count mismatch: {len(block_bytes)} != {EXPECTED_BYTES}")
actual_sha = hashlib.sha256(block_bytes).hexdigest()
if actual_sha != EXPECTED_SHA256:
    raise RuntimeError(f"Protected v1.7.26 block SHA-256 mismatch: {actual_sha}")
block = block_bytes.decode("utf-8")

required_source = [
    V176_MARKER,
    "window.WarRoomInspectSnapshots=snapshots",
    "window.WarRoomInspectSwitchReset={clear}",
    "window.WarRoomCharacterModelManifest={build",
    "wr-character-model-stage",
    "/item-appearance?id=",
    "window.WOTLK_TO_RETAIL_DISPLAY_ID_API=undefined",
    "generateModels(aspect",
]
for marker in required_source:
    if marker not in block:
        raise RuntimeError("Recovered v1.7.26 source missing marker: " + marker)

h = index.read_text(encoding="utf-8")
if h.count(V176_MARKER) > 1:
    raise RuntimeError("Duplicate protected v1.7.26 block already present")

if V176_MARKER not in h:
    start = h.find(V175_GRAPHICS_MARKER)
    if start < 0:
        raise RuntimeError("Protected v1.7.25 graphics block not found; refusing unsafe v1.7.26 reconstruction")
    end_marker = h.find(V175_GRAPHICS_END, start)
    if end_marker < 0:
        raise RuntimeError("Could not locate end of protected v1.7.25 graphics block")
    end = end_marker + len(V175_GRAPHICS_END)
    h = h[:start] + block + h[end:]

for marker in required_source:
    if marker not in h:
        raise RuntimeError("Integrated app missing protected marker: " + marker)
if h.count(V176_MARKER) != 1:
    raise RuntimeError("Protected v1.7.26 integration is not unique")

index.write_text(h, encoding="utf-8")
print(f"Restored exact protected War Room v1.7.26 Inspect/gear/3D block ({actual_sha})")
