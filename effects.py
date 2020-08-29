import colorsys


def _hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


def breathe_color(pixel_count=300, color1=(255, 255, 255), color2=(0, 0, 0), speed=0.01):
    blend = 0
    while True:
        r = int((color1[0] * blend + color2[0] * (1 - blend)) / 2)
        g = int((color1[1] * blend + color2[1] * (1 - blend)) / 2)
        b = int((color1[2] * blend + color2[2] * (1 - blend)) / 2)

        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))

        yield [(r, g, b)] * pixel_count

        blend += speed

        if blend > 1:
            speed = -abs(speed)
        elif blend < 0:
            speed = abs(speed)
    pass


def solid_color(pixel_count=300, color1=(255,0,0)):
    while True:
        yield [color1] * pixel_count


def rainbow_breathe(pixel_count=300, speed=0.01):
    hue = 0
    while True:
        yield [_hsv2rgb(hue, 1, 1)] * pixel_count
        hue += speed
        hue %= 1


def rainbow_wave(pixel_count=300, wave_speed=0.01, wave_frequency=0.01):
    offset = 0
    while True:
        yield [_hsv2rgb((offset + i * wave_frequency) % 1, 1, 1) for i in range(pixel_count)]
        offset += wave_speed