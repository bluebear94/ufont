import sys
import fontforge
import psMat

CONSONANTS = "PTKSFNMHZYCXLWGQDBAIEUROV"

behaviours = {
  "K": {
    "mat": psMat.compose(
      psMat.scale(0.4),
      psMat.translate(550, 0)),
    "dia": "ltd01"
  },
  "T": {
    "mat": psMat.compose(
      psMat.scale(64.0 / 80.0),
      psMat.translate(1000.0 * 16.0 / 80.0 / 2.0, 0)
    ),
    "dia": "ltd02"
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
      mat = beh["mat"]
      print(mat)
      font.transform(mat)
      glyph.changeWeight(15)
      font.selection.select(beh["dia"])
      font.copy()
      font.selection.select(glyph)
      font.pasteInto()
  # Generate double glyphs

font.save(sys.argv[2])

for g in font.glyphs():
  print("Name: " + g.glyphname)