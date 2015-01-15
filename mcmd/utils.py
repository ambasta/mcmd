def get_display_brightness(ambient_brightness):
    '''
    Calculate the optimal display brightness given ambient brightness
    Currently calculated as:
        0 < ambient < 255
        Practically, webcam detects ambient light of 15
        y = 0.003089 * x * x - 6.22622 * x + 318.74
    as a logrithamic curve
    '''
    ambient_brightness = float(ambient_brightness)
    display_brightness = ambient_brightness / 2.55

    return display_brightness
