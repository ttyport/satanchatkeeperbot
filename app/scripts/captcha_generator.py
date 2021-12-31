#!/usr/bin/env python3

import random
import string
from PIL import Image
from claptcha import Claptcha
from os import remove


def random_string():
    random_letters = (random.choice(string.ascii_uppercase) for _ in range(6))
    return "".join(random_letters)


def generate_captcha(username):
    captcha = Claptcha(random_string, "../data/font.otf", resample=Image.BICUBIC, noise=0.3)
    text, image = captcha.write(f'../data/{username}.png')
    return text


def delete_captcha(username):
    remove(f"../data/{username}.png")
