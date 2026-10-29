from pathlib import Path
import hashlib
import struct

SRC = Path("11.08fw_3.bin")
DIST = Path("dist")
DIST.mkdir(exist_ok=True)

OUT = DIST / "KARINA_11.08_IMPROVED.bin"
ORIGINAL = DIST / "KARINA_11.08_ORIGINAL.bin"

EXPECTED_SIZE = 60948
FONT_START = 0xD502
FONT_LENGTH = 286

data = bytearray(SRC.read_bytes())
if len(data) != EXPECTED_SIZE:
    raise SystemExit(f"Unexpected firmware size: {len(data)} (expected {EXPECTED_SIZE})")

# Keep the original image byte-for-byte available for recovery/comparison.
ORIGINAL.write_bytes(data)

# Safe, isolated display-font improvement from the existing Karina-mod project.
# No code/bootloader/config areas are touched by this pass.
patched = bytearray(data)
end = FONT_START + FONT_LENGTH
for i in range(FONT_START + 1, end):
    patched[i] |= data[i - 1]

if patched[:FONT_START] != data[:FONT_START] or patched[end:] != data[end:]:
    raise SystemExit("Patch escaped the isolated font region")

OUT.write_bytes(patched)

def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def changed_ranges(a, b):
    aa, bb = a.read_bytes(), b.read_bytes()
    ranges=[]
    start=None
    for i,(x,y) in enumerate(zip(aa,bb)):
        if x != y and start is None:
            start=i
        if start is not None and (x == y or i == len(aa)-1):
            stop=i if x != y and i == len(aa)-1 else i-1
            ranges.append((start,stop,stop-start+1))
            start=None
    return ranges

ranges=changed_ranges(ORIGINAL, OUT)
if not ranges:
    raise SystemExit("No bytes changed")
if any(s < FONT_START or e >= end for s,e,_ in ranges):
    raise SystemExit(f"Unexpected changed range: {ranges}")

print(f"size={len(patched)}")
print(f"original_sha256={sha256(ORIGINAL)}")
print(f"improved_sha256={sha256(OUT)}")
print(f"changed_ranges={ranges}")
