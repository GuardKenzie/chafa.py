from chafa import *

def test_raw():
    config = CanvasConfig()

    config.width = 36
    config.height = (256 - (16+24))  // 36 + 2


    config.canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_256

    pixels = [0, 0, 0, 0]

    canvas = Canvas(config)
    canvas.draw_all_pixels(
        PixelType.CHAFA_PIXEL_RGBA8_PREMULTIPLIED,
        pixels,
        1, 1, 3
    )


    for row in canvas[:]:
        for pix in row:
            pix.char = "▀"
            pix.remove_foreground()


    for pix in canvas[0,:16]:
        pix.raw_fg_color = pix.x

    for row in canvas[1:-1, :]:
        for pix in row:
            pix.raw_fg_color = pix.x + 16 + ((pix.y-1) * 5 * config.width//5)

    for pix in canvas[-1, :24]:
        pix.raw_fg_color = 255 - (23 - pix.x)

    i = 0
    for pix in canvas[-1, -5:-1]:
        pix.char = str(i)
        i+=1
        pix.raw_fg_color = 3

    print(canvas.print().decode())
