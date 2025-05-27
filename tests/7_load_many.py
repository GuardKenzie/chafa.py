import chafa.loader

# Uncomment to enable ImageMagick event logging:
# import ctypes
# chafa.loader._MagickWand.SetLogEventMask(ctypes.c_char_p(b'all\0'))

# Load enough copies of 'snake.jpg' to reveal resource leaks.
for i in range(1, 10_000+1):
    img = chafa.loader.Loader('snake.jpg')
    print(f'\x1b[G{i}', end='', flush=True)
    if img.width == 0:
        print(f'\x1b[GFailed after loading {i} copies of "snake.jpg"')
        break
else:
    print('\nA-OK')
