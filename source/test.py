import unittest
import source.main as main
from bs4 import BeautifulSoup

class TestStringMethods(unittest.TestCase):
    def testParse(self):
        graph = main.parse("./test.xml")
        self.assertNotEqual(graph,None)
        self.assertNotEqual(len(graph),0)
        self.assertNotEqual(graph[0],None)

    def testRender(self):
        graph = main.parse("./test.xml")
        root = graph[0]
        html = root.render()
        self.assertNotEqual(html,None)
        isHtml = bool(BeautifulSoup(html,'html.parser').find())
        self.assertEqual(isHtml,True)
        # self.assertRaises(Exception, main.parse(""))

