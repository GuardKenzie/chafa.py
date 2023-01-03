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
- [ ] **DOCS**

# Canvas

- [ ] copy
- [x] Peeking at config
- [x] inspect characters at (x, y)
- [x] inspect color at (x, y)
- [ ] raw color
- [ ] **DOCS**
- [ ] What argument type should `draw_pixels` accept for the pixel array?
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
- [ ] **DOCS**

# TermDb

- [x] copy
- [x] fallback info
- [ ] **DOCS**

# TermInfo

- [x] copy
- [ ] sequences
    - [ ] get
    - [ ] set
- [x] supplement
- [ ] **emitters!!!**
- [ ] **DOCS**

# Misc
- [ ] Properly figure out how the loader should work
- [x] Error handling (I think)
- [ ] Splitting classes into separate files?
