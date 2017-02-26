import xmltodict
from bs4 import BeautifulSoup
import os
import sys


class Node:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.components = []
        self.parent = None
        self.dependencies = []
        self.basePath = ""
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
        for component in self.dependencies:
            # importPath = os.path.normpath(self.componentsBasePath + "/" + component.value)
            importPath = os.path.normpath(findFileFromNode(self,"",component))
            # print(component.basePath)
            importString += "import %s from '%s/%s.vue'\n" % (
                component, importPath,component.value)
            componentsString += "%s," % (component)
            # print(componentsString)
        template = "<template><div id='%s'>%s</div></template>\n<script> %s export default { name: '%s', components: { %s }, } </script>\n<style></style>" % (
            self.value, componentEl, importString, self.value, componentsString)
        return template

    def create(self):
        if not os.path.exists(self.basePath + '/' + self.componentsBasePath):
            os.makedirs(self.basePath + '/' + self.componentsBasePath)

        template = self.render()

        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

        open("{}.vue".format(self.basePath + '/' + self.value), 'w').write(template)

        print("Created %s" % (self.value + '.vue'))

        for component in self.components:
            component.create()

def findFileFromNode(start,path,toFind):
    Q = []
    return findFileFromNodeInner(start,path,toFind,False,Q)


def findFileFromNodeInner(start,path,toFind,wentDown,Q):
    # check if visited
    if start in Q:
        return False
    # check is we reach the top
    if not start:
        return False
    if start.id == toFind.id:
        return path
    # append current node to visited
    Q.append(start)
    # get the foundedPath by searching in the children, it can also be False
    foundedPath = searchInChildren(start,path,toFind,Q)
    if not foundedPath:
        # go one level up and search into the parent
        return findFileFromNodeInner(start.parent, "../" + path, toFind, False,Q)
    return foundedPath

def searchInChildren(start,path,toFind,Q):
    for component in start.components:
        realPath = findFileFromNodeInner(component, path + '/' + component.value, toFind,True,Q)
        if realPath != False:
              return realPath
    return False

def findFile(name):
    for r, d, f in os.walk("./"):
        for files in f:
            if files == name + '.vue':
                return os.path.join(r, files)

def createAllPathes(root,basePath):
    root.basePath = basePath
    for component in root.components:
            newPath = os.path.join(basePath, root.componentsBasePath, component.value)
            createAllPathes(component,newPath)

def createAll(root,destinationPath):
    createAllPathes(root,destinationPath)
    root.create()

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
                    value = BeautifulSoup(cell.get("@value"), "lxml").text
                    node = VueNode(id, value)
                    cache[node.id] = node
                    graph.append(node)

        for cell in (doc['mxGraphModel']['root']['mxCell']):
            if cell.get('@edge'):
                source = cache[cell.get('@source')]
                target = cache[cell.get('@target')]
                if (cell.get('@value') == "Use"):
                    if target not in source.dependencies:
                        source.dependencies.append(target)
                else:
                    if source not in target.components:
                        target.components.append(source)
                        source.parent = target

        del cache
        return graph


def main():
    # xmlFileName = sys.argv[1]
    # destinationPath = sys.argv[2]

    xmlFileName = "e.xml"
    destinationPath = "./"
    # try:
    graph = parse(xmlFileName)
    graph[0].componentsBasePath = "components"
    createAll(graph[0],destinationPath)
    # graph[0].create(destinationPath)
    print('done.')

    # except Exception as e:
    #     print(e)
    #     usage()


main()
