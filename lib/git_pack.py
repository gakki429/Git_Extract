# -*- coding: utf-8 -*-
__author__ = 'gakki429'

import re
import os
import zlib
import hashlib
from lib.utils import _mkdir, _print

class GitPack(object):
    """Git Parse Pack Format"""
    def __init__(self, git_path, pack_hash):
        self.git_path = git_path
        self.pack_hash = pack_hash
        self.objects = {} # hash: {type, length}
        self.objects_num = 0
        self.idx_path = 'objects/pack/pack-{}.idx'.format(self.pack_hash)
        self.pack_path = 'objects/pack/pack-{}.pack'.format(self.pack_hash)
        self.pack_data = ''

    def pack_header(self):
        pack = open(self.pack_path, 'rb').read()
        signature = pack[:4]
        if signature == 'PACK':
            version_number = pack[4:8]
            objects_number = pack[8:12]
            self.objects_num = int(objects_number.encode('hex'), 16)
            self.pack_data = pack

    def idx_header(self):
        pack_idx = open(self.idx_path, 'rb').read()
        magic_number = pack_idx[:4]
        if magic_number == '\xfftOc':
            version_number = pack_idx[4:8]
            fan_out_table = pack_idx[8:8+1024]
            pack_hash = pack_idx[-40:-20]
            idx_hash = pack_idx[-20:]
            # Todo: 区分版本（v1，v2），区分idx大小，大于 2g 的 offset 为 8bytes
            idx_data = pack_idx[8+1024:-40]
            self.parse_idx(idx_data)

    def split_to_hex(self, length, data):
        data = re.findall(r'(.{{{}}})'.format(length), data, re.S|re.M)
        return map(lambda x: x.encode('hex'), data)

    def parse_idx(self, idx_data):
        num = self.objects_num
        _hashs = self.split_to_hex(20, idx_data[:num*20])
        _crcs = self.split_to_hex(4, idx_data[num*20:num*24])
        _offsets = self.split_to_hex(4, idx_data[num*24:])
        for i in range(num):
            self.objects[_hashs[i]] = {'crc': _crcs[i], 'offset': int(_offsets[i], 16)}

    def extract_pack(self):
        sort_objects = sorted(self.objects.items(), key=lambda x: x[1]['offset'])
        for i in range(len(sort_objects)):
            _hash, _info = sort_objects[i]
            crc = _info['crc']
            offset = _info['offset']
            if i == len(sort_objects)-1:
                next_offset = -20
            else:
                next_offset = sort_objects[i+1][1]['offset']
            self.objects[_hash]['data'] = self.pack_data[offset:next_offset]
        self.parse_pack()

    def pack_type(self, num):
        _types = {
            '1': 'commit',
            '2': 'tree',
            '3': 'blob',
            '4': 'tag',
            '6': 'ofs_delta',
            '7': 'ref_delta',
        }
        return _types[str(int(num, 2))]

    def parse_pack(self):
        for _hash, _info in sorted(self.objects.items(), key=lambda x: x[1]['offset']):
            _size = []
            try:
                flag, zlib_data = re.search('(.*?)(\x78\x9c.*)', _info['data'], re.S).groups()
            except AttributeError:
                return
            for i in range(len(flag)):
                bin_info = bin(int(flag[i].encode('hex'), 16))[2:].rjust(8, '0')
                msb = bin_info[0]
                if i == 0:
                    _type = bin_info[1:4]
                    _size.append(bin_info[-4:])
                else:
                    _size.append(bin_info[-7:])
            _length = int(''.join(_size[::-1]), 2) # 这里其实是小端，不是大端
            _type = self.pack_type(_type)
            self.objects[_hash]['type'] = _type
            self.objects[_hash]['length'] = _length
            self.objects[_hash]['file'] = zlib.decompress(zlib_data)

    def pack_to_object_file(self):
        for _object in self.objects.values():
            try:
                object_format = '{} {}\x00{}'.format(
                    _object['type'], _object['length'], _object['file'])
            except KeyError:
                continue
            sha = hashlib.sha1(object_format).hexdigest()
            path = 'objects/{}/{}'.format(sha[:2], sha[2:])
            zlib_object = zlib.compress(object_format)
            _mkdir(path)
            _print('[+] Pack {}'.format(path), 'green', end='\r')
            open(path, 'wb').write(zlib_object)
        _print('', logtime=False)

    def pack_init(self):
        self.pack_header()
        self.idx_header()
        self.extract_pack()
        self.pack_to_object_file()
        # Todo: 重建 ofs_delta，ref_delta
