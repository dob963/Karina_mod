from pathlib import Path

p = Path("App/app/spectrum.c")
s = p.read_text()

anchor = "static int clamp(int v, int min, int max)\n"
helper = r'''
/* Karina V3 Spectrum UI enhancement.
 * Visual-only: same framebuffer geometry, no keyboard/radio-state changes.
 * Each 3x5 glyph is reinforced horizontally by one pixel. */
static void GUI_DisplaySmallestBold(const char *pString, uint8_t x, uint8_t y)
{
    const uint8_t *p = (const uint8_t *)pString;
    while (*p && x < 128)
    {
        uint8_t c = (uint8_t)(*p++);
        if (c < 0x20 || c >= 0x80)
        {
            x += 4;
            continue;
        }
        c -= 0x20;
        for (uint8_t i = 0; i < 3; ++i)
        {
            uint8_t pixels = gFont3x5[c][i];
            for (uint8_t j = 0; j < 6; ++j)
            {
                if (pixels & 1u)
                {
                    const uint8_t xx = (uint8_t)(x + i);
                    const uint8_t yy = (uint8_t)(y + j);
                    if (xx < 128 && yy < 64)
                        PutPixel(xx, yy, true);
                    if (xx + 1u < 128 && yy < 64)
                        PutPixel((uint8_t)(xx + 1u), yy, true);
                }
                pixels >>= 1;
            }
        }
        x += 4;
    }
}

'''
if "static void GUI_DisplaySmallestBold(" not in s:
    if anchor not in s:
        raise SystemExit("anchor not found")
    s = s.replace(anchor, helper + anchor, 1)

old = """    // Align frequency with channel name in status bar (both at x=43).
    // Left-aligned (End == Start = 43) so it does not collide with BW at x=108.
    UI_PrintStringSmallNormal(String, 43, 43, 0);
"""
new = """    // Improved Spectrum: bold frequency, same position and dimensions.
    UI_PrintStringSmallBold(String, 43, 43, 0);
"""
if old not in s:
    raise SystemExit("frequency draw anchor not found")
s = s.replace(old, new, 1)

start = s.index("static void DrawNums()")
end = s.index("static bool SpectrumColumnAtOrAboveY", start)
block = s[start:end]
repls = {
    "GUI_DisplaySmallest(String, 0, 1, false, true);":"GUI_DisplaySmallestBold(String, 0, 1);",
    "GUI_DisplaySmallest(String, 0, 7, false, true);":"GUI_DisplaySmallestBold(String, 0, 7);",
    "GUI_DisplaySmallest(String, 36, 49, false, true);":"GUI_DisplaySmallestBold(String, 36, 49);",
    "GUI_DisplaySmallest(String, 0, 49, false, true);":"GUI_DisplaySmallestBold(String, 0, 49);",
    "GUI_DisplaySmallest(String, 48, 49, false, true);":"GUI_DisplaySmallestBold(String, 48, 49);",
    "GUI_DisplaySmallest(String, 93, 49, false, true);":"GUI_DisplaySmallestBold(String, 93, 49);",
}
for a,b in repls.items():
    block = block.replace(a,b)
s = s[:start] + block + s[end:]
p.write_text(s)
print("OK")
