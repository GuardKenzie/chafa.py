# CanvasConfig

- [x] Peaking at symbol maps?

- [x] fill_symbol_map
- [x] transparency_threshold
- [x] fg_only
- [x] fg and bg color
- [x] work factor
- [x] dithering
    - [x] mode
    - [x] intensity
- [x] optimizations
- [x] **DOCS**

# Canvas

- [ ] new_similar
- [x] Peeking at config
- [x] inspect characters at (x, y)
- [x] inspect color at (x, y)
- [x] raw color
- [x] **DOCS**
- [x] What argument type should `draw_pixels` accept for the pixel array? <- This is pretty much done
    1. array (pretty fast)
    2. python list and convert to array (slower than array)
    3. Look into `from_buffer` for use with pyvips (faster than array)
    4. Only ctypes array and make user handle conversion (This would be bad)

# Symbol map

- [x] copy
- [x] adding
    - [x] by tags
    - [x] by range
- [x] removing
    - [x] by tags
    - [x] by range

- [x] selectors

- [ ] allow builtin glyphs
- [ ] get glyph
- [ ] add glyph
- [x] **DOCS**

# TermDb

- [x] copy
- [x] fallback info
- [x] **DOCS**

# TermInfo

- [x] copy
- [ ] sequences
    - [ ] get
    - [ ] set
- [x] supplement
- [ ] **emitters!!!**
- [x] **DOCS**

# Misc
- [x] Properly figure out how the loader should work (pretty happy with it for now but could be faster)
- [x] Error handling (I think this is done?)
- [ ] ~~Splitting classes into separate files?~~ (not for now)

# Docs
- [x] Add remaining enums
  - [x] Dither mode
  - [x] Pixel Type

- [x] Docs for the loader

- [x] Write a tutorial
- [x] Add some examples
- [x] Installation
