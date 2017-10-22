import sys
import math
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
  "D": {
    "scale": 1.0,
    "offset": (0, 0),
    "dia": "D"
  },
  "B": {
    "scale": 0.5,
    "offset": (250, 200),
    "dia": "ltd10"
  },
  "A": {
    "scale": 56.0 / 80.0,
    "offset": (1000.0 * 24.0 / 80.0 / 2.0, 0),
    "dia": "ltd11"
  },
  "E": {
    "scale": 0.4,
    "offset": (475, 0),
    "dia": "ltd12"
  },
  "R": {
    "scale": 0.9,
    "offset": (-40, 0),
    "dia": "ltd13"
  },
  "P": {
    "scale": 1.0,
    "offset": (0, 0),
    "dia": "ltd14"
  },
  "Y": {
    "scale": 0.5,
    "offset": (250, 160),
    "dia": "Y"
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
  glyph.changeWeight(50 * (1 - scale))
  font.selection.select(beh["dia"])
  font.copy()
  font.selection.select(glyph)
  font.pasteInto()

def insertReverser(glyph):
  font.selection.select("ltd05")
  font.copy()
  font.selection.select(glyph)
  font.pasteInto()

if sys.argv[1] == sys.argv[2]:
  print("Please choose a different filename to save to")
  exit(-1)

font = fontforge.open(sys.argv[1])
print(dir(font))
print(font)

overrides = set()

for c in CONSONANTS:
  for d in CONSONANTS:
    glyphname = "lt_" + c + d
    if glyphname in font: overrides.add(glyphname)

covered = overrides.copy()

for c in CONSONANTS:
  for d in CONSONANTS:
    glyphname = "lt_" + c + d
    # Respect overrides
    if glyphname in overrides: continue
    glyph = font.createChar(-1, glyphname)
    if c == d:
      perform(glyph, DUPBEH, d)
      covered.add(glyphname)
    elif c in behaviours:
      beh = behaviours[c]
      perform(glyph, beh, d)
      covered.add(glyphname)
    # set dimensions
    glyph.width = 1000
    glyph.vwidth = 1000

for c in CONSONANTS:
  for d in CONSONANTS:
    # Now generate reverse glyphs
    glyphname = "lt_" + c + d
    glyph = font[glyphname]
    # Respect overrides
    if glyphname in covered:
      continue
    if "lt_" + d + c in covered:
      font.selection.select("lt_" + d + c)
      font.copy()
      font.selection.select(glyph)
      font.paste()
      insertReverser(glyph)
    else:
      font.selection.select(ord(c))
      font.copy()
      font.selection.select(glyph)
      font.paste()
      font.selection.select(ord(d))
      font.copy()
      font.selection.select(glyph)
      font.pasteInto()
      if CONSONANTS.index(c) > CONSONANTS.index(d):
        insertReverser(glyph)
    glyph.width = 1000
    glyph.vwidth = 1000

font.addLookup("ltligs", "gsub_ligature", (), [
    ("liga", [("latn", ["dflt"])])
  ])
font.addLookupSubtable("ltligs", "ltligs1")

for c in CONSONANTS:
  for d in CONSONANTS:
    glyphname = "lt_" + c + d
    glyph = font[glyphname]
    glyph.addPosSub("ltligs1", (c, d))

font.save(sys.argv[2])

for g in font.glyphs():
  print("Name: " + g.glyphname)