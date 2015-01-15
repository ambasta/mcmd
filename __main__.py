import time
from mcmd import MCMD


if __name__ == '__main__':
    mcmd = MCMD()
    while True:
        new_brightness = mcmd.adjust()
        new_brightness = int(new_brightness * 100 / 318)
        mcmd.set_brightness(new_brightness)
        time.sleep(10)
