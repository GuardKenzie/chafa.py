from chafa import *

def test_raw_color():
    config = CanvasConfig()

    config.height = config.width = 16
    config.canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_256

    pixels = [255, 255, 255]

    canvas = Canvas(config)
    canvas.draw_all_pixels(
        PixelType.CHAFA_PIXEL_RGB8,
        pixels,
        1, 1, 3
    )

    for y in range(config.height):
        for x in range(config.width):
            canvas[y,x].raw_fg_color = ((y * config.width) + x)
            canvas[y,x].char = "▀"
            canvas[y,x].raw_bg_color = ((config.height-1 - y) * config.width) + (config.width -1- x)

    print(canvas.print().decode())