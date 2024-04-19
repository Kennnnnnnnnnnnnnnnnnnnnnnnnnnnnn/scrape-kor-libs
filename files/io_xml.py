import os
import xml.etree.ElementTree as ET

from .io_file import *
'''
root = ET.fromstring(xml_str)
findall, get, .text, .attrib
ET.parse, tree.getroot()
tree_root = ET.parse('input.xml')

<library>
    <list>
        <title>가나다도서관</title>
        <valid>O</valid>
    </list>
</library>
'''


class IoXml(IoFile):
    @staticmethod
    def create(path_in, path_out, list_libs):
        obj = None
        ext_in = os.path.splitext(path_in)[1]
        # print("%s" % ext_in)
        if ext_in == '.xml':
            obj = IoXml(path_in, path_out, list_libs)
        return obj

    def __init__(self, path_in, path_out, list_libs):
        self.f_in = open(path_in, mode='r', encoding='UTF-8')
        self.path_out = path_out
        self.root_in = ET.parse(self.f_in)
        # os.remove(path_out)
        self.root_out = ET.Element('body')
        self.list_libs = list_libs
        self.iter_dir = IterableGetDirName(self.root_in, 'area')
        self.nodes = None
        self.library = None
        self._list = None
        super(__class__, self).__init__()

    def get_dir_iter(self):
        try:
            # print(self.iter_dir.get_cur())
            self.nodes = self.iter_dir.get_cur().findall('library')
            res = self.iter_dir.__next__()
        except IndexError or StopIteration:
            res = ''
        return res

    def set_dir(self, name):
        self.nodes = self.root_in.find(name).findall('list')

    def create_values(self, key):
        self.iter_get[key] = IterableGetValue(key, self.nodes)

    def init_result(self, key):
        item = ET.Element('library', {'name': key})
        self.library = item
        self.root_out.append(item)

    def create_keyword_iter(self, row):
        self._list = ET.Element('list')
        self.library.append(self._list)
        self.iter_set = IterableSetValue('keyword', self._list)

    def insert_keyword_iter(self, val):
        self.iter_set.set_value(val)

    def create_value_iter(self, row):
        item = ET.Element('entry')
        self._list.append(item)
        self.iter_set = IterableSetValue('prop', item)

    def insert_value_iter(self, val):
        self.iter_set.set_value(val)

    def __del__(self):
        # self.root_out.write(self.root_out)
        self.f_in.close()
        tree = ET.ElementTree(self.root_out)
        ET.indent(tree)
        tree.write(self.path_out, encoding='utf-8')


class IterableGetDirName(Iterable):
    def __init__(self, root_in, name):
        self.names = root_in.findall(name)
        self.len = len(self.names)
        self.idx = 0

    def __next__(self):
        if self.idx >= self.len:
            raise StopIteration
        else:
            res = self.names[self.idx].attrib['name']
            self.idx += 1
        return res

    def get_cur(self):
        return self.names[self.idx]


class IterableGetValue(Iterable):
    def __init__(self, key, items):
        self.key = key
        self.items = items
        self.len = len(self.items)
        self.idx = 0

    def __next__(self):
        if self.idx >= self.len:
            raise StopIteration
        else:
            # print("%d %s" % (self.idx, self.key))
            res = self.items[self.idx].attrib[self.key]
            self.idx += 1
        return res


class IterableSetValue(Iterable):
    def __init__(self, key, node):
        self.key = key 
        self.node = node

    def __next__(self):
        pass

    def set_value(self, val):
        item = ET.Element(self.key)
        item.text = val
        self.node.append(item)
