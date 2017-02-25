import xmltodict
from bs4 import BeautifulSoup
import os
import sys


class Node:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.components = []
        self.componentsBasePath = ""

    def __str__(self):
        return self.value

    def render(self):
        return "to be override"


class VueNode(Node):
    def render(self):
        importString = ""
        componentsString = ""
        componentEl = ""
        for component in self.components:
            importPath = os.path.normpath(self.componentsBasePath + "/" + component.value)
            importString += "import %s from '.%s/%s.vue'\n" % (
                component, importPath, component.value)
            componentsString += "%s," % (component)
            # print(componentsString)
        template = "<template><div id='%s'>%s</div></template>\n<script> %s export default { name: '%s', components: { %s }, } </script>\n<style></style>" % (
            self.value, componentEl, importString, self.value, componentsString)
        return template

    def create(self, basePath):
        if not os.path.exists(basePath + '/' + self.componentsBasePath):
            os.makedirs(basePath + '/' + self.componentsBasePath)

        template = self.render()

        if not os.path.exists(basePath):
            os.makedirs(basePath)

        open("{}.vue".format(basePath + '/' + self.value), 'w').write(template)

        print("Created %s" %(self.value + '.vue'))

        for component in self.components:
            newPath = os.path.normpath(basePath + '/' + self.componentsBasePath + '/' + component.value)
            component.create(newPath)


def usage():
    print("usage: python3 main.py [xmlFile] [destinationPath]")


def parse(xmlFileName):
    cache = {}
    graph = []
    with open(xmlFileName) as fd:
        doc = xmltodict.parse(fd.read())
        for cell in (doc['mxGraphModel']['root']['mxCell']):

            if not cell.get('@edge'):
                # node
                if cell.get('@value'):
                    id = cell.get("@id")
                    # remove html junk in the title
                    value = BeautifulSoup(cell.get("@value")).text
                    node = VueNode(id, value)
                    cache[node.id] = node
                    graph.append(node)
        for cell in (doc['mxGraphModel']['root']['mxCell']):
            if cell.get('@edge'):
                source = cache[cell.get('@source')]
                target = cache[cell.get("@target")]
                if source not in target.components:
                    target.components.append(source)
        del cache
        return graph


def main():
    xmlFileName = sys.argv[1]
    destinationPath = sys.argv[2]

    try:
        graph = parse(xmlFileName)
        graph[0].componentsBasePath = "/components"
        graph[0].create(destinationPath)
        print('done.')

    except Exception as e:
        print(e)
        usage()


main()
