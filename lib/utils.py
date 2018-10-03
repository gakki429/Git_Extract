# -*- coding: utf-8 -*-
__author__ = 'gakki429'

import os
import sys
import struct

try:
    from ctypes import windll, create_string_buffer
except ImportError:
    pass

def win_default_color():
    stdout_handle = windll.kernel32.GetStdHandle(-11)
    csbi = create_string_buffer(22)
    windll.kernel32.GetConsoleScreenBufferInfo(stdout_handle, csbi)
    wattr = struct.unpack("hhhhHhhhhhh", csbi.raw)[4]
    return wattr

if sys.platform.startswith('win'):
    default = win_default_color()
    default_bg = default & 0xf0

def win_set_color(color='cyan'):
    win_color = {
        'green': 0xa,
        'cyan': 0xb,
        'red': 0xc,
        'default': default,
    }
    stdout_handle = windll.kernel32.GetStdHandle(-11)
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, win_color[color]|default_bg)

def _print(stdout, color='cyan'):
    if sys.platform.startswith('win'):
        win_set_color(color)
        print '{}\r\n'.format(stdout),
        win_set_color('default')
    else:
        unix_color = {
            'red': 31,
            'green': 32,
            'cyan': 36,
        }
        print '\033[1;{}m{}\033[0m\n'.format(unix_color[color], stdout),

def _mkdir(path):
    path = os.path.dirname(path)
    if path and not os.path.exists(path):
        os.makedirs(path)