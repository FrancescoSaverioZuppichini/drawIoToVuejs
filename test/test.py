import unittest

from drawIoToVuejs import main as drawIoToVueJs


class TestDrawIoToVuejs(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.xmlFilePath = './test.xml'

    def parse(self):
        graph = drawIoToVueJs.parse(self.xmlFilePath)
        self.assertNotEqual(graph,None)


