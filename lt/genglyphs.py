import sys
import fontforge
import psMat

CONSONANTS = "PTKSFNMHZYCXLWGQDBAIEUROV"

behaviours = {
  "K": {
    "scale": 0.4,
    "offset": (550, 0),
    "dia": "ltd01"
  },
  "T": {
    "scale": 64.0 / 80.0,
    "offset": (1000.0 * 16.0 / 80.0 / 2.0, 0),
    "dia": "ltd02"
  },
  "S": {
    "scale": 1.0,
    "offset": (0, 0),
    "dia": "ltd03"
  },
  "X": {
    "scale": 0.9,
    "offset": (-40, 0),
    "dia": "ltd04"
  },
  "F": {
    "scale": 1.0,
    "offset": (0, 0),
    "dia": "ltd07"
  },
  "C": {
    "scale": 64.0 / 80.0,
    "offset": (1000.0 * 16.0 / 80.0 / 2.0, 0),
    "dia": "ltd09"
  },
}

DUPBEH = {
  "scale": 1.0,
  "offset": (0, 0),
  "dia": "ltd06"
}

def perform(glyph, beh, base):
  font.selection.select(ord(base))
  font.copy()
  font.selection.select(glyph)
  font.paste()
  scale = beh["scale"]
  offset = beh["offset"]
  font.transform(psMat.compose(
    psMat.scale(scale),
    psMat.translate(offset[0], offset[1])
  ))
  glyph.changeWeight(25 * (1 - scale))
  font.selection.select(beh["dia"])
  font.copy()
  font.selection.select(glyph)
  font.pasteInto()

font = fontforge.open(sys.argv[1])
print(dir(font))
print(font)

overrides = set()

for c in CONSONANTS:
  for d in CONSONANTS:
    glyphname = "lt_" + c + d
    if glyphname in font: overrides.add(glyphname)

for c in CONSONANTS:
  for d in CONSONANTS:
    glyphname = "lt_" + c + d
    # Respect overrides
    if glyphname in overrides: continue
    glyph = font.createChar(-1, glyphname)
    if c == d:
      perform(glyph, DUPBEH, d)
    elif c in behaviours:
      beh = behaviours[c]
      perform(glyph, beh, d)
    elif d in behaviours:
      beh = behaviours[d]
      perform(glyph, beh, c)
      font.selection.select("ltd05")
      font.copy()
      font.selection.select(glyph)
      font.pasteInto()
    elif ("lt_" + d + c) in overrides:
      font.selection.select("lt_" + d + c)
      font.copy()
      font.selection.select(glyph)
      font.paste()
      font.selection.select("ltd05")
      font.copy()
      font.selection.select(glyph)
      font.pasteInto()
    # set dimensions
    glyph.width = 1000
    glyph.vwidth = 1000

font.save(sys.argv[2])

for g in font.glyphs():
  print("Name: " + g.glyphname)