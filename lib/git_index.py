# -*- coding: utf-8 -*-
__author__ = 'gakki429'

import re

class GitIndex(object):
    """Git Parse Index Format"""
    def __init__(self, git_path):
        self.git_path = git_path
        self.index_path = 'index'
        self.index_data = open(self.index_path, 'rb')
        self.index_number = 0
        self.tree_objects = {}
        self.blob_objects = {}

    def str2int(self, string):
        return int(string.encode('hex'), 16)

    def reads(self, size, count=1):
        datas = []
        for i in range(count):
            data = self.index_data.read(size)
            datas.append(data)
        if len(datas) == 1:
            return datas[0]
        else:
            return tuple(datas)

    def dirc_parse(self):
        signature = self.reads(4)
        if signature == 'DIRC':
            version_number = self.reads(4)
            self.index_number = self.str2int(self.reads(4))
            self.dirc_entry()

    def dirc_entry(self):
        for i in range(self.index_number):
            ctime, ctime_nanosecond = self.reads(4, 2)
            mtime, mtime_nanosecond = self.reads(4, 2)
            device, inode = self.reads(4, 2)
            mode = str(oct(self.str2int(self.reads(4))))[1:]
            uid, gid = self.reads(4, 2)
            size = self.str2int(self.reads(4))
            _hash = self.reads(20).encode('hex')
            flags = self.str2int(self.reads(2))
            bin_flags = bin(flags)[2:].rjust(16, '0')
            # Todo: 依据 flags 区分版本
            name_len = flags & 0xfff
            filename = self.reads(name_len)
            fill_len = 8 - ((0x3e + name_len) % 8)
            fill = self.reads(fill_len)
            if _hash in self.blob_objects:
                self.blob_objects[_hash].append({'filename': filename, 'mode': mode, 'size': size})
            else:
                self.blob_objects[_hash] = [{'filename': filename, 'mode': mode, 'size': size}]

    def tree_parse(self):
        signature = self.reads(4)
        if signature == 'TREE':
            tree_length = self.str2int(self.reads(4))
            tree_data = self.reads(tree_length)
            self.tree_extension(tree_data)

    def tree_extension(self, tree_data):
        tree_info = re.findall(r'(.*?)\x00(\d+) (\d+)\x0a(.{20})', tree_data, re.S|re.M)
        for _name, _all_count, _dir_count, _hash in tree_info:
            _hash = _hash.encode('hex')
            self.tree_objects[_hash] = {'name': _name}

    def index_init(self):
        self.dirc_parse()
        self.tree_parse()
        # Todo: 完善其他几种类型的解析
        self.index_data.close()
