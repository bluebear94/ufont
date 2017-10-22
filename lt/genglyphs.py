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
  }
}

font = fontforge.open(sys.argv[1])
print(dir(font))
print(font)

for c in CONSONANTS:
  for name, beh in behaviours.items():
    if c != name:
      glyph = font.createChar(-1, "lt-" + name + c)
      font.selection.select(ord(c))
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
      glyph.width = 1000;
      glyph.vwidth = 1000;
  # Generate double glyphs

font.save(sys.argv[2])

for g in font.glyphs():
  print("Name: " + g.glyphname)