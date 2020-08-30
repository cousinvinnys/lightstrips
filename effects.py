import colorsys


def _hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


def breathe_color(pixel_count=300, color_1=(255, 255, 255), color_2=(0, 0, 0), speed=20):
    """Continuously fades between two colors

    Args:
        pixel_count (int): Number of LEDs in the strips $$ no_input
        color_1 (color): The color to fade to
        color_2 (color): The color to fade from
        speed (float): How fast the lights should fade from the one color to the other $$ range(0, 100)

    Yields:
        list: The colors to be output to the pixels
    """
    blend = 0
    while True:
        r = int((color_1[0] * blend + color_2[0] * (1 - blend)) / 2)
        g = int((color_1[1] * blend + color_2[1] * (1 - blend)) / 2)
        b = int((color_1[2] * blend + color_2[2] * (1 - blend)) / 2)

        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))

        yield [(r, g, b)] * pixel_count

        blend += speed / 2000

        if blend > 1:
            speed = -abs(speed)
        elif blend < 0:
            speed = abs(speed)
    pass


def solid_color(pixel_count=300, color=(255, 0, 0)):
    """Sets the lights to a single solid color

    Args:
        pixel_count (int): Number of LEDs in the strips $$ no_input
        color1 (color): The color to display

    Yields:
        list: The colors to be output to the pixels
    """
    while True:
        yield [color] * pixel_count


def rainbow_breathe(pixel_count=300, speed=20):
    """Loops all of the pixels simultaneously through a rainbow of colors

    Args:
        pixel_count (int): Number of LEDs in the strips $$ no_input
        speed (float): The speed to loop though the rainbow $$ range(0, 100)

    Yields:
        list: The colors to be output to the pixels
    """
    hue = 0
    while True:
        yield [_hsv2rgb(hue, 1, 1)] * pixel_count
        hue += speed / 2000
        hue %= 1

def rainbow_wave(pixel_count=300, wave_speed=20, wave_period=100):
    """Scrolls a wave of RGB puke across the light Strips

    Args:
        pixel_count (int): Number of LEDs in the strips $$ no_input
        wave_speed (float): The speed that the wave should move $$ range(0,100)
        wave_period (float): The number of pixels before a color repeats $$ range(1,300)

    Yields:
        list: The colors to be output to the pixels
    """
    offset = 0
    while True:
        yield [_hsv2rgb((offset + i / wave_period) % 1, 1, 1) for i in range(pixel_count)]
        offset += wave_speed / 2000

def test_effect(pixel_count=300, integer=0, integer_with_range=0, floating=0.0, floating_with_range=0.0, color=(255, 255, 255)):
    """Solely for testing the effect selection page. Displays an alternating checkerboard pattern

    Args:
        pixel_count (int): Number of LEDs in the strips $$ no_input
        integer (int): An integer
        integer_with_range (int): An integer with a range $$ range(0, 10)
        floating (float): A floating point
        floating_with_range (float): A floating point with a range $$ range(0, 100)
        color (color): A color
    """

    while True:
        yield [([(0,0,0) * 3] + [(255,255,255) * 3]) * 50]
        yield [([(0,0,0) * 3] + [(255,255,255) * 3]) * 50]
        yield [([(0,0,0) * 3] + [(255,255,255) * 3]) * 50]
        yield [([(255,255,255) * 3] + [(0,0,0) * 3]) * 50]
        yield [([(255,255,255) * 3] + [(0,0,0) * 3]) * 50]
        yield [([(255,255,255) * 3] + [(0,0,0) * 3]) * 50]
