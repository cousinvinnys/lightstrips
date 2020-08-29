import colorsys

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def rainbow_breathe(speed=0.01):
    hue = 0
    while True:
        yield [hsv2rgb(hue, 1, 1)] * 300
        hue += speed
        hue %= 1