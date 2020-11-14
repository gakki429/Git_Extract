# -*- coding: utf-8 -*-
__author__ = 'gakki429'

import os
import ssl
import struct
import sys
import time
import urllib
import urllib2

try:
    from ctypes import windll, create_string_buffer
except ImportError:
    pass

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    # https://gist.github.com/magnetikonline/9d3aa5d3df53b6a445eda77a16db20bc
    def http_error_300(self, req, fp, code, msg, header_list):
        data = urllib.addinfourl(fp, header_list, req.get_full_url())
        data.status = code
        data.code = code
        return data

    http_error_301 = http_error_300
    http_error_302 = http_error_300
    http_error_303 = http_error_300
    http_error_307 = http_error_300

urllib2.install_opener(
    urllib2.build_opener(NoRedirectHandler())
)
urllib2.getproxies = lambda: {}
ssl._create_default_https_context = ssl._create_unverified_context

def http_resp(url):
    return urllib2.urlopen(url)

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

def _print(stdout, color='cyan', logtime=True, end=''):
    if logtime:
        stdout = '[{}] {}'.format(time.strftime('%H:%M:%S', time.localtime()), stdout)
    if sys.platform.startswith('win'):
        if not end:
            end = '\r\n'
        win_set_color(color)
        print '{}{}'.format(stdout, end),
        win_set_color('default')
    else:
        if not end:
            end = '\n'
        unix_color = {
            'red': 31,
            'green': 32,
            'cyan': 36,
        }
        print '\033[1;{}m{}\033[0m{}'.format(unix_color[color], stdout, end),

def _mkdir(path):
    path = os.path.dirname(path)
    if path and not os.path.exists(path):
        os.makedirs(path)
