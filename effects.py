import colorsys

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def rainbow_breathe(pixel_count=300, speed=0.01):
    hue = 0
    while True:
        yield [hsv2rgb(hue, 1, 1)] * pixel_count
        hue += speed
        hue %= 1

def rainbow_wave(pixel_count=300, wave_speed=0.01, wave_frequency=0.01):
    offset = 0
    while True:
        yield [hsv2rgb((offset + i * wave_frequency) % 1, 1, 1) for i in range(pixel_count)]
        offset += wave_speed