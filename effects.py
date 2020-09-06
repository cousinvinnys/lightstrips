import colorsys
from random import randint
from time import time


def _hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def _color_brightness(color, brightness):
    # Brightness (float): 0-1
    return (int(brightness * color[0]), int(brightness * color[1]), int(brightness * color[2]))


def _blend(color_1, color_2, percentage_color_1):
    r = int((color_1[0] * percentage_color_1 + color_2[0] * (1 - percentage_color_1)) / 2)
    g = int((color_1[1] * percentage_color_1 + color_2[1] * (1 - percentage_color_1)) / 2)
    b = int((color_1[2] * percentage_color_1 + color_2[2] * (1 - percentage_color_1)) / 2)

    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))

    return (r, g, b)


def breathe_color(pixel_count, color_1=(255, 255, 255), color_2=(0, 0, 0), speed=20):
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
        blended = _blend(color_1, color_2, blend)

        yield [blended] * pixel_count

        blend += speed / 2000

        if blend > 1:
            speed = -abs(speed)
        elif blend < 0:
            speed = abs(speed)
    pass


def solid_color(pixel_count, color=(255, 0, 0)):
    """Sets the lights to a single solid color

    Args:
        pixel_count (int): Number of LEDs in the strips $$ no_input
        color (color): The color to display

    Yields:
        list: The colors to be output to the pixels
    """
    while True:
        yield [color] * pixel_count


def rainbow_breathe(pixel_count, speed=20):
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


def rainbow_wave(pixel_count, wave_speed=20, wave_period=100):
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


def stars(pixel_count, starriness=10, color=(255, 255, 255)):
    '''Twinkly little stars

    Args:
        pixel_count (int): Number of LEDS in the strips $$ no_input
        starriness (float): Percentage of the light strip that should be taken by stars $$ range(0, 100)
        color (color): The color of the stars

    Yields:
        list: The colors to be output to the pixels
    '''

    def get_star_count(stars):
        space_count = stars.count(0)
        star_count = len(stars) - space_count
        return star_count

    starriness /= 100.0
    stars = [0] * pixel_count
    while True:
        num_stars = get_star_count(stars)
        star_ratio = num_stars / len(stars)

        # Summon new stars
        while star_ratio < starriness:
            num_stars = get_star_count(stars)
            star_ratio = num_stars / len(stars)
            stars[randint(0, len(stars) - 1)] = randint(255 // 2, 255)

        # Fade out current stars
        for i in range(len(stars)):
            if stars[i] > 0:
                stars[i] -= 1
                if stars[i] < 0:
                    stars[i] = 0

        # Create list to yield
        pixels = []
        for i in range(len(stars)):
            pixels.append(_color_brightness(color, stars[i] / 255))

        yield pixels


def fade(pixel_count, from_color=(0, 0, 0), to_color=(255, 255, 255), duration=3600):
    ''' Fades from from_color to to_color over duration seconds

    Args:
        pixel_count (int): Number of LEDS in the strips $$ no_input
        from_color (color): The color to start at
        to_color (color): The color to end at
        duration (int): The number of seconds to perform the fade over $$ input range(1, 86400)

    Yields:
        list: The colors to be output to the pixels
    '''

    time_start = time()
    pixels = [from_color] * pixel_count
    while True:
        percent_complete = 1 - (time() - time_start) / duration
        percent_complete = percent_complete if percent_complete < 1 else 1
        color = _blend(from_color, to_color, percent_complete)
        yield [color] * pixel_count


# TODO: fade_in(duration), fade_out(duration), galaxy, snow, weather
