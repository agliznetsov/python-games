import functools
import os

import pygame


def load_image(filename):
    fullpath = os.path.join(os.path.dirname(__file__), 'data', filename)
    if not os.path.exists(fullpath):
        raise FileNotFoundError('File not found: {}'.format(fullpath))

    image = pygame.image.load(fullpath)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image


def load_sound(file):
    """because pygame can be compiled without mixer."""
    if not pygame.mixer:
        return None
    file = os.path.join(os.path.dirname(__file__), "data", file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print(f"Warning, unable to load, {file}")
    return None
