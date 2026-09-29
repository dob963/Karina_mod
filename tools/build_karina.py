from pathlib import Path

SRC = Path("11.08fw_3.bin")
OUT = Path("dist")
OUT.mkdir(exist_ok=True)

data = bytearray(SRC.read_bytes())
if len(data) != 60948:
    raise SystemExit(f"Unexpected firmware size: {len(data)}")

# Reproduce the known font-only patch, but keep the original untouched.
# The patch is deliberately isolated to the big-digit font region.
start = 0xD502
length = 286
end = start + length
patched = bytearray(data)
for i in range(start + 1, end):
    patched[i] |= data[i - 1]

(OUT / "11.08fw_3_KARINA_PLUS_TEST.bin").write_bytes(patched)
(OUT / "11.08fw_3_ORIGINAL_COPY.bin").write_bytes(data)
print("Built firmware artifacts.")
